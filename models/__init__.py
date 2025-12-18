from flask_sqlalchemy import SQLAlchemy

# 1. Itt jön létre az egyetlen, közös db objektum
db = SQLAlchemy()

# 2. Itt regisztráljuk a modellt a db-hez
from models.users import Users

def init_db(app):
    """Ezt hívjuk meg az app.py-ban"""
    db.init_app(app)