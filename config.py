import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.getenv('SECRET_KEY')

    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_SERVER = os.getenv('DB_SERVER')
    DB_NAME = os.getenv('DB_NAME')

    APP_ORG = os.getenv('APP_ORG')
    APP_SHORTORG = os.getenv('APP_SHORTORG')
    APP_SHORTNAME = os.getenv('APP_SHORTNAME')
    APP_LONGNAME = os.getenv('APP_LONGNAME')
    APP_LOGO = os.getenv('APP_LOGO')
    APP_LOGOSIZE = int(os.getenv('APP_LOGOSIZE', 30))
    APP_VER = os.getenv('APP_VER')

    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
