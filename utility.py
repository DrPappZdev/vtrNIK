# utility.py
from flask import request
from models import db, Logging  # Importáljuk az adatbázist és a modellt

def log_event(userid, event_type, description, table_name=None, record_id=None):
    """
    Rendszeresemények naplózása az adatbázisba.
    """
    try:
        # Gép azonosítója (IP cím)
        machine_id = request.remote_addr if request else "System"

        new_log = Logging(
            userid=userid,
            machineId=machine_id[:20],
            tableName=table_name[:20] if table_name else None,
            recordId=record_id,
            eventType=event_type[:50],
            eventDescription=description[:500]
        )

        db.session.add(new_log)
        db.session.commit()

        print(f"Log mentve: {event_type} - {description}")

    except Exception as e:
        db.session.rollback()
        print(f"HIBA a naplózás során: {e}")


def format_date(date):
    """Példa egy másik hasznos segédfüggvényre: dátum formázása"""
    if date:
        return date.strftime('%Y. %m. %d. %H:%M')
    return ""