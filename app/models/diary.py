from app import db
from datetime import datetime

class Diary(db.Model):
    diary_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry = db.Column(db.String, nullable=False) 
    posted_at = db.Column(db.DateTime, nullable=False) # default=datetime.now
    reflex_id = db.Column(db.Integer, db.ForeignKey('reflex.reflex_id')) #double check this
    reflex = db.relationship("Reflex", back_populates="diaries") #lazy=True