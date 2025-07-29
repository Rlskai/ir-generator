# config.py
import os

# Bot Configuration
BOT_TOKEN = "7927632819:AAFRaxmU8RjpkCSPImPe7xpUXSuPIACX7NY"

# Data Storage
DATA_FILE_PATH = "data/users.json"

# Valid Military Ranks
VALID_RANKS = [
    'REC', 'PTE', 'LCP', 'CPL', 'CFC', '3SG', '2SG', '1SG', 'SSG', 'MSG',
    '3WO', '2WO', '1WO', 'SWO', 'CWO', 'OCT', '2LT', 'LTA', 'CPT', 'MAJ',
    'LTC', 'SLTC', 'COL', 'BG', 'MG', 'LG'
]

# User States for Extended Registration, Comprehensive IR, and Particulars Editing (stored in user profile)
class UserState:
    IDLE = "idle"
    # Registration States
    AWAITING_RANK = "awaiting_rank"
    AWAITING_NAME = "awaiting_name"
    AWAITING_COMPANY = "awaiting_company"
    AWAITING_UNIT = "awaiting_unit"
    AWAITING_CONTACT = "awaiting_contact"
    # Comprehensive IR Generation States
    AWAITING_IR_TYPE = "awaiting_ir_type"
    AWAITING_NATURE_TYPE = "awaiting_nature_type"
    AWAITING_DATE_TIME = "awaiting_date_time"
    AWAITING_SERVICEMAN = "awaiting_serviceman"
    AWAITING_LOCATION = "awaiting_location"
    AWAITING_INJURY = "awaiting_injury"
    AWAITING_DESCRIPTION = "awaiting_description"
    AWAITING_FOLLOWUP = "awaiting_followup"
    # Individual Field Editing States
    EDITING_RANK = "editing_rank"
    EDITING_NAME = "editing_name"
    EDITING_COMPANY = "editing_company"
    EDITING_UNIT = "editing_unit"
    EDITING_CONTACT = "editing_contact"

# IR Template - Comprehensive Military Format
IR_TEMPLATE = """{date_incident} / {unit} / XX / {company} - {ir_type}
1) Nature and Type of Incident:
{nature_type}

2) Date and Time of Incident:
{date_incident} {time_incident}HRS

3) Serviceman Involved:
{serviceman_details}

4) Location of Incident:
{location}

5) Injury/Damage:
{injury_damage}

6) Brief Description of Incident:
{description}

7) Follow Up Updates:
{followup}

8) Stakeholder informed:
a) NOK:YES
b) Date/Time of Verbal Report to GSOC:
c) Date/Time of ESIS Report:
d) Date/Time reported to 9DIV DOO:

9) Unit Reporting POC:
{rank} {full_name}
PC / {company}/ {unit}
{contact_number}"""

# IR Options for Inline Keyboards
IR_TYPES = ["INITIAL", "INITIAL & FINAL", "UPDATE", "UPDATE & FINAL"]
NATURE_TYPES = ["NON-TRAINING RELATED", "TRAINING RELATED"]

# Validation Patterns (Fixed regex syntax with proper closing quotes)
NRIC_PATTERN = r'^[A-Z]\d{7}[A-Z]$'
PES_PATTERN = r'^PES [A-F][1-9]$'
DATE_PATTERN = r'^\d{6}$'  # DDMMYY
TIME_PATTERN = r'^\d{4}HRS?$'  # HHMMHRS (case insensitive)

# Validation Limits
MAX_IR_CONTENT_LENGTH = 4000

# Default User Profile Structure
DEFAULT_USER_PROFILE = {
    "rank": None,
    "full_name": None,
    "company": None,
    "unit": None,
    "contact_number": None,
    "registered": False,
    "state": UserState.IDLE,
    "temp_data": {}
}

# Logging Configuration
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_LEVEL = 'INFO'