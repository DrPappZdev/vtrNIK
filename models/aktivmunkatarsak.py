from models import db

class AktivMunkatarsak(db.Model):
    __tablename__ = 'aktiv_munkatarsak'
    id = db.Column(db.Integer, primary_key=True)
    nev = db.Column(db.String)
    titulus = db.Column(db.String)
    rendfokozat = db.Column(db.String)
    beosztas = db.Column(db.String)
    Nemzeti_Minosites = db.Column(db.String)
    NATO_Minosites = db.Column(db.String)
    EU_Minosites = db.Column(db.String)
    Ervenyesseg = db.Column(db.Date)

    def __repr__(self):
        return f'<AktivMunkatarsak {self.nev}>'