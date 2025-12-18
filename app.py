# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from models import db, Users, init_db
from config import SQLALCHEMY_DATABASE_URI
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '@H4Z4DN4K_r3ndul3tl3nul_L3GYHiV3_0h_M4GY4R!_sir0d_L3SZ_3z!'

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
#    flash('A rendszer üzenetküldése aktív!', 'info')
    if request.method == 'POST':
        data = request.form.get('credentials')
        if not data or '+' not in data:
            return "Hibás formátum!", 400

        input_nick, input_pass = data.split('+', 1)
        users = db.session.query(Users).all()

        for user in users:
            if check_password_hash(user.agentNick, input_nick):
                if check_password_hash(user.agentPassword, input_pass):
                    session['user_id'] = user.id
                    return f"Siker! Üdv, {input_nick}"

        return "Hibás adatok!", 401

    return render_template('main.html')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # Minden adatot törlünk a munkamenetből
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