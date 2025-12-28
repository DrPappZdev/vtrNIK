# app.py
from pydoc import text

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from models import db, Users, Munkatarsak, Rendfokozat, Beosztasok, Jogok, AktivMunkatarsak
from models import MinositesiSzint, NemzetiSzbt, NatoSzbt, EuSzbt, Szervezetifa
from models import init_db
from werkzeug.security import check_password_hash
from config import Config
from utility import log_event
from datetime import date
from sqlalchemy import or_

app = Flask(__name__)

app.config.from_object(Config)

init_db(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('A kért oldal eléréséhez be kell jelentkezned!')
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(function_column):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                return redirect(url_for('login'))
            user_perms = session.get('user_permissions', {})
            if not user_perms.get(function_column, False):
                log_event(
                    userid=user_id,
                    event_type="PAGE_LOAD_UNAUTHORIZED_ACCESS",
                    description=f"Illetéktelen belépési kísérlet a(z) {function_column} oldalra",
                    table_name = "user",
                    record_id = 0
                )
                flash("Nincs jogosultsága a kért művelethez!", "danger")
                return redirect(url_for('main'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/get_person_details/<int:person_id>')
@login_required
def get_person_details(person_id):
    try:
        # 1. Alapadatok és a kapcsolódó szöveges megnevezések lekérése JOIN-okkal
        # Egyszerre kérjük le a rendfokozatot és a beosztást is
        result = db.session.query(
            Munkatarsak,
            Rendfokozat,
            Beosztasok
        ).join(Rendfokozat, Munkatarsak.rendfokozat == Rendfokozat.id) \
            .join(Beosztasok, Munkatarsak.beosztas == Beosztasok.id) \
            .filter(Munkatarsak.id == person_id).first()

        if not result:
            return {"error": "Személy nem található"}, 404

        person, rf_obj, beo_obj = result

        # 2. Nemzeti SzBT adatok lekérése (mint az előbb)
        szbt_data = db.session.query(NemzetiSzbt, MinositesiSzint) \
            .join(MinositesiSzint, NemzetiSzbt.szbtNemMinSzint == MinositesiSzint.id) \
            .filter(NemzetiSzbt.agentId == person_id).first()

        nemzeti_szint_szoveg = None
        nemzeti_lejarat = "---"
        if szbt_data:
            szbt, m_szint = szbt_data
            nemzeti_szint_szoveg = m_szint.minSzint
            nemzeti_lejarat = szbt.szbtNemLejaratiDatum.strftime('%Y.%m.%d.') if szbt.szbtNemLejaratiDatum else "---"

        # 3. Szervezeti egység (marad a régi logikád)
        szervezeti_szoveg = "Nincs megadva"
        if person.szervezetiElem:
            szf = Szervezetifa.query.get(person.szervezetiElem)
            if szf:
                szervezeti_szoveg = f"Főig: {szf.kod_Foig} / Ig: {szf.kod_Ig} / Oszt: {szf.kod_O}"

        nemzeti_lejarat_iso = szbt.szbtNemLejaratiDatum.isoformat() if szbt.szbtNemLejaratiDatum else None
        # 4. JSON válasz: ID-k a szerkesztéshez, SZÖVEGEK a dashboardhoz
        return {
            "titulus": person.titulus or "",
            "nev": person.nev or "",
            "valid_e": person.valid_e,
            "szuletesiNev": person.szuletesiNev or "",
            "szuletesiHely": person.szuletesiHely or "",
            "szuletesiIdo": person.szuletesiIdo.strftime('%Y-%m-%d') if person.szuletesiIdo else "",
            "anyjaNeve": person.anyjaNeve or "",
            "rendfokozat_id": person.rendfokozat,  # ID a select-hez
            "rendfokozat_nev": rf_obj.rendfokozat,  # Szöveg a dash-hez
            "beosztas_id": person.beosztas,  # ID a select-hez
            "beosztas_nev": beo_obj.beosztas,  # Szöveg a dash-hez
            "szervezetiElem": str(person.szervezetiElem or ""),
            "szervezeti_szoveg": szervezeti_szoveg,
            "memo": person.memo or "",
            "nemzeti_szint": nemzeti_szint_szoveg,
            "nemzeti_ervenyesseg": nemzeti_lejarat,
            "nemzeti_szint": nemzeti_szint_szoveg,
            "nemzeti_ervenyesseg": nemzeti_lejarat,
            "nemzeti_lejarat_iso": nemzeti_lejarat_iso
        }

    except Exception as e:
        print(f"Szerver hiba: {e}")
        return {"error": str(e)}, 500

@app.route('/persec/add_person', methods=['POST'])
@permission_required('func_Persec')
@login_required
def add_person():
    try:
        # Dátum konvertálása HTML-ből  (YYYY-MM-DD) Python date-re
        szul_datum_str = request.form.get('szuletesiIdo')
        szul_datum = datetime.strptime(szul_datum_str, '%Y-%m-%d').date() if szul_datum_str else None

        uj_munkatars = Munkatarsak(
            valid_e=True,
            titulus=request.form.get('titulus'),
            nev=request.form.get('nev'),
            szuletesiNev=request.form.get('szuletesiNev'),
            szuletesiHely=request.form.get('szuletesiHely'),
            szuletesiIdo=szul_datum,
            anyjaNeve=request.form.get('anyjaNeve'),
            rendfokozat=int(request.form.get('rendfokozat')),
            beosztas=int(request.form.get('beosztas')),
            memo=request.form.get('memo'),
            szervezetiElem=None
        )

        db.session.add(uj_munkatars)
        db.session.commit()

        flash(f"{uj_munkatars.nev} sikeresen rögzítve!", "success")

    except Exception as e:
        db.session.rollback()
        print(f"DEBUG HIBA: {str(e)}")
        flash(f"Hiba történt a mentés során: {str(e)}", "danger")

    return redirect(url_for('persec'))

@app.route('/resultNameSearch')
@permission_required('func_Persec')
@login_required
def result_name_search():

    query_string = request.args.get('query', '').strip()
    status = request.args.get('status', 'all')
    strict = request.args.get('strict', 'true') == 'true'

    # Nyelvérzékenység kapcsolása
    if strict:
        search_filter = or_(
            Munkatarsak.nev.ilike(f'%{query_string}%'),
            Munkatarsak.szuletesiNev.ilike(f'%{query_string}%')
        )
    else:
        search_filter = or_(
            Munkatarsak.nev.collate('Latin1_General_CI_AI').ilike(f'%{query_string}%'),
            Munkatarsak.szuletesiNev.collate('Latin1_General_CI_AI').ilike(f'%{query_string}%')
        )
    stmt = Munkatarsak.query.filter(search_filter)

    if status == "active":
        stmt = stmt.filter(Munkatarsak.valid_e == 1)
    elif status == "inactive":
        stmt = stmt.filter(Munkatarsak.valid_e == 0)

    munkatarsak_lista = stmt.all()
    m_ids = [m.id for m in munkatarsak_lista]

    # 2. Nemzeti SZBT adatok lekérése a megtalált munkatársakhoz
    # Csak azokat kérjük le, amik nincsenek visszavonva (nincs visszavonó dátum)
    nemzeti_adatok = NemzetiSzbt.query.filter(
        NemzetiSzbt.agentId.in_(m_ids),
        NemzetiSzbt.szbtNemVisszavonDatum == None
    ).all()

    # Szótár építése: { munkatars_id: minosites_szint_id }
    nemzeti_map = {n.agentId: n.szbtNemMinSzint for n in nemzeti_adatok}

    # --- NATO ADATOK ---
    nato_adatok = NatoSzbt.query.filter(NatoSzbt.agentId.in_(m_ids), NatoSzbt.szbtNatoVisszavonDatum == None).all()
    nato_map = {n.agentId: n.szbtNatoMinSzint for n in nato_adatok}

    # --- EU ADATOK ---
    eu_adatok = EuSzbt.query.filter(EuSzbt.agentId.in_(m_ids), EuSzbt.szbtEuVisszavonDatum == None).all()
    eu_map = {e.agentId: e.szbtEuMinSzint for e in eu_adatok}


    # Érvényességi dátumok térképe (a táblázat utolsó oszlopához)
    lejarati_map = {n.agentId: n.szbtNemLejaratiDatum for n in nemzeti_adatok}

    # 3. Segédszótárak (Rendfokozat, Beosztás, Szintek)
    ranks = {r.id: r.rendfokozat for r in Rendfokozat.query.all()}
    positions = {b.id: b.beosztas for b in Beosztasok.query.all()}
    secretLevel = {str(l.id): l.minSzint for l in MinositesiSzint.query.all()}

    today = datetime.now().date()
    limit_date = today + timedelta(days=30)

    return render_template('nevkeresesEredmenye.html',
                           munkatarsak=munkatarsak_lista,
                           query_string=query_string,
                           status=status,
                           ranks=ranks,
                           positions=positions,
                           minszint=secretLevel,
                           nemzeti_map=nemzeti_map,
                           nato_map=nato_map,  # ÚJ
                           eu_map=eu_map,
                           lejarati_map=lejarati_map,  # ÚJ!
                           today=today,
                           limit_date=limit_date)

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

                    #  kolléga kikeresése
                    agent_data = db.session.query(Munkatarsak).filter_by(id=user.agentId).first()

                    if agent_data and agent_data.valid_e:

                        # rendfokozat és a beosztás kibányászása
                        rank_data = db.session.query(Rendfokozat).filter_by(id=agent_data.rendfokozat).first()
                        beo = db.session.query(Beosztasok).filter_by(id=agent_data.beosztas).first()

                        # ha nem lenne meg
                        rank_name = rank_data.rendfokozat if rank_data else "Ismeretlen"

                        session['user_id'] = user.agentId
                        session['user_titulus'] = agent_data.titulus
                        session['user_neve'] = agent_data.nev
                        session['user_rendfokozat'] = rank_name
                        session['user_beosztas'] = beo.beosztas
                        userNeve = session.get('user_neve', '')
                        user_jogok = Jogok.query.filter_by(agentId=user.agentId).first()
                        if user_jogok:
                            permissions = {
                                'is_Admin': user_jogok.is_Admin,
                                'func_Persec': user_jogok.func_Persec,
                                'func_Systems': user_jogok.func_Systems,
                                'func_Hiring': user_jogok.func_Hiring,
                                'func_UserHandling': user_jogok.func_UserHandling,
                                'func_QueryCreator': user_jogok.func_QueryCreator,
                                'func_AppSettings': user_jogok.func_AppSettings,
                                'func_Logging': user_jogok.func_Logging
                            }
                            session['user_permissions'] = permissions
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
        flash(f"Hibás bejelentkezés!", "danger")

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

from datetime import date, datetime, timedelta  # Ne felejtsd el az importot a fájl elején!

@app.route('/persec')
@permission_required('func_Persec')
@login_required
def persec():
    today = datetime.now().date()
    limit_date = today + timedelta(days=30)
    munkatarsak_adatai = AktivMunkatarsak.query.order_by(AktivMunkatarsak.nev.asc()).all()

    rendfokozatok = Rendfokozat.query.order_by(Rendfokozat.rendfokozat).all()
    beosztasok = Beosztasok.query.order_by(Beosztasok.beosztas).all()

    log_event(
        userid=session.get('user_id', '0'),
        event_type="PAGE_LOAD",
        description=f"PerSec_site betöltése",
        table_name="munkatarsak",
        record_id=0
    )

    return render_template(
        'szemelyibiztonsag.html',
        munkatarsak=munkatarsak_adatai,
        rendfokozatok=rendfokozatok,
        beosztasok=beosztasok,
        today=date.today(),
        limit_date=limit_date
    )

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