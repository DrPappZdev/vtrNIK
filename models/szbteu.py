from models import db

class EuSzbt(db.Model):
    __tablename__ = 'szbtEU'
    __table_args__ = {'schema': 'dbo'}
    id = db.Column(db.Integer, primary_key=True)
    agentId = db.Column(db.Integer)
    szbtEuMinSzint = db.Column(db.Integer)
    szbtEuIktsz = db.Column(db.String(50), nullable=False)
    szbtEuIktsz_NBF = db.Column(db.String(50), nullable=False)
    szbtEuLejaratiDatum = db.Column(db.Date, nullable=False)
    szbtEuVisszavonIktsz = db.Column(db.String(50), nullable=True)
    szbtEuVisszavonDatum = db.Column(db.Date, nullable=True)
    szbtEuFajlNev = db.Column(db.String(50), nullable=True)
    szbtEuFajlTartalom = db.Column(db.LargeBinary, nullable=True)

def __init__(self, **kwargs):
    super(EuSzbt, self).__init__(**kwargs)