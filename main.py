# main.py
#!/usr/bin/env python3
"""
IR Report Bot - Registration Phase
Focus: User registration with rank and name prompts
"""

import sys
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from config import BOT_TOKEN, LOGGING_FORMAT, LOGGING_LEVEL
from services.registration_service import RegistrationService
from services.response_service import ResponseService
from services.inline_keyboard_service import InlineKeyboardService
from handlers.command_handler import CommandHandler as IRCommandHandler
from handlers.message_handler import MessageHandler as IRMessageHandler
from handlers.callback_handler import CallbackHandler

# Configure logging
logging.basicConfig(
    format=LOGGING_FORMAT,
    level=getattr(logging, LOGGING_LEVEL)
)
logger = logging.getLogger(__name__)

class IRBot:
    def __init__(self):
        if not BOT_TOKEN:
            raise ValueError("Bot token not found. Please set TELEGRAM_BOT_TOKEN environment variable.")
        
        # Create singleton service instances that persist across requests
        self.registration_service = RegistrationService()
        self.response_service = ResponseService()
        self.keyboard_service = InlineKeyboardService()
        
        # Initialize handlers with shared service instances
        self.command_handler = IRCommandHandler(self.registration_service, self.response_service, self.keyboard_service)
        self.message_handler = IRMessageHandler(self.registration_service, self.response_service, self.keyboard_service)
        self.callback_handler = CallbackHandler(self.registration_service, self.response_service)
        
        # Build application
        self.application = ApplicationBuilder().token(BOT_TOKEN).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup bot handlers for registration and IR generation process"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.command_handler.start_command))
        
        # Callback handlers (inline keyboard buttons)
        self.application.add_handler(CallbackQueryHandler(self.callback_handler.handle_callback))
        
        # Message handlers (text input for rank, name, IR1, IR2)
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler.handle_message)
        )
    
    def run(self):
        """Start the bot"""
        logger.info("Starting IR Report Bot - Registration & IR Generation...")
        print("🤖 IR Report Bot (Registration & IR Generation) started successfully!")
        print("🚀 Bot is running... Press Ctrl+C to stop.")
        self.application.run_polling()

def main():
    """Main function to start the IR Report Bot"""
    try:
        bot = IRBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user.")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("💡 Please set your bot token: export TELEGRAM_BOT_TOKEN='your_token_here'")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()