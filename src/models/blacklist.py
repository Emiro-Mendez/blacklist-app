from src.db.database import db
import uuid

class Blacklist(db.Model):
    __tablename__ = 'blacklists'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    app_uuid = db.Column(db.String(36), nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "app_uuid": self.app_uuid,
            "reason": self.reason,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }