from src.db.database import db
from src.models.blacklist import Blacklist

class BlacklistRepository:
    def create(self, email, app_uuid, reason=None):
        entry = Blacklist(email=email, app_uuid=app_uuid, reason=reason)
        db.session.add(entry)
        db.session.commit()
        return entry

    def get_by_email(self, email):
        return Blacklist.query.filter_by(email=email).first()