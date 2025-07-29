# handlers/message_handler.py
import logging
from telegram import Update
from telegram.ext import ContextTypes

from config import UserState

logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(self, registration_service, response_service, keyboard_service):
        # Use shared service instances including keyboard service
        self.registration_service = registration_service
        self.response_service = response_service
        self.keyboard_service = keyboard_service
        logger.info("MessageHandler initialized with all 3 services")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all text messages based on user registration state"""
        user_id = str(update.effective_user.id)
        message_text = update.message.text.strip()
        
        logger.info(f"Message from user {user_id}: '{message_text}'")
        
        try:
            current_state = self.registration_service.get_user_state(user_id)
            logger.info(f"User {user_id} current state: {current_state}")
            
            if current_state == UserState.AWAITING_RANK:
                await self._handle_rank_input(update, user_id, message_text)
                
            elif current_state == UserState.AWAITING_NAME:
                await self._handle_name_input(update, user_id, message_text)
                
            elif current_state == UserState.AWAITING_COMPANY:
                await self._handle_company_input(update, user_id, message_text)
                
            elif current_state == UserState.AWAITING_UNIT:
                await self._handle_unit_input(update, user_id, message_text)
                
            elif current_state == UserState.AWAITING_CONTACT:
                await self._handle_contact_input(update, user_id, message_text)
                
            elif current_state == UserState.AWAITING_DATE_TIME:
                await self._handle_date_time_input(update, user_id, message_text)
                
            elif current_state == UserState.AWAITING_SERVICEMAN:
                await self._handle_serviceman_input(update, user_id, message_text)
                
            elif current_state == UserState.AWAITING_LOCATION:
                await self._handle_location_input(update, user_id, message_text)
                
            elif current_state == UserState.AWAITING_INJURY:
                await self._handle_injury_input(update, user_id, message_text)
                
            elif current_state == UserState.AWAITING_DESCRIPTION:
                await self._handle_description_input(update, user_id, message_text)
                
            elif current_state == UserState.AWAITING_FOLLOWUP:
                await self._handle_followup_input(update, user_id, message_text)
                
            elif current_state == UserState.EDITING_RANK:
                await self._handle_rank_edit(update, user_id, message_text)
                
            elif current_state == UserState.EDITING_NAME:
                await self._handle_name_edit(update, user_id, message_text)
                
            elif current_state == UserState.EDITING_COMPANY:
                await self._handle_company_edit(update, user_id, message_text)
                
            elif current_state == UserState.EDITING_UNIT:
                await self._handle_unit_edit(update, user_id, message_text)
                
            elif current_state == UserState.EDITING_CONTACT:
                await self._handle_contact_edit(update, user_id, message_text)
                
            else:
                # User is idle or in unknown state
                await update.message.reply_text(
                    "Please use /start to begin the registration process."
                )
                logger.info(f"User {user_id} sent message in idle/unknown state: {current_state}")
                
        except Exception as e:
            logger.error(f"Error handling message from user {user_id}: {e}")
            error_message = self.response_service.format_system_error()
            await update.message.reply_text(error_message)
    
    async def _handle_rank_input(self, update: Update, user_id: str, rank_input: str):
        """Handle rank input during registration"""
        logger.info(f"Processing rank input from user {user_id}: '{rank_input}'")
        
        is_valid, error_message = self.registration_service.validate_rank(rank_input)
        
        if is_valid:
            # Store rank and ask for name
            clean_rank = rank_input.upper().strip()
            self.registration_service.store_user_temp_data(user_id, 'rank', clean_rank)
            
            message = self.response_service.format_name_prompt()
            await update.message.reply_text(message)
            
            self.registration_service.set_user_state(user_id, UserState.AWAITING_NAME)
            logger.info(f"User {user_id} provided valid rank: {clean_rank} - set to AWAITING_NAME")
        else:
            # Invalid rank - ask again
            error_msg = self.response_service.format_validation_error(error_message)
            await update.message.reply_text(error_msg)
            logger.info(f"User {user_id} provided invalid rank: {rank_input}")
    
    async def _handle_name_input(self, update: Update, user_id: str, name_input: str):
        """Handle name input during registration"""
        logger.info(f"Processing name input from user {user_id}: '{name_input}'")
        
        is_valid, error_message = self.registration_service.validate_name(name_input)
        
        if is_valid:
            # Store name and ask for company
            clean_name = name_input.upper().strip()
            self.registration_service.store_user_temp_data(user_id, 'full_name', clean_name)
            
            message = self.response_service.format_company_prompt()
            await update.message.reply_text(message)
            
            self.registration_service.set_user_state(user_id, UserState.AWAITING_COMPANY)
            logger.info(f"User {user_id} provided valid name: {clean_name} - set to AWAITING_COMPANY")
        else:
            # Invalid name - ask again
            error_msg = self.response_service.format_validation_error(error_message)
            await update.message.reply_text(error_msg)
            logger.info(f"User {user_id} provided invalid name: {name_input}")
    
    async def _handle_company_input(self, update: Update, user_id: str, company_input: str):
        """Handle company input during registration"""
        logger.info(f"Processing company input from user {user_id}: '{company_input}'")
        
        is_valid, error_message = self.registration_service.validate_company(company_input)
        
        if is_valid:
            # Store company and ask for unit
            clean_company = company_input.upper().strip()
            self.registration_service.store_user_temp_data(user_id, 'company', clean_company)
            
            message = self.response_service.format_unit_prompt()
            await update.message.reply_text(message)
            
            self.registration_service.set_user_state(user_id, UserState.AWAITING_UNIT)
            logger.info(f"User {user_id} provided valid company: {clean_company} - set to AWAITING_UNIT")
        else:
            # Invalid company - ask again
            error_msg = self.response_service.format_validation_error(error_message)
            await update.message.reply_text(error_msg)
            logger.info(f"User {user_id} provided invalid company: {company_input}")
    
    async def _handle_unit_input(self, update: Update, user_id: str, unit_input: str):
        """Handle unit input during registration"""
        logger.info(f"Processing unit input from user {user_id}: '{unit_input}'")
        
        is_valid, error_message = self.registration_service.validate_unit(unit_input)
        
        if is_valid:
            # Store unit and ask for contact
            clean_unit = unit_input.upper().strip()
            self.registration_service.store_user_temp_data(user_id, 'unit', clean_unit)
            
            message = self.response_service.format_contact_prompt()
            await update.message.reply_text(message)
            
            self.registration_service.set_user_state(user_id, UserState.AWAITING_CONTACT)
            logger.info(f"User {user_id} provided valid unit: {clean_unit} - set to AWAITING_CONTACT")
        else:
            # Invalid unit - ask again
            error_msg = self.response_service.format_validation_error(error_message)
            await update.message.reply_text(error_msg)
            logger.info(f"User {user_id} provided invalid unit: {unit_input}")
    
    async def _handle_contact_input(self, update: Update, user_id: str, contact_input: str):
        """Handle contact number input and complete registration"""
        logger.info(f"Processing contact input from user {user_id}: '{contact_input}'")
        
        is_valid, error_message = self.registration_service.validate_contact_number(contact_input)
        
        if is_valid:
            # Get all stored data and complete registration
            stored_rank = self.registration_service.get_user_temp_data(user_id, 'rank')
            stored_name = self.registration_service.get_user_temp_data(user_id, 'full_name')
            stored_company = self.registration_service.get_user_temp_data(user_id, 'company')
            stored_unit = self.registration_service.get_user_temp_data(user_id, 'unit')
            
            if not all([stored_rank, stored_name, stored_company, stored_unit]):
                # Something went wrong - restart registration
                await update.message.reply_text(
                    "Something went wrong. Please use /start to begin registration again."
                )
                logger.error(f"Missing stored data for user {user_id}")
                return
            
            # Register the user with all 5 fields
            success = self.registration_service.register_user(
                user_id, stored_rank, stored_name, stored_company, stored_unit, contact_input
            )
            
            if success:
                # Registration complete
                particulars = self.registration_service.get_formatted_particulars(user_id)
                message = self.response_service.format_registration_success(particulars)
                
                # Use keyboard service for main menu
                keyboard = self.keyboard_service.get_main_menu_keyboard()
                
                await update.message.reply_text(message, reply_markup=keyboard)
                
                logger.info(f"Successfully registered user {user_id} with all 5 fields")
            else:
                # Registration failed
                error_msg = self.response_service.format_system_error()
                await update.message.reply_text(error_msg)
                logger.error(f"Failed to register user {user_id}")
        else:
            # Invalid contact - ask again
            error_msg = self.response_service.format_validation_error(error_message)
            await update.message.reply_text(error_msg)
            logger.info(f"User {user_id} provided invalid contact: {contact_input}")
    
    # Comprehensive IR Input Handlers
    async def _handle_date_time_input(self, update: Update, user_id: str, date_time_input: str):
        """Handle date and time input during IR generation"""
        logger.info(f"Processing date/time input from user {user_id}: '{date_time_input}'")
        
        is_valid, date_part, time_part, error_message = self.registration_service.validate_date_time(date_time_input)
        
        if is_valid:
            # Store date and time parts
            self.registration_service.store_ir_data(user_id, 'date_incident', date_part)
            self.registration_service.store_ir_data(user_id, 'time_incident', time_part)
            
            message = self.response_service.format_serviceman_prompt()
            await update.message.reply_text(message)
            
            self.registration_service.set_user_state(user_id, UserState.AWAITING_SERVICEMAN)
            logger.info(f"User {user_id} provided valid date/time: {date_part} {time_part}HRS")
        else:
            # Invalid date/time - ask again
            error_msg = self.response_service.format_validation_error(error_message)
            await update.message.reply_text(error_msg)
            logger.info(f"User {user_id} provided invalid date/time: {date_time_input}")
    
    async def _handle_serviceman_input(self, update: Update, user_id: str, serviceman_input: str):
        """Handle serviceman details input during IR generation"""
        logger.info(f"Processing serviceman input from user {user_id}: '{serviceman_input[:20]}...'")
        
        is_valid, formatted_details, error_message = self.registration_service.validate_serviceman_details(serviceman_input)
        
        if is_valid:
            # Store formatted serviceman details
            self.registration_service.store_ir_data(user_id, 'serviceman_details', formatted_details)
            
            message = self.response_service.format_location_prompt()
            await update.message.reply_text(message)
            
            self.registration_service.set_user_state(user_id, UserState.AWAITING_LOCATION)
            logger.info(f"User {user_id} provided valid serviceman details")
        else:
            # Invalid serviceman details - ask again
            error_msg = self.response_service.format_validation_error(error_message)
            await update.message.reply_text(error_msg)
            logger.info(f"User {user_id} provided invalid serviceman details")
    
    async def _handle_location_input(self, update: Update, user_id: str, location_input: str):
        """Handle location input during IR generation"""
        logger.info(f"Processing location input from user {user_id}: '{location_input}'")
        
        is_valid, error_message = self.registration_service.validate_ir_content(location_input)
        
        if is_valid:
            # Store location
            self.registration_service.store_ir_data(user_id, 'location', location_input.strip())
            
            message = self.response_service.format_injury_prompt()
            await update.message.reply_text(message)
            
            self.registration_service.set_user_state(user_id, UserState.AWAITING_INJURY)
            logger.info(f"User {user_id} provided valid location")
        else:
            # Invalid location - ask again
            error_msg = self.response_service.format_validation_error(error_message)
            await update.message.reply_text(error_msg)
            logger.info(f"User {user_id} provided invalid location")
    
    async def _handle_injury_input(self, update: Update, user_id: str, injury_input: str):
        """Handle injury/damage input during IR generation"""
        logger.info(f"Processing injury input from user {user_id}: '{injury_input}'")
        
        is_valid, error_message = self.registration_service.validate_ir_content(injury_input)
        
        if is_valid:
            # Store injury/damage
            self.registration_service.store_ir_data(user_id, 'injury_damage', injury_input.strip())
            
            message = self.response_service.format_description_prompt()
            await update.message.reply_text(message)
            
            self.registration_service.set_user_state(user_id, UserState.AWAITING_DESCRIPTION)
            logger.info(f"User {user_id} provided valid injury/damage")
        else:
            # Invalid injury - ask again
            error_msg = self.response_service.format_validation_error(error_message)
            await update.message.reply_text(error_msg)
            logger.info(f"User {user_id} provided invalid injury")
    
    async def _handle_description_input(self, update: Update, user_id: str, description_input: str):
        """Handle description input during IR generation"""
        logger.info(f"Processing description input from user {user_id}: '{description_input[:50]}...'")
        
        is_valid, error_message = self.registration_service.validate_ir_content(description_input)
        
        if is_valid:
            # Store description
            self.registration_service.store_ir_data(user_id, 'description', description_input.strip())
            
            # Check if IR type contains "FINAL" to determine next step
            ir_type = self.registration_service.get_user_temp_data(user_id, 'ir_type')
            
            if ir_type and "FINAL" in ir_type:
                # Auto-fill final report followup
                self.registration_service.store_ir_data(user_id, 'followup', 'This serves as a final report')
                await self._generate_comprehensive_ir_report(update, user_id)
            else:
                # Ask for follow-up updates
                message = self.response_service.format_followup_prompt()
                await update.message.reply_text(message)
                self.registration_service.set_user_state(user_id, UserState.AWAITING_FOLLOWUP)
            
            logger.info(f"User {user_id} provided valid description")
        else:
            # Invalid description - ask again
            error_msg = self.response_service.format_validation_error(error_message)
            await update.message.reply_text(error_msg)
            logger.info(f"User {user_id} provided invalid description")
    
    async def _handle_followup_input(self, update: Update, user_id: str, followup_input: str):
        """Handle follow-up updates input and generate final report"""
        logger.info(f"Processing followup input from user {user_id}: '{followup_input[:50]}...'")
        
        is_valid, error_message = self.registration_service.validate_ir_content(followup_input)
        
        if is_valid:
            # Store follow-up updates
            self.registration_service.store_ir_data(user_id, 'followup', followup_input.strip())
            
            # Generate comprehensive IR report
            await self._generate_comprehensive_ir_report(update, user_id)
            
            logger.info(f"User {user_id} provided valid followup")
        else:
            # Invalid followup - ask again
            error_msg = self.response_service.format_validation_error(error_message)
            await update.message.reply_text(error_msg)
            logger.info(f"User {user_id} provided invalid followup")
    
    async def _generate_comprehensive_ir_report(self, update: Update, user_id: str):
        """Generate and send comprehensive IR report"""
        try:
            # Get all IR data and user particulars
            ir_data = self.registration_service.complete_comprehensive_ir_creation(user_id)
            user_particulars = self.registration_service.get_user_particulars(user_id)
            
            # Generate final comprehensive report
            final_report = self.response_service.generate_comprehensive_ir_report(ir_data, user_particulars)
            
            # Send report with markdown formatting
            await update.message.reply_text(f"```\n{final_report}\n```", parse_mode='Markdown')
            
            # Send completion message with menu using keyboard service
            completion_message = self.response_service.format_ir_completion_message()
            keyboard = self.keyboard_service.get_main_menu_keyboard()
            
            await update.message.reply_text(completion_message, reply_markup=keyboard)
            
            logger.info(f"Successfully generated comprehensive IR report for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error generating comprehensive IR report for user {user_id}: {e}")
            error_msg = self.response_service.format_system_error()
            await update.message.reply_text(error_msg)
    
    # Individual Field Editing Handlers
    async def _handle_rank_edit(self, update: Update, user_id: str, rank_input: str):
        """Handle rank editing"""
        logger.info(f"Processing rank edit from user {user_id}: '{rank_input}'")
        
        is_valid, error_message = self.registration_service.validate_rank(rank_input)
        
        if is_valid:
            # Update rank field
            success = self.registration_service.update_single_field(user_id, 'rank', rank_input)
            
            if success:
                # Show success and return to details view
                success_msg = self.response_service.format_field_updated_success("Rank")
                await update.message.reply_text(success_msg)
                
                # Show updated details using keyboard service
                particulars = self.registration_service.get_user_particulars(user_id)
                details_msg = self.response_service.format_details_updated_view(particulars)
                keyboard = self.keyboard_service.get_details_view_keyboard()
                
                await update.message.reply_text(details_msg, reply_markup=keyboard)
                self.registration_service.set_user_state(user_id, UserState.IDLE)
                
                logger.info(f"User {user_id} successfully updated rank to {rank_input}")
            else:
                error_msg = self.response_service.format_system_error()
                await update.message.reply_text(error_msg)
        else:
            # Invalid rank - ask again
            error_msg = self.response_service.format_validation_error(error_message)
            await update.message.reply_text(error_msg)
    
    async def _handle_name_edit(self, update: Update, user_id: str, name_input: str):
        """Handle name editing"""
        logger.info(f"Processing name edit from user {user_id}: '{name_input}'")
        
        is_valid, error_message = self.registration_service.validate_name(name_input)
        
        if is_valid:
            # Update name field
            success = self.registration_service.update_single_field(user_id, 'full_name', name_input)
            
            if success:
                success_msg = self.response_service.format_field_updated_success("Name")
                await update.message.reply_text(success_msg)
                
                # Show updated details using keyboard service
                particulars = self.registration_service.get_user_particulars(user_id)
                details_msg = self.response_service.format_details_updated_view(particulars)
                keyboard = self.keyboard_service.get_details_view_keyboard()
                
                await update.message.reply_text(details_msg, reply_markup=keyboard)
                self.registration_service.set_user_state(user_id, UserState.IDLE)
                
                logger.info(f"User {user_id} successfully updated name")
            else:
                error_msg = self.response_service.format_system_error()
                await update.message.reply_text(error_msg)
        else:
            error_msg = self.response_service.format_validation_error(error_message)
            await update.message.reply_text(error_msg)
    
    async def _handle_company_edit(self, update: Update, user_id: str, company_input: str):
        """Handle company editing"""
        logger.info(f"Processing company edit from user {user_id}: '{company_input}'")
        
        is_valid, error_message = self.registration_service.validate_company(company_input)
        
        if is_valid:
            success = self.registration_service.update_single_field(user_id, 'company', company_input)
            
            if success:
                success_msg = self.response_service.format_field_updated_success("Company")
                await update.message.reply_text(success_msg)
                
                particulars = self.registration_service.get_user_particulars(user_id)
                details_msg = self.response_service.format_details_updated_view(particulars)
                keyboard = self.keyboard_service.get_details_view_keyboard()
                
                await update.message.reply_text(details_msg, reply_markup=keyboard)
                self.registration_service.set_user_state(user_id, UserState.IDLE)
                
                logger.info(f"User {user_id} successfully updated company")
            else:
                error_msg = self.response_service.format_system_error()
                await update.message.reply_text(error_msg)
        else:
            error_msg = self.response_service.format_validation_error(error_message)
            await update.message.reply_text(error_msg)
    
    async def _handle_unit_edit(self, update: Update, user_id: str, unit_input: str):
        """Handle unit editing"""
        logger.info(f"Processing unit edit from user {user_id}: '{unit_input}'")
        
        is_valid, error_message = self.registration_service.validate_unit(unit_input)
        
        if is_valid:
            success = self.registration_service.update_single_field(user_id, 'unit', unit_input)
            
            if success:
                success_msg = self.response_service.format_field_updated_success("Unit")
                await update.message.reply_text(success_msg)
                
                particulars = self.registration_service.get_user_particulars(user_id)
                details_msg = self.response_service.format_details_updated_view(particulars)
                keyboard = self.keyboard_service.get_details_view_keyboard()
                
                await update.message.reply_text(details_msg, reply_markup=keyboard)
                self.registration_service.set_user_state(user_id, UserState.IDLE)
                
                logger.info(f"User {user_id} successfully updated unit")
            else:
                error_msg = self.response_service.format_system_error()
                await update.message.reply_text(error_msg)
        else:
            error_msg = self.response_service.format_validation_error(error_message)
            await update.message.reply_text(error_msg)
    
    async def _handle_contact_edit(self, update: Update, user_id: str, contact_input: str):
        """Handle contact editing"""
        logger.info(f"Processing contact edit from user {user_id}: '{contact_input}'")
        
        is_valid, error_message = self.registration_service.validate_contact_number(contact_input)
        
        if is_valid:
            success = self.registration_service.update_single_field(user_id, 'contact_number', contact_input)
            
            if success:
                success_msg = self.response_service.format_field_updated_success("Contact")
                await update.message.reply_text(success_msg)
                
                particulars = self.registration_service.get_user_particulars(user_id)
                details_msg = self.response_service.format_details_updated_view(particulars)
                keyboard = self.keyboard_service.get_details_view_keyboard()
                
                await update.message.reply_text(details_msg, reply_markup=keyboard)
                self.registration_service.set_user_state(user_id, UserState.IDLE)
                
                logger.info(f"User {user_id} successfully updated contact")
            else:
                error_msg = self.response_service.format_system_error()
                await update.message.reply_text(error_msg)
        else:
            error_msg = self.response_service.format_validation_error(error_message)
            await update.message.reply_text(error_msg)