from config import Config
from datetime import datetime, timezone

class Conversation(Config.getdb().Model):
    __tablename__ = 'conversations'
    id = Config.getdb().Column(Config.getdb().Integer, primary_key=True)
    user_id = Config.getdb().Column(Config.getdb().Integer, Config.getdb().ForeignKey('users.id'), nullable=False)
    message = Config.getdb().Column(Config.getdb().Text, nullable=False)
    response = Config.getdb().Column(Config.getdb().Text, nullable=False)
    timestamp = Config.getdb().Column(Config.getdb().DateTime, nullable=False, default=datetime.now(timezone.utc))

    user = Config.getdb().relationship('User',backref=Config.getdb().backref('conversations', lazy=True))
    