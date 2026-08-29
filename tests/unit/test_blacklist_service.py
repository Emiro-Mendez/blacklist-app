import pytest
from src.services.blacklist_service import BlacklistService
from src.models.errors import ConflictError

def test_add_email_success(mocker):
    mock_repo = mocker.MagicMock()
    mock_repo.get_by_email.return_value = None
    mock_entry = mocker.MagicMock()
    mock_repo.create.return_value = mock_entry

    service = BlacklistService(repo=mock_repo)
    result = service.add_email("test@example.com", "123e4567-e89b-12d3-a456-426614174000")
    assert result == mock_entry
    mock_repo.create.assert_called_once_with("test@example.com", "123e4567-e89b-12d3-a456-426614174000", None)

def test_add_email_already_exists(mocker):
    mock_repo = mocker.MagicMock()
    mock_repo.get_by_email.return_value = True
    service = BlacklistService(repo=mock_repo)
    with pytest.raises(ConflictError):
        service.add_email("test@example.com", "123e4567-e89b-12d3-a456-426614174000")

def test_check_email_exists(mocker):
    mock_repo = mocker.MagicMock()
    mock_repo.get_by_email.return_value = True
    service = BlacklistService(repo=mock_repo)
    assert service.check_email("exists@test.com") is True

def test_check_email_not_exists(mocker):
    mock_repo = mocker.MagicMock()
    mock_repo.get_by_email.return_value = None
    service = BlacklistService(repo=mock_repo)
    assert service.check_email("notexists@test.com") is False