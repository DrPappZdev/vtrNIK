
from models import db

class Jogok(db.Model):
    __tablename__ = 'jogosultsagok'
    __table_args__ = {'schema': 'dbo'}
    id = db.Column(db.Integer, primary_key=True)
    agentId = db.Column(db.Integer, nullable=False)
    is_Admin = db.Column(db.Boolean, nullable=False, default=False)
    func_Persec = db.Column(db.Boolean, nullable=False, default=False)
    func_Systems = db.Column(db.Boolean, nullable=False, default=False)
    func_Hiring = db.Column(db.Boolean, nullable=False, default=False)
    func_UserHandling = db.Column(db.Boolean, nullable=False, default=False)
    func_QueryCreator = db.Column(db.Boolean, nullable=False, default=False)
    func_AppSettings = db.Column(db.Boolean, nullable=False, default=False)
    func_Logging = db.Column(db.Boolean, nullable=False, default=False)


def __init__(self, **kwargs):
    super(Jogok, self).__init__(**kwargs)