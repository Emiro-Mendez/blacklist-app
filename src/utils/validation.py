import re
import uuid

def is_valid_email(email):
    # Permite TLDs con múltiples partes (ej. co.uk, com.mx)
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+$'
    return re.match(pattern, email) is not None

def is_valid_uuid(val):
    try:
        uuid.UUID(val)
        return True
    except ValueError:
        return False