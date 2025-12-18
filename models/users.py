from datetime import datetime, timezone
from models import db

class Users(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'dbo'}
    id = db.Column(db.Integer, primary_key=True)
    agentId = db.Column(db.Integer, nullable=False)
    agentNick = db.Column(db.String(255), nullable=False)
    agentPassword = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    disabled_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)