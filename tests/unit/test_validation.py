from src.utils.validation import is_valid_email, is_valid_uuid

def test_is_valid_email_edge_cases():
    assert not is_valid_email("user@.com")
    assert not is_valid_email("user@domain.c")   # TLD muy corto
    assert not is_valid_email("plainaddress")
    assert not is_valid_email("missing@domain")
    assert is_valid_email("user@domain.com")
    assert is_valid_email("user.name@domain.co.uk")
    # también válido con guiones
    assert is_valid_email("user-name@domain-site.com")

def test_is_valid_uuid():
    assert is_valid_uuid("123e4567-e89b-12d3-a456-426614174000") is True
    assert is_valid_uuid("123") is False
    assert is_valid_uuid("not-a-uuid") is False
    assert is_valid_uuid("") is False