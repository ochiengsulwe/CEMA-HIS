import uuid

from datetime import datetime, timezone

from api.v1 import db


class TokenBlocklist(db.Model):
    """Stores revocked tokens"""
    id = db.Column(db.String(60), primary_key=True, index=True,
                   default=lambda: str(uuid.uuid4()))
    jti = db.Column(db.String(36), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<TokenBlocklist {self.jti}>"
