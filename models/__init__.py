from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.users import Users
from models.munkatarsak import Munkatarsak
from models.rendfokozat import Rendfokozat
from models.beosztasok import Beosztasok
from models.logging import Logging
from models.jogok import Jogok
from models.aktivmunkatarsak import AktivMunkatarsak
from models.minszintek import MinositesiSzint
from models.szbtnemzeti import NemzetiSzbt
from models.szbtnato import NatoSzbt
from models.szbteu import EuSzbt
from models.szervezetifa import Szervezetifa

def init_db(app):
    db.init_app(app)