# services/inline_keyboard_service.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import IR_TYPES, NATURE_TYPES

class InlineKeyboardService:
    """Service for generating inline keyboards for IR selections"""
    
    def get_main_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Create enhanced main menu inline keyboard with My Details option"""
        keyboard = [
            [InlineKeyboardButton("📝 New IR", callback_data="new_ir")],
            [InlineKeyboardButton("👤 My Details", callback_data="my_details")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_details_view_keyboard(self) -> InlineKeyboardMarkup:
        """Create keyboard for viewing/editing registration details"""
        keyboard = [
            [InlineKeyboardButton("✏️ Edit Rank", callback_data="edit_rank"),
             InlineKeyboardButton("✏️ Edit Name", callback_data="edit_name")],
            [InlineKeyboardButton("✏️ Edit Company", callback_data="edit_company"),
             InlineKeyboardButton("✏️ Edit Unit", callback_data="edit_unit")],
            [InlineKeyboardButton("✏️ Edit Contact", callback_data="edit_contact")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_ir_type_keyboard(self) -> InlineKeyboardMarkup:
        """Create IR type selection keyboard"""
        keyboard = []
        for ir_type in IR_TYPES:
            keyboard.append([InlineKeyboardButton(ir_type, callback_data=f"ir_type_{ir_type.replace(' ', '_').replace('&', 'AND').lower()}")])
        return InlineKeyboardMarkup(keyboard)
    
    def get_nature_type_keyboard(self) -> InlineKeyboardMarkup:
        """Create nature type selection keyboard"""
        keyboard = []
        for nature_type in NATURE_TYPES:
            callback_data = f"nature_{nature_type.replace(' ', '_').replace('-', '_').lower()}"
            keyboard.append([InlineKeyboardButton(nature_type, callback_data=callback_data)])
        return InlineKeyboardMarkup(keyboard)