from .email import EmailMedium
from .sms import SMSMedium

# Import other mediums as needed

MEDIUM_HANDLERS = {
    "sms": SMSMedium(),
    "email": EmailMedium(),
    # Add other mediums here
}
