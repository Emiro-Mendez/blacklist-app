import re
import uuid

def is_valid_email(email):
    # TLD final de al menos 2 caracteres; permite múltiples segmentos (ej. co.uk)
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9-]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_uuid(val):
    try:
        uuid.UUID(val)
        return True
    except ValueError:
        return False