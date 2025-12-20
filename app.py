# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from models import db, Users, Agents, Rendfokozat, Beosztasok
from models import init_db
#from config import SQLALCHEMY_DATABASE_URI
from werkzeug.security import check_password_hash
from config import Config
from utility import log_event

app = Flask(__name__)

app.config.from_object(Config)

init_db(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('A kért oldal eléréséhez be kell jelentkezned!')
            # Itt adjuk hozzá a 'next' paramétert!
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/logincheck', methods=['GET', 'POST'])
def logincheck():
    if request.method == 'POST':
        data = request.form.get('credentials')

        if not data or '+' not in data:
            log_event(
                userid=0,
                event_type="LOGIN_ERROR",
                description=f"Sikertelen belépési kísérlet!",
                table_name="user",
                record_id=0
            )
            flash("Hibás adatküldés!", "danger")
            return redirect(url_for('login'))

        try:
            input_nick, input_pass = data.split('+', 1)
        except ValueError:
            flash("Hibás adatformátum!", "danger")
            return redirect(url_for('login'))

        users = db.session.query(Users).all()
        for user in users:
            if check_password_hash(user.agentNick, input_nick):
                if check_password_hash(user.agentPassword, input_pass):

                    # 1. Ügynök keresése (mivel mondtad, hogy az agentId helyett id van)
                    agent_data = db.session.query(Agents).filter_by(id=user.agentId).first()

                    if agent_data and agent_data.valid_e:

                        # 2. rang és beosztás kibányászása
                        rank_data = db.session.query(Rendfokozat).filter_by(id=agent_data.rendfokozat).first()
                        beo = db.session.query(Beosztasok).filter_by(id=agent_data.beosztas).first()

                        # Biztonsági ellenőrzés, ha véletlenül nincs meg a kód a táblában
                        rank_name = rank_data.rendfokozat if rank_data else "Ismeretlen"
                        print("agentData ", agent_data.beosztas, input_pass, "  ", input_nick, " ", rank_name , " ", beo.beosztas)

                        session['user_id'] = user.agentId
                        session['user_titulus'] = agent_data.titulus
                        session['user_neve'] = agent_data.nev
                        session['user_rendfokozat'] = rank_name
                        session['user_beosztas'] = beo.beosztas
                        userNeve = session.get('user_neve', '')
                        log_event(
                            userid=user.agentId,
                            event_type="LOGIN",
                            description=f"Belépés: {userNeve}",
                            table_name="user",
                            record_id=0
                        )

                        return redirect(url_for('main'))
        log_event(
            userid=0,
            event_type="LOGIN_ERROR",
            description=f"Sikertelen belépési kísérlet!",
            table_name="user",
            record_id=0
        )
        flash("Hibás adatok!", "danger")
        return redirect(url_for('login'))
    return render_template('main.html')

@app.route('/main')
@login_required
def main():
    log_event(
        userid=session.get('user_id', '0'),
        event_type="PAGE_LOAD",
        description=f"Main_site betöltése",
        table_name="user",
        record_id=0
    )
    return render_template('main.html')

@app.route('/persec')
@login_required
def persec():
    log_event(
        userid=session.get('user_id', '0'),
        event_type="PAGE_LOAD",
        description=f"PerSec_site betöltése",
        table_name="munkatarsak",
        record_id=0
    )
    return render_template('szemelyibiztonsag.html')


@app.route('/')
def login():
    ev_type = "PAGE_LOAD"
    event_desc = "Login_site betöltése"
    next_page = request.args.get('next')
    if next_page:
        ev_type = 'PAGE_LOAD_UNAUTHORIZED_ACCESS'
        event_desc = f"Illetéktelen belépési kísérlet a(z) {next_page} oldalra"
    log_event(
        userid=session.get('user_id', 0),
        event_type=ev_type,
        description=event_desc,
        table_name="user",
        record_id=0
    )
    return render_template('login.html')

@app.route('/logout')
def logout():
    log_event(
        userid=session.get('user_id', ''),
        event_type="LOGOUT",
        description=f"Kijelentkezés: {session.get('user_neve', '')}",
        table_name="user",
        record_id=0
    )
    session.clear()
    response = redirect(url_for('login'))
    response.set_cookie('session', '', expires=0)
    #flash('Sikeresen kijelentkeztél.')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    context = {
        'nick': session.get('agent_nick'),
        'title': 'Vezérlőpult'
    }
    return render_template('dashboard.html', **context)

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == '__main__':
    app.run(debug=True)