"""
Flashcard Database Models using SQLAlchemy
Supports multi-user flashcard system with status tracking
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Tab(db.Model):
    """Danh mục nhóm thẻ (ví dụ: Khải 1, Khải 2, ...)"""
    __tablename__ = 'tabs'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    cards = db.relationship('Card', backref='tab', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cards': [card.to_dict() for card in self.cards],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Card(db.Model):
    """Thẻ flashcard với 3 mặt: tiêu đề, trích đoạn, giải nghĩa"""
    __tablename__ = 'cards'
    
    id = db.Column(db.String(50), primary_key=True)
    tab_id = db.Column(db.String(50), db.ForeignKey('tabs.id'), nullable=False)
    ref = db.Column(db.String(50), nullable=False)  # ví dụ: "Khải 1:1"
    title = db.Column(db.Text, nullable=False)  # Mặt 1: Tiêu đề
    verse = db.Column(db.Text, default='')  # Mặt 2: Trích đoạn (HTML)
    analysis = db.Column(db.Text, default='')  # Mặt 3: Giải nghĩa (HTML)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    statuses = db.relationship('CardStatus', backref='card', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_statuses=True):
        data = {
            'id': self.id,
            'tab_id': self.tab_id,
            'ref': self.ref,
            'title': self.title,
            'verse': self.verse,
            'analysis': self.analysis,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if include_statuses:
            data['statuses'] = {status.user_id: status.status for status in self.statuses}
        return data


class CardStatus(db.Model):
    """Trạng thái học thuộc của người dùng cho mỗi thẻ"""
    __tablename__ = 'card_statuses'
    
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.String(50), db.ForeignKey('cards.id'), nullable=False)
    user_id = db.Column(db.String(100), nullable=False)  # Username
    status = db.Column(db.String(1), default='')  # '' (default), 'g' (passed), 'r' (review), 'h' (hard)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint: một user chỉ có một status cho mỗi card
    __table_args__ = (db.UniqueConstraint('card_id', 'user_id', name='uq_card_user'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'card_id': self.card_id,
            'user_id': self.user_id,
            'status': self.status,
            'updated_at': self.updated_at.isoformat()
        }


def init_db(app):
    """Initialize database with app context"""
    with app.app_context():
        db.create_all()
