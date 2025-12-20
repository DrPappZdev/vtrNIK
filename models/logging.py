from models import db

class Logging(db.Model):
    __tablename__ = 'logging'
    __table_args__ = {'schema': 'dbo'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, nullable=False)
    machineId = db.Column(db.String(20))
    tableName = db.Column(db.String(20))
    recordId = db.Column(db.Integer)
    eventType = db.Column(db.String(50))
    eventDescription = db.Column(db.String(500))
    # Az eventTime-ot az SQL Server automatikusan kezeli a DEFAULT GETDATE() miatt

    def __init__(self, **kwargs):
        super(Logging, self).__init__(**kwargs)