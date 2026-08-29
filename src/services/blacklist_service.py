from src.repositories.blacklist_repository import BlacklistRepository
from src.models.errors import ConflictError

class BlacklistService:
    def __init__(self, repo=None):
        self.repo = repo or BlacklistRepository()

    def add_email(self, email, app_uuid, reason=None):
        if self.repo.get_by_email(email):
            raise ConflictError(f"Email {email} already in blacklist")
        return self.repo.create(email, app_uuid, reason)

    def check_email(self, email):
        return self.repo.get_by_email(email) is not None