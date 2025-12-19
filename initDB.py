
from app import app, db
from models import Users
from sqlalchemy import text
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone

# A 3 teszt felhasználó adatai
users_to_seed = [
    #(101, "PappZ", "PappZTitok"),
    (102, "IllesD", "IllesDTitok"),
    #(103, "TesztE", "TesztETitok")
]


def seed_database():
    with app.app_context():
        # 1. ELŐSZÖR létrehozzuk a táblát (vagy ellenőrizzük, hogy létezik-e)
        print("Táblák ellenőrzése és létrehozása az SSMS-ben...")
        #db.create_all()

        # 2. Ellenőrizzük, hogy üres-e a tábla
        try:
            count = db.session.execute(text("SELECT count(*) FROM users")).scalar()
            if count is None:
                count = 0
        except Exception:
            count = 0

        if count > 100:
            print(f"Az adatbázis már tartalmaz {count} felhasználót. Megállunk.")
            return

        print("Felhasználók generálása és mentése...")

        for aid, nick, password in users_to_seed:
            # Új felhasználó objektum
            u = Users()

            # Mezők feltöltése
            u.agentId = aid
            # Mindkét mezőt hash-eljük a kérésed szerint
            u.agentNick = generate_password_hash(nick, method='pbkdf2:sha256')
            u.agentPassword = generate_password_hash(password, method='pbkdf2:sha256')

            # Időbélyegek
            u.created_at = datetime.now(timezone.utc)
            u.updated_at = datetime.now(timezone.utc)

            db.session.add(u)
            print(f" -> '{nick}' (ID: {aid}) előkészítve.")

        # 3. Mentés véglegesítése
        try:
            db.session.commit()
            print("\nSIKER! Az adatok mentve lettek az SSMS-be.")
        except Exception as e:
            db.session.rollback()
            print(f"\nHIBA történt a mentéskor: {e}")


if __name__ == "__main__":
    seed_database()