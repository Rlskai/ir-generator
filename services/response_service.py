# services/response_service.py
from config import VALID_RANKS, IR_TEMPLATE

class ResponseService:
    """Service for generating user-facing messages during registration and comprehensive IR generation"""
    
    def format_rank_prompt(self) -> str:
        """Format prompt for rank input"""
        ranks_str = ", ".join(VALID_RANKS)
        return f"""Please provide your military rank:

Valid ranks: {ranks_str}

Example: 2LT"""
    
    def format_name_prompt(self) -> str:
        """Format prompt for name input after rank is provided"""
        return """Great! Now please provide your full name:

Example: RYAN LIM SHUEN KAI"""
    
    def format_company_prompt(self) -> str:
        """Format prompt for company input after name is provided"""
        return """Please provide your company:

Example: ALPHA COMPANY"""
    
    def format_unit_prompt(self) -> str:
        """Format prompt for unit input after company is provided"""
        return """Please provide your unit:

Example: 1ST BATTALION"""
    
    def format_contact_prompt(self) -> str:
        """Format prompt for contact number input after unit is provided"""
        return """Finally, please provide your contact number:

Example: 91234567"""
    
    def format_registration_success(self, particulars: str) -> str:
        """Format registration success message (concise)"""
        return f"""✅ Registration successful!

{particulars}

You can now create IR reports using the button below."""
    
    def format_welcome_back_message(self, particulars: str) -> str:
        """Format welcome back message for existing users"""
        return f"""Welcome back, {particulars}! 👋

Ready to create a new IR report?"""
    
    # Comprehensive IR Generation Prompts
    def format_date_time_prompt(self) -> str:
        """Format prompt for date and time input"""
        return """Please provide the date and time of incident:

Format: DDMMYY HHMMHRS
Example: 160625 1730HRS"""
    
    def format_serviceman_prompt(self) -> str:
        """Format prompt for serviceman details input (with masked example)"""
        return """Please provide serviceman details:

Format: NRIC/RANK NAME/4D/NSF/PES
Example: TXXXX356D/PTE XXX/S3234/NSF/PES B1"""
    
    def format_location_prompt(self) -> str:
        """Format prompt for location input"""
        return """Please provide the location of incident:

Example: Pasir Lebar Medical Centre"""
    
    def format_injury_prompt(self) -> str:
        """Format prompt for injury/damage input"""
        return """Please describe the injury or damage:

Example: Anxiety issues"""
    
    def format_description_prompt(self) -> str:
        """Format prompt for brief description input"""
        return """Please provide a brief description of the incident:

Example: On 160625 PTE XXXX brought up that he was given a 32D MC..."""
    
    def format_followup_prompt(self) -> str:
        """Format prompt for follow-up updates input"""
        return """Please provide follow-up updates (include date and time):

Example: 120625 1400HRS - Medical review completed, MC extended"""
    
    # Particulars Viewing and Editing Methods
    def format_details_view(self, particulars: dict[str, str]) -> str:
        """Format current details display for viewing/editing"""
        return f"""Your Current Details:

Rank: {particulars.get('rank', 'Not set')}
Name: {particulars.get('full_name', 'Not set')}
Company: {particulars.get('company', 'Not set')}
Unit: {particulars.get('unit', 'Not set')}
Contact: {particulars.get('contact_number', 'Not set')}

Select a field to edit or return to the main menu:"""
    
    def format_edit_rank_prompt(self, current_rank: str) -> str:
        """Prompt for editing rank"""
        ranks_str = ", ".join(VALID_RANKS)
        return f"""Current rank: {current_rank}

Please provide your updated military rank:

Valid ranks: {ranks_str}

Example: CPT"""
    
    def format_edit_name_prompt(self, current_name: str) -> str:
        """Prompt for editing name"""
        return f"""Current name: {current_name}

Please provide your updated full name:

Example: SARAH TAN WEI LING"""
    
    def format_edit_company_prompt(self, current_company: str) -> str:
        """Prompt for editing company"""
        return f"""Current company: {current_company}

Please provide your updated company:

Example: BRAVO COMPANY"""
    
    def format_edit_unit_prompt(self, current_unit: str) -> str:
        """Prompt for editing unit"""
        return f"""Current unit: {current_unit}

Please provide your updated unit:

Example: 2ND BATTALION"""
    
    def format_edit_contact_prompt(self, current_contact: str) -> str:
        """Prompt for editing contact"""
        return f"""Current contact: {current_contact}

Please provide your updated contact number:

Example: 81234567"""
    
    def format_field_updated_success(self, field_name: str) -> str:
        """Success message after field update - shows full details after"""
        return f"✅ {field_name} updated successfully!"
    
    def format_my_details_header(self) -> str:
        """Header message when user views their details"""
        return "📋 Here are your current registration details:"
    
    def format_details_updated_view(self, particulars: dict[str, str]) -> str:
        """Format updated details display after a field edit"""
        return f"""Your Updated Details:

Rank: {particulars.get('rank', 'Not set')}
Name: {particulars.get('full_name', 'Not set')}
Company: {particulars.get('company', 'Not set')}
Unit: {particulars.get('unit', 'Not set')}
Contact: {particulars.get('contact_number', 'Not set')}

Select another field to edit or return to the main menu:"""
    
    def generate_comprehensive_ir_report(self, ir_data: dict[str, str], user_particulars: dict[str, str]) -> str:
        """
        Generate complete IR report using comprehensive template
        
        Args:
            ir_data: Dict with all IR fields
            user_particulars: Dict with rank, full_name, company, unit, contact_number
            
        Returns:
            Complete formatted IR report
        """
        return IR_TEMPLATE.format(
            date_incident=ir_data.get('date_incident', ''),
            unit=user_particulars.get('unit', ''),
            company=user_particulars.get('company', ''),
            ir_type=ir_data.get('ir_type', ''),
            nature_type=ir_data.get('nature_type', ''),
            time_incident=ir_data.get('time_incident', ''),
            serviceman_details=ir_data.get('serviceman_details', ''),
            location=ir_data.get('location', ''),
            injury_damage=ir_data.get('injury_damage', ''),
            description=ir_data.get('description', ''),
            followup=ir_data.get('followup', ''),
            rank=user_particulars.get('rank', ''),
            full_name=user_particulars.get('full_name', ''),
            contact_number=user_particulars.get('contact_number', '')
        )
    
    def format_ir_completion_message(self) -> str:
        """Format message when comprehensive IR is completed"""
        return """✅ Comprehensive IR Report Generated Successfully!

Your complete IR report is shown above. You can create another IR report using the button below."""
    
    def format_validation_error(self, error_message: str) -> str:
        """Format validation error message"""
        return f"❌ {error_message}\n\nPlease try again."
    
    def format_system_error(self) -> str:
        """Format system error message"""
        return """❌ System error occurred. Please try again later.

If the problem persists, please contact the administrator."""