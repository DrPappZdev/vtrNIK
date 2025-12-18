# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from models import db, Users, Agents, Rendfokozat, Beosztasok
from models import init_db
#from config import SQLALCHEMY_DATABASE_URI
from werkzeug.security import check_password_hash
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

init_db(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('A kért oldal eléréséhez be kell jelentkezned!')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/logincheck', methods=['GET', 'POST'])
def logincheck():
    if request.method == 'POST':
        data = request.form.get('credentials')
        input_nick, input_pass = data.split('+', 1)
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

                        # 3. SESSION feltöltése minden jóval
                        session['user_id'] = user.agentId
                        session['user_titulus'] = agent_data.titulus
                        session['user_neve'] = agent_data.nev
                        session['user_rendfokozat'] = rank_name
                        session['user_beosztas'] = beo.beosztas
                        #session['agent_rank_id'] = agent_data.rendfokozat  # A kód is meglehet

                        #flash(f"Üdvözlöm, {rank_name} {agent_data.nev}!", "success")
                        return redirect(url_for('main'))

        flash("Hibás adatok!", "danger")
        return redirect(url_for('login'))
    return render_template('main.html')

@app.route('/main')
@login_required
def main():
    return render_template('main.html')

@app.route('/persec')
@login_required
def persec():
    return render_template('szemelyibiztonsag.html')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
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

if __name__ == '__main__':
    app.run(debug=True)