from models import db

class Rendfokozat(db.Model):
    __tablename__ = 'rendfokozatok'
    __table_args__ = {'schema': 'dbo'}
    id = db.Column(db.Integer, primary_key=True)
    rendfokozat = db.Column(db.String(50), nullable=False)
    aktiv_e = db.Column(db.Boolean, nullable=False)

def __init__(self, **kwargs):
    super(Rendfokozat, self).__init__(**kwargs)