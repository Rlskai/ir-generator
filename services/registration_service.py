# services/registration_service.py
import json
import os
import re
import logging
from typing import Dict, Optional, Tuple, Any

from config import DATA_FILE_PATH, VALID_RANKS, UserState, DEFAULT_USER_PROFILE, MAX_IR_CONTENT_LENGTH, NRIC_PATTERN, PES_PATTERN, DATE_PATTERN, TIME_PATTERN

logger = logging.getLogger(__name__)

class RegistrationService:
    def __init__(self):
        self.data_file = DATA_FILE_PATH
        self.users_data = self._load_users()
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def _load_users(self) -> Dict:
        """Load users data from JSON file, create empty dict if file doesn't exist"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"Loaded {len(data)} users from {self.data_file}")
                    return data
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Error loading users file: {e}")
                return {}
        logger.info("No existing users file found, starting fresh")
        return {}
    
    def _save_users(self) -> bool:
        """Save users data to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.users_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved users data to {self.data_file}")
            return True
        except IOError as e:
            logger.error(f"Error saving users file: {e}")
            return False
    
    def _get_user_profile(self, user_id: str) -> Dict:
        """Get user profile, create default if doesn't exist"""
        user_key = str(user_id)
        if user_key not in self.users_data:
            # Create new user profile with default values
            self.users_data[user_key] = DEFAULT_USER_PROFILE.copy()
            self.users_data[user_key]["temp_data"] = {}  # Ensure temp_data is a fresh dict
            self._save_users()
            logger.info(f"Created new user profile for {user_id}")
        
        return self.users_data[user_key]
    
    def _update_user_profile(self, user_id: str, updates: Dict) -> bool:
        """Update user profile and save to file"""
        user_key = str(user_id)
        profile = self._get_user_profile(user_id)
        profile.update(updates)
        return self._save_users()
    
    def is_user_registered(self, user_id: str) -> bool:
        """Check if user is already registered"""
        profile = self._get_user_profile(user_id)
        is_registered = profile.get("registered", False)
        logger.info(f"User {user_id} registration check: {is_registered}")
        return is_registered
    
    def validate_rank(self, rank: str) -> Tuple[bool, str]:
        """
        Validate military rank
        
        Args:
            rank: Raw rank input from user
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        rank = rank.strip().upper()
        logger.info(f"Validating rank: '{rank}'")
        
        if not rank:
            return False, "Rank cannot be empty."
        
        if rank not in VALID_RANKS:
            valid_ranks_str = ", ".join(VALID_RANKS)
            return False, f"Invalid rank: {rank}\n\nValid ranks: {valid_ranks_str}"
        
        logger.info(f"Rank '{rank}' is valid")
        return True, ""
    
    def validate_name(self, name: str) -> Tuple[bool, str]:
        """
        Validate full name
        
        Args:
            name: Raw name input from user
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        name = name.strip()
        logger.info(f"Validating name: '{name}'")
        
        if not name:
            return False, "Name cannot be empty."
        
        # Validate full name (only letters, spaces, and common name characters)
        if not re.match(r'^[A-Za-z\s\-\'.]+$', name):
            return False, "Name can only contain letters, spaces, hyphens, and apostrophes."
        
        # Check for minimum length
        if len(name) < 2:
            return False, "Name must be at least 2 characters long."
        
        logger.info(f"Name '{name}' is valid")
        return True, ""
    
    def validate_company(self, company: str) -> Tuple[bool, str]:
        """
        Validate company
        
        Args:
            company: Raw company input from user
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        company = company.strip()
        logger.info(f"Validating company: '{company}'")
        
        if not company:
            return False, "Company cannot be empty."
        
        # Basic validation - letters, numbers, spaces, and common characters
        if not re.match(r'^[A-Za-z0-9\s\-\'.&()]+$', company):
            return False, "Company can only contain letters, numbers, spaces, hyphens, apostrophes, periods, ampersands, and parentheses."
        
        # Check for minimum length  
        if len(company) < 1:
            return False, "Company must be at least 1 character long."
        
        logger.info(f"Company '{company}' is valid")
        return True, ""
    
    def validate_unit(self, unit: str) -> Tuple[bool, str]:
        """
        Validate unit
        
        Args:
            unit: Raw unit input from user
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        unit = unit.strip()
        logger.info(f"Validating unit: '{unit}'")
        
        if not unit:
            return False, "Unit cannot be empty."
        
        # Basic validation - letters, numbers, spaces, and common characters
        if not re.match(r'^[A-Za-z0-9\s\-\'.&()/]+$', unit):
            return False, "Unit can only contain letters, numbers, spaces, hyphens, apostrophes, periods, ampersands, parentheses, and forward slashes."
        
        # Check for minimum length
        if len(unit) < 1:
            return False, "Unit must be at least 1 character long."
        
        logger.info(f"Unit '{unit}' is valid")
        return True, ""
    
    def validate_contact_number(self, contact: str) -> Tuple[bool, str]:
        """
        Validate contact number
        
        Args:
            contact: Raw contact number input from user
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        contact = contact.strip()
        logger.info(f"Validating contact number: '{contact}'")
        
        if not contact:
            return False, "Contact number cannot be empty."
        
        # Remove common separators for validation
        clean_contact = re.sub(r'[\s\-\+\(\)]', '', contact)
        
        # Remove +65 prefix if present
        if clean_contact.startswith('65') and len(clean_contact) == 10:
            clean_contact = clean_contact[2:]
        
        # Basic validation - should be 8 digits starting with 8 or 9
        if not re.match(r'^[89]\d{7}$', clean_contact):
            return False, "Please provide a valid Singapore mobile number (8 digits starting with 8 or 9, e.g., 91234567)."
        
        logger.info(f"Contact number '{contact}' is valid")
        return True, ""
    
    def validate_ir_content(self, content: str) -> Tuple[bool, str]:
        """
        Validate IR content (basic validation)
        
        Args:
            content: IR content to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        content = content.strip()
        
        if not content:
            return False, "IR content cannot be empty."
        
        if len(content) > MAX_IR_CONTENT_LENGTH:
            return False, f"IR content is too long. Please keep it under {MAX_IR_CONTENT_LENGTH} characters."
        
        return True, ""
    
    def validate_date_time(self, date_time_input: str) -> Tuple[bool, str, str, str]:
        """
        Validate date and time input in format DDMMYY HHMMHRS
        
        Args:
            date_time_input: Raw date/time input from user
            
        Returns:
            Tuple of (is_valid, date_part, time_part, error_message)
        """
        date_time_input = date_time_input.strip()
        
        if not date_time_input:
            return False, "", "", "Date and time cannot be empty."
        
        # Split into date and time parts
        parts = date_time_input.split()
        if len(parts) != 2:
            return False, "", "", "Please provide date and time in format: DDMMYY HHMMHRS"
        
        date_part, time_part = parts[0], parts[1].upper()
        
        # Validate date format (DDMMYY)
        if not re.match(DATE_PATTERN, date_part):
            return False, "", "", "Date must be in DDMMYY format (e.g., 160625)"
        
        # Validate time format (HHMMHRS)
        if not re.match(TIME_PATTERN, time_part):
            return False, "", "", "Time must be in HHMMHRS format (e.g., 1730HRS)"
        
        # Extract time numbers for validation
        time_nums = time_part[:4]
        hours = int(time_nums[:2])
        minutes = int(time_nums[2:])
        
        if hours > 23 or minutes > 59:
            return False, "", "", "Invalid time. Hours must be 00-23, minutes must be 00-59"
        
        # Basic date validation
        day = int(date_part[:2])
        month = int(date_part[2:4])
        
        if day < 1 or day > 31 or month < 1 or month > 12:
            return False, "", "", "Invalid date. Please check day (01-31) and month (01-12)"
        
        return True, date_part, time_nums, ""
    
    def validate_serviceman_details(self, details: str) -> Tuple[bool, str, str]:
        """
        Validate serviceman details in format NRIC/RANK NAME/4D/NSF/PES
        
        Args:
            details: Raw serviceman details from user
            
        Returns:
            Tuple of (is_valid, formatted_details, error_message)
        """
        details = details.strip()
        
        if not details:
            return False, "", "Serviceman details cannot be empty."
        
        # Split by forward slash
        parts = details.split('/')
        if len(parts) != 5:
            return False, "", "Please provide all 5 components: NRIC/RANK NAME/4D/NSF/PES"
        
        nric, rank_name, four_d, nsf, pes = [part.strip() for part in parts]
        
        # Validate NRIC format (strict)
        if not re.match(NRIC_PATTERN, nric.upper()):
            return False, "", "NRIC must be in format: Letter + 7 digits + Letter (e.g., T0123456D)"
        
        # Validate PES format (strict)
        if not re.match(PES_PATTERN, pes.upper()):
            return False, "", "PES must be in format: PES [A-F][1-4] (e.g., PES B1)"
        
        # Basic validation for other fields
        if not rank_name:
            return False, "", "Rank and name cannot be empty"
        
        if not four_d:
            return False, "", "4D number cannot be empty"
        
        if nsf.upper() != "NSF":
            return False, "", "Fourth field must be 'NSF'"
        
        # Format with proper spacing and auto-insert / after first NRIC letter
        formatted_nric = nric[0].upper() + "/" + nric[1:].upper()
        formatted_details = f"{formatted_nric}/{rank_name.upper()}/{four_d.upper()}/{nsf.upper()}/{pes.upper()}"
        
        return True, formatted_details, ""
    
    def register_user(self, user_id: str, rank: str, full_name: str, company: str, unit: str, contact_number: str) -> bool:
        """Register a new user by updating their profile with all 5 fields"""
        try:
            # Clean contact number to 8 digits
            clean_contact = re.sub(r'[\s\-\+\(\)]', '', contact_number)
            if clean_contact.startswith('65') and len(clean_contact) == 10:
                clean_contact = clean_contact[2:]
            
            updates = {
                "rank": rank.upper().strip(),
                "full_name": full_name.upper().strip(),
                "company": company.upper().strip(),
                "unit": unit.upper().strip(),
                "contact_number": clean_contact,
                "registered": True,
                "state": UserState.IDLE,
                "temp_data": {}  # Clear temp data after registration
            }
            
            success = self._update_user_profile(user_id, updates)
            
            if success:
                logger.info(f"Successfully registered user {user_id}: {rank} {full_name} - {company} - {unit} - {clean_contact}")
            else:
                logger.error(f"Failed to save registration for user {user_id}")
            
            return success
        except Exception as e:
            logger.error(f"Error registering user {user_id}: {e}")
            return False
    
    def get_user_particulars(self, user_id: str) -> Optional[Dict[str, str]]:
        """Get user's personal particulars"""
        profile = self._get_user_profile(user_id)
        if profile.get("registered", False):
            return {
                "rank": profile.get("rank"),
                "full_name": profile.get("full_name"),
                "company": profile.get("company"),
                "unit": profile.get("unit"),
                "contact_number": profile.get("contact_number")
            }
        return None
    
    def get_formatted_particulars(self, user_id: str) -> str:
        """Get formatted personal particulars for display (all 5 fields)"""
        particulars = self.get_user_particulars(user_id)
        if particulars and all(particulars.values()):
            return f"{particulars['rank']} {particulars['full_name']} - {particulars['company']} - {particulars['unit']} - {particulars['contact_number']}"
        return ""
    
    # File-Based State Management Methods
    def get_user_state(self, user_id: str) -> str:
        """Get current state for specific user from their profile"""
        profile = self._get_user_profile(user_id)
        state = profile.get("state", UserState.IDLE)
        logger.debug(f"User {user_id} current state: {state}")
        return state
    
    def set_user_state(self, user_id: str, state: str) -> None:
        """Set state for specific user in their profile"""
        profile = self._get_user_profile(user_id)
        old_state = profile.get("state", "none")
        
        updates = {"state": state}
        
        # Clear temp data when user goes to idle state
        if state == UserState.IDLE:
            updates["temp_data"] = {}
        
        self._update_user_profile(user_id, updates)
        logger.info(f"User {user_id} state change: {old_state} -> {state}")
    
    def clear_user_state(self, user_id: str) -> None:
        """Clear state for specific user"""
        updates = {
            "state": UserState.IDLE,
            "temp_data": {}
        }
        self._update_user_profile(user_id, updates)
        logger.info(f"Cleared state for user {user_id}")
    
    # File-Based Temporary Data Management
    def store_user_temp_data(self, user_id: str, key: str, value: Any) -> None:
        """Store temporary data for specific user in their profile"""
        profile = self._get_user_profile(user_id)
        temp_data = profile.get("temp_data", {})
        temp_data[key] = value
        
        self._update_user_profile(user_id, {"temp_data": temp_data})
        logger.debug(f"Stored temp data for user {user_id}: {key} = {value}")
    
    def get_user_temp_data(self, user_id: str, key: str) -> Optional[Any]:
        """Get temporary data for specific user from their profile"""
        profile = self._get_user_profile(user_id)
        temp_data = profile.get("temp_data", {})
        value = temp_data.get(key)
        logger.debug(f"Retrieved temp data for user {user_id}: {key} = {value}")
        return value
    
    def clear_user_temp_data(self, user_id: str) -> None:
        """Clear all temporary data for specific user"""
        profile = self._get_user_profile(user_id)
        old_temp_data = profile.get("temp_data", {})
        
        self._update_user_profile(user_id, {"temp_data": {}})
        
        if old_temp_data:
            logger.debug(f"Cleared temp data for user {user_id}: {old_temp_data}")
        else:
            logger.debug(f"No temp data to clear for user {user_id}")
    
    # Utility Methods
    def get_all_user_states(self) -> Dict[str, str]:
        """Get all user states (for debugging)"""
        states = {}
        for user_id, profile in self.users_data.items():
            states[user_id] = profile.get("state", UserState.IDLE)
        return states
    
    def get_active_users_count(self) -> int:
        """Get count of users currently in non-idle state"""
        active_count = 0
        for profile in self.users_data.values():
            if profile.get("state", UserState.IDLE) != UserState.IDLE:
                active_count += 1
        return active_count
    
    def get_user_profile_summary(self, user_id: str) -> Dict:
        """Get user profile summary for debugging"""
        profile = self._get_user_profile(user_id)
        return {
            "registered": profile.get("registered", False),
            "state": profile.get("state", UserState.IDLE),
            "has_temp_data": bool(profile.get("temp_data", {})),
            "particulars": self.get_formatted_particulars(user_id) if profile.get("registered") else None
        }
    
    # IR Generation Methods
    def start_ir_creation(self, user_id: str) -> None:
        """Initialize comprehensive IR creation process"""
        self.set_user_state(user_id, UserState.AWAITING_IR_TYPE)
        # Clear any existing IR data
        profile = self._get_user_profile(user_id)
        temp_data = profile.get("temp_data", {})
        
        # Clear all IR-related temp data
        ir_keys = ['ir_type', 'nature_type', 'date_incident', 'time_incident', 
                   'serviceman_details', 'location', 'injury_damage', 'description', 'followup']
        for key in ir_keys:
            temp_data.pop(key, None)
            
        self._update_user_profile(user_id, {"temp_data": temp_data})
        logger.info(f"Started comprehensive IR creation for user {user_id}")
    
    def store_ir_data(self, user_id: str, key: str, value: str) -> None:
        """Store IR-related data"""
        self.store_user_temp_data(user_id, key, value)
        logger.info(f"Stored IR data for user {user_id}: {key}")
    
    def get_comprehensive_ir_data(self, user_id: str) -> dict[str, str]:
        """Get all comprehensive IR data"""
        profile = self._get_user_profile(user_id)
        temp_data = profile.get("temp_data", {})
        
        return {
            'ir_type': temp_data.get('ir_type', ''),
            'nature_type': temp_data.get('nature_type', ''),
            'date_incident': temp_data.get('date_incident', ''),
            'time_incident': temp_data.get('time_incident', ''),
            'serviceman_details': temp_data.get('serviceman_details', ''),
            'location': temp_data.get('location', ''),
            'injury_damage': temp_data.get('injury_damage', ''),
            'description': temp_data.get('description', ''),
            'followup': temp_data.get('followup', '')
        }
    
    def update_single_field(self, user_id: str, field: str, value: str) -> bool:
        """
        Update a single registration field
        
        Args:
            user_id: User ID
            field: Field name (rank, full_name, company, unit, contact_number)
            value: New value for the field
            
        Returns:
            Success status
        """
        try:
            profile = self._get_user_profile(user_id)
            
            if not profile.get("registered", False):
                logger.error(f"Attempted to update field for unregistered user {user_id}")
                return False
            
            # Clean the value based on field type
            if field == "contact_number":
                # Clean contact number to 8 digits
                clean_contact = re.sub(r'[\s\-\+\(\)]', '', value)
                if clean_contact.startswith('65') and len(clean_contact) == 10:
                    clean_contact = clean_contact[2:]
                updates = {field: clean_contact}
            else:
                # Other fields - just uppercase and strip
                updates = {field: value.upper().strip()}
            
            success = self._update_user_profile(user_id, updates)
            
            if success:
                logger.info(f"Updated {field} for user {user_id}: {value}")
            else:
                logger.error(f"Failed to update {field} for user {user_id}")
            
            return success
        except Exception as e:  # ← Added missing except block
            logger.error(f"Error updating {field} for user {user_id}: {e}")
            return False
        
    def complete_comprehensive_ir_creation(self, user_id: str) -> dict[str, str]:
        """Complete comprehensive IR creation and return to idle"""
        ir_data = self.get_comprehensive_ir_data(user_id)
        self.set_user_state(user_id, UserState.IDLE)
        logger.info(f"Completed comprehensive IR creation for user {user_id}")
        return ir_data