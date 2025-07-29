# handlers/command_handler.py
import logging
from telegram import Update
from telegram.ext import ContextTypes

from config import UserState

logger = logging.getLogger(__name__)

class CommandHandler:
    def __init__(self, registration_service, response_service, keyboard_service):
        # Use shared service instances instead of creating new ones
        self.registration_service = registration_service
        self.response_service = response_service
        self.keyboard_service = keyboard_service
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command - main entry point for registration"""
        user_id = str(update.effective_user.id)
        user_name = update.effective_user.first_name or "User"
        
        logger.info(f"Start command from user {user_id} ({user_name})")
        
        try:
            # Check if user is already registered
            if self.registration_service.is_user_registered(user_id):
                # Existing user - show main menu with both IR and Details options
                particulars = self.registration_service.get_formatted_particulars(user_id)
                message = self.response_service.format_welcome_back_message(particulars)
                keyboard = self.keyboard_service.get_main_menu_keyboard()
                
                await update.message.reply_text(message, reply_markup=keyboard)
                self.registration_service.set_user_state(user_id, UserState.IDLE)
                logger.info(f"Welcomed back existing user {user_id}")
                
            else:
                # New user - start registration process
                message = self.response_service.format_rank_prompt()
                await update.message.reply_text(message)
                self.registration_service.set_user_state(user_id, UserState.AWAITING_RANK)
                logger.info(f"Started registration for new user {user_id} - set to AWAITING_RANK")
                
        except Exception as e:
            logger.error(f"Error in start_command for user {user_id}: {e}")
            error_message = self.response_service.format_system_error()
            await update.message.reply_text(error_message)