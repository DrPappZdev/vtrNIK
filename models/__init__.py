from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.users import Users
from models.agents import Agents
from models.rendfokozat import Rendfokozat
from models.beosztasok import Beosztasok
from models.logging import Logging

def init_db(app):
    db.init_app(app)