from models import db

class NatoSzbt(db.Model):
    __tablename__ = 'szbtNATO'
    __table_args__ = {'schema': 'dbo'}
    id = db.Column(db.Integer, primary_key=True)
    agentId = db.Column(db.Integer)
    szbtNatoMinSzint = db.Column(db.Integer)
    szbtNatoIktsz = db.Column(db.String(50), nullable=False)
    szbtNatoIktsz_NBF = db.Column(db.String(50), nullable=False)
    szbtNatoLejaratiDatum = db.Column(db.Date, nullable=False)
    szbtNatoVisszavonIktsz = db.Column(db.String(50), nullable=True)
    szbtNatoVisszavonDatum = db.Column(db.Date, nullable=True)
    szbtNatoFajlNev = db.Column(db.String(50), nullable=True)
    szbtNatoFajlTartalom = db.Column(db.LargeBinary, nullable=True)

def __init__(self, **kwargs):
    super(NatoSzbt, self).__init__(**kwargs)