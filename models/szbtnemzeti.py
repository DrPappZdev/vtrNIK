from models import db

class NemzetiSzbt(db.Model):
    __tablename__ = 'szbtNemzeti'
    __table_args__ = {'schema': 'dbo'}
    id = db.Column(db.Integer, primary_key=True)
    agentId = db.Column(db.Integer)
    szbtNemMinSzint = db.Column(db.Integer)
    szbtNemIktsz = db.Column(db.String(50), nullable=False)
    szbtNemLejaratiDatum = db.Column(db.Date, nullable=False)
    szbtNemVisszavonIktsz = db.Column(db.String(50), nullable=True)
    szbtNemVisszavonDatum = db.Column(db.Date, nullable=True)
    szbtNemFajlNev = db.Column(db.String(50), nullable=True)
    szbtNemFajlTartalom = db.Column(db.LargeBinary, nullable=True)

def __init__(self, **kwargs):
    super(NemzetiSzbt, self).__init__(**kwargs)