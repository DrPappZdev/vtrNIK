from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.users import Users
from models.agents import Agents
from models.rendfokozat import Rendfokozat
from models.beosztasok import Beosztasok
from models.logging import Logging
from models.jogok import Jogok
from models.AktivMunkatarsak import AktivMunkatarsak

def init_db(app):
    db.init_app(app)