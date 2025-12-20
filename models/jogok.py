
from models import db

class Jogok(db.Model):
    __tablename__ = 'jogosultsagok'
    __table_args__ = {'schema': 'dbo'}
    id = db.Column(db.Integer, primary_key=True)
    agentId = db.Column(db.Integer, nullable=False)
    func_Persec = db.Column(db.Boolean, nullable=False)
    func_Systems = db.Column(db.Boolean, nullable=False)
    func_Hiring = db.Column(db.Boolean, nullable=False)

def __init__(self, **kwargs):
    super(Jogok, self).__init__(**kwargs)