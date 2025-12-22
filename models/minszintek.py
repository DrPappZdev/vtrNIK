from models import db

class MinositesiSzint(db.Model):
    __tablename__ = 'minSzintek'
    __table_args__ = {'schema': 'dbo'}
    id = db.Column(db.Integer, primary_key=True)
    minSzint = db.Column(db.String(50), nullable=False)
    valid_e = db.Column(db.Boolean, nullable=False)

def __init__(self, **kwargs):
    super(MinositesiSzint, self).__init__(**kwargs)