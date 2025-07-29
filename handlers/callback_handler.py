# handlers/callback_handler.py
import logging
from telegram import Update
from telegram.ext import ContextTypes

from config import UserState
from services.inline_keyboard_service import InlineKeyboardService

logger = logging.getLogger(__name__)

class CallbackHandler:
    def __init__(self, registration_service, response_service):
        # Use shared service instances
        self.registration_service = registration_service
        self.response_service = response_service
        self.keyboard_service = InlineKeyboardService()
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard button presses"""
        query = update.callback_query
        user_id = str(query.from_user.id)
        
        logger.info(f"Callback from user {user_id}: {query.data}")
        
        try:
            await query.answer()  # Acknowledge the callback
            
            if query.data == "new_ir":
                await self._handle_new_ir(query, user_id)
                
            elif query.data.startswith("ir_type_"):
                await self._handle_ir_type_selection(query, user_id, query.data)
                
            elif query.data.startswith("nature_"):
                await self._handle_nature_type_selection(query, user_id, query.data)
                
            elif query.data == "my_details":
                await self._handle_my_details(query, user_id)
                
            elif query.data.startswith("edit_"):
                await self._handle_edit_field(query, user_id, query.data)
                
            elif query.data == "back_to_main":
                await self._handle_back_to_main(query, user_id)
                
        except Exception as e:
            logger.error(f"Error in handle_callback for user {user_id}: {e}")
            error_message = self.response_service.format_system_error()
            await query.edit_message_text(error_message)
    
    async def _handle_new_ir(self, query, user_id: str):
        """Handle 'New IR' button click - Start comprehensive IR creation"""
        # Check if user is registered
        if not self.registration_service.is_user_registered(user_id):
            await query.edit_message_text(
                "Please complete registration first by using /start"
            )
            logger.warning(f"Unregistered user {user_id} tried to create IR")
            return
        
        # Start comprehensive IR creation process
        self.registration_service.start_ir_creation(user_id)
        
        # Show IR type selection keyboard
        message = "Select the type of IR:"
        keyboard = self.keyboard_service.get_ir_type_keyboard()
        await query.edit_message_text(message, reply_markup=keyboard)
        
        logger.info(f"Started comprehensive IR creation for user {user_id}")
    
    async def _handle_ir_type_selection(self, query, user_id: str, callback_data: str):
        """Handle IR type selection"""
        # Extract IR type from callback data
        ir_type_map = {
            "ir_type_initial": "INITIAL",
            "ir_type_initial_and_final": "INITIAL & FINAL", 
            "ir_type_update": "UPDATE",
            "ir_type_update_and_final": "UPDATE & FINAL"
        }
        
        ir_type = ir_type_map.get(callback_data)
        if not ir_type:
            await query.edit_message_text("Invalid IR type selected. Please try again.")
            return
        
        # Store IR type and move to nature selection
        self.registration_service.store_ir_data(user_id, 'ir_type', ir_type)
        self.registration_service.set_user_state(user_id, UserState.AWAITING_NATURE_TYPE)
        
        message = "Select the nature and type of incident:"
        keyboard = self.keyboard_service.get_nature_type_keyboard()
        await query.edit_message_text(message, reply_markup=keyboard)
        
        logger.info(f"User {user_id} selected IR type: {ir_type}")
    
    async def _handle_nature_type_selection(self, query, user_id: str, callback_data: str):
        """Handle nature type selection"""
        # Extract nature type from callback data
        nature_type_map = {
            "nature_non_training_related": "NON-TRAINING RELATED",
            "nature_training_related": "TRAINING RELATED"
        }
        
        nature_type = nature_type_map.get(callback_data)
        if not nature_type:
            await query.edit_message_text("Invalid nature type selected. Please try again.")
            return
        
        # Store nature type and move to date/time input
        self.registration_service.store_ir_data(user_id, 'nature_type', nature_type)
        self.registration_service.set_user_state(user_id, UserState.AWAITING_DATE_TIME)
        
        message = self.response_service.format_date_time_prompt()
        await query.edit_message_text(message)
        
        logger.info(f"User {user_id} selected nature type: {nature_type}")
    
    async def _handle_my_details(self, query, user_id: str):
        """Handle 'My Details' button click - Show comprehensive details view"""
        # Check if user is registered
        if not self.registration_service.is_user_registered(user_id):
            await query.edit_message_text(
                "Please complete registration first by using /start"
            )
            logger.warning(f"Unregistered user {user_id} tried to view details")
            return
        
        # Get user particulars and show details view
        particulars = self.registration_service.get_user_particulars(user_id)
        if not particulars:
            await query.edit_message_text("Error retrieving your details. Please try again.")
            logger.error(f"Failed to retrieve particulars for user {user_id}")
            return
        
        # Format the details view message
        details_message = self.response_service.format_details_view(particulars)
        keyboard = self.keyboard_service.get_details_view_keyboard()
        
        await query.edit_message_text(details_message, reply_markup=keyboard)
        
        logger.info(f"User {user_id} viewed their details: {self.registration_service.get_formatted_particulars(user_id)}")
    
    async def _handle_edit_field(self, query, user_id: str, callback_data: str):
        """Handle edit field button clicks"""
        # Extract field name from callback data
        field = callback_data.replace("edit_", "")
        
        # Get current value
        particulars = self.registration_service.get_user_particulars(user_id)
        if not particulars:
            await query.edit_message_text("Error retrieving your details. Please try again.")
            return
        
        # Set appropriate editing state and show prompt
        field_state_map = {
            "rank": UserState.EDITING_RANK,
            "name": UserState.EDITING_NAME,
            "company": UserState.EDITING_COMPANY,
            "unit": UserState.EDITING_UNIT,
            "contact": UserState.EDITING_CONTACT
        }
        
        field_prompt_map = {
            "rank": lambda: self.response_service.format_edit_rank_prompt(particulars.get('rank', '')),
            "name": lambda: self.response_service.format_edit_name_prompt(particulars.get('full_name', '')),
            "company": lambda: self.response_service.format_edit_company_prompt(particulars.get('company', '')),
            "unit": lambda: self.response_service.format_edit_unit_prompt(particulars.get('unit', '')),
            "contact": lambda: self.response_service.format_edit_contact_prompt(particulars.get('contact_number', ''))
        }
        
        if field not in field_state_map:
            await query.edit_message_text("Invalid field selected. Please try again.")
            return
        
        # Set editing state and show prompt
        self.registration_service.set_user_state(user_id, field_state_map[field])
        message = field_prompt_map[field]()
        await query.edit_message_text(message)
        
        logger.info(f"User {user_id} started editing {field}")
    
    async def _handle_back_to_main(self, query, user_id: str):
        """Handle back to main menu button"""
        # Get user particulars for welcome message
        particulars = self.registration_service.get_formatted_particulars(user_id)
        message = self.response_service.format_welcome_back_message(particulars)
        keyboard = self.keyboard_service.get_main_menu_keyboard()
        
        await query.edit_message_text(message, reply_markup=keyboard)
        self.registration_service.set_user_state(user_id, UserState.IDLE)
        
        logger.info(f"User {user_id} returned to main menu")