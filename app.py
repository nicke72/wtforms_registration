#!bin/python
from flask import Flask, request, render_template, redirect, url_for
from model import RegForm, loginForm
from flask_bootstrap import Bootstrap
import sqlite3 as sql
from datetime import date, timedelta
import flask_login

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')
Bootstrap(app)

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# Our mock database. Do not use in production!
users = {'foo@bar.tld': {'password': 'secret'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form['email']   #Change int model and login.html to user_id
        if request.form['password'] == users[email]['password']: # Change
            user = User()
            user.id = email #change
            flask_login.login_user(user)
            return redirect(url_for('registration'))

    return render_template('login.html', form=form)


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))
    #return 'Unauthorized'


@app.route('/', methods=['GET', 'POST'])
@app.route('/registration', methods=['GET', 'POST'])
@flask_login.login_required
def registration():
    form = RegForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            mac_address = request.form.get('mac_address')
            date_expired = request.form.get('date_expired')
            email = request.form.get('email')
            user_id = 'test'

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO macs (mac_address,date_expired,email,user_id) VALUES (?,?,?,?)",(mac_address,date_expired,email,user_id) )
                con.commit()
                msg = "Record successfully added"

        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            con.close() 
            return render_template('registration_complete.html',mac_address = mac_address, date_expired = date_expired, email = email, user_id = user_id, msg = msg )
            
    return render_template('registration_custom.html', form=form)

@app.route('/list')
@flask_login.login_required
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
   
    cur = con.cursor()
    cur.execute("select * from macs where user_id = 'ergkl'")
    rows = cur.fetchall() 
    print(len(rows))
    if len(rows) > 0: 
        return render_template('list.html',rows = rows)
    else:
        return render_template('no_entry_list.html')

if __name__ == '__main__':
    app.run(debug=True)
