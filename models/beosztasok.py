from models import db

class Beosztasok(db.Model):
    __tablename__ = 'beosztasok'
    __table_args__ = {'schema': 'dbo'}
    id = db.Column(db.Integer, primary_key=True)
    beosztas = db.Column(db.String(50), nullable=False)
    aktiv_e = db.Column(db.Boolean, nullable=False)

def __init__(self, **kwargs):
    super(Beosztasok, self).__init__(**kwargs)