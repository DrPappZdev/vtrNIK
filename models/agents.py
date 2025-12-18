from datetime import datetime, timezone
from models import db

class Agents(db.Model):
    __tablename__ = 'munkatarsak'
    __table_args__ = {'schema': 'dbo'}
    id = db.Column(db.Integer, primary_key=True)
    valid_e = db.Column(db.Boolean, nullable=False)
    titulus = db.Column(db.String(10), nullable=False)
    nev = db.Column(db.String(50), nullable=False)
    szuletesiNev = db.Column(db.String(50), nullable=False)
    szuletesiHely = db.Column(db.String(50), nullable=False)
    szuletesiIdo = db.Column(db.Date, nullable=False)
    anyjaNeve = db.Column(db.String(50), nullable=False)
    rendfokozat = db.Column(db.Integer, nullable=False)
    beosztas = db.Column(db.Integer, nullable=False)
    szervezetiElem = db.Column(db.Integer, nullable=False)
    memo = db.Column(db.Text, nullable=True)

def __init__(self, **kwargs):
    super(Agents, self).__init__(**kwargs)