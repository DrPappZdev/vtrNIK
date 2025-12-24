from models import db

class Szervezetifa(db.Model):
    __tablename__ = 'szervezetiFa'
    __table_args__ = {'schema': 'dbo'}
    id = db.Column(db.Integer, primary_key=True)
    kod_Foig = db.Column(db.Integer)
    kod_FoigHely = db.Column(db.Integer)
    kod_Ig = db.Column(db.Integer)
    kod_Fo = db.Column(db.Integer)
    kod_O = db.Column(db.Integer)

def __init__(self, **kwargs):
    super(Szervezetifa, self).__init__(**kwargs)