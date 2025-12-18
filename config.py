import urllib
from flask_sqlalchemy import SQLAlchemy

DB_CONFIG = {
    'server': 'localhost,1433',
    'database': 'vtrHBF',
    'username': 'pappz',
    'password': 'PappZ2024',
    'driver': 'ODBC Driver 17 for SQL Server'
}

params = urllib.parse.quote_plus(
    f"DRIVER={DB_CONFIG['driver']};"
    f"SERVER={DB_CONFIG['server']};"
    f"DATABASE={DB_CONFIG['database']};"
    f"UID={DB_CONFIG['username']};"
    f"PWD={DB_CONFIG['password']}"
)

SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"