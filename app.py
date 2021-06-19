from flask import Flask, render_template, redirect, url_for, request, session, flash, g, jsonify
from functools import wraps
import sqlite3, cgi, cgitb, json, os

'''
TODO:
- handle logins
- give needs data
'''

app = Flask(__name__)

app.database='farmers.db'

app.secret_key = "opfasidn43rw908c"


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

def connect_db():
    return sqlite3.connect(app.database)

@app.route('/')
def home():

    #NOTE: THE ID OF THE FARMER IS WORKING

    print("farmer id:", session.get('id', None))
    return render_template('index.html')

@app.route('/farmers')
def farmers():
    g.db = connect_db()
    cur = g.db.execute("SELECT * FROM farmers_list")
    data = cur.fetchall()
    print(data)
    return render_template('farmers.html', farmers=data)

@app.route('/needs')
def needs():
    g.db = connect_db()
    cur = g.db.execute("SELECT * FROM needs")
    data = cur.fetchall()
    print(data)
    return render_template('needs.html', needs=data)

@app.route('/createneed', methods=['GET', 'POST'])
def createneed():
    if request.method == 'POST':
        g.db = connect_db()
        cur = g.db.execute("SELECT * FROM needs")
        data = cur.fetchall()
        print(data)
        g.db.execute(
            '''
            INSERT INTO needs(need_text, farmer_id)
            VALUES(?,?)
            ''', [request.form['need_text'], session['id']]
        )
        g.db.commit()
        print(request.form['need_text'], session['id'])
        return redirect(url_for('dashboard'))
    
    return render_template('createneed.html')


#for flask to domain connection
# https://towardsdatascience.com/how-to-deploy-your-website-to-a-custom-domain-8cb23063c1ff

#while this works, you should do this:
# https://flask-login.readthedocs.io/en/latest/
# https://medium.com/analytics-vidhya/how-to-use-flask-login-with-sqlite3-9891b3248324



#need to make "welcome, {{name}}"
@app.route('/login', methods=['GET', 'POST'])
def login():
    error=None
    if request.method == 'POST':
        g.db = connect_db()
        cur = g.db.execute('SELECT * FROM logins')
        data = cur.fetchall()
        print(data)
        login_valid = False
        farmer_id = None

        for farmer in data:
            if farmer[1] == request.form['email'] and farmer[2] == request.form['password']:
                login_valid = True
                farmer_id = farmer[0]
                print(farmer_id)

        if login_valid is False:
            #if login incorrect
            error = 'Your email or password is incorrect. Please try again.'
        else:
            #if login correct
            session['id'] = farmer_id
            session['logged_in'] = True
            return redirect(url_for('dashboard'))

    return render_template('login.html', error=error)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        g.db = connect_db()
        cur = g.db.execute('SELECT * FROM logins')
        data = cur.fetchall()
        print(data)
        user_exists = False
        for farmer in data:
            if farmer[1] == request.form['email'] and farmer[2] == request.form['password']:
                user_exists = True
                farmer_id = farmer[0]
                print(farmer_id)
        
        if user_exists:
            flash('This user already exists in the system. Try logging in.')
            return redirect(url_for('login'))

        else:
            print("received data")
            print("age", request.form['age'])
            g.db.execute(
                '''
                INSERT INTO farmers_list(
                    first_name,
                    last_name,
                    age,
                    email,
                    phone_number,
                    plants,
                    seeds,
                    tools,
                    chemicals
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', [
                    request.form['first_name'],
                    request.form['last_name'],
                    request.form['age'],
                    request.form['email'],
                    request.form['phone_number'],
                    request.form['plants'],
                    request.form['seeds'],
                    request.form['tools'],
                    request.form['chemicals'],
                ]
            )
            g.db.execute(
                '''
                INSERT INTO logins(email, password) VALUES(?, ?)
                ''', [request.form['email'], request.form['password']]
            )

            g.db.commit()

            the_cur = g.db.execute('SELECT * FROM logins')
            the_data = the_cur.fetchall()
            print(the_data)

            return redirect(url_for('login'))

    return render_template('register.html')



#ignore all of this, it is just testing.
@app.route('/testing')
def testing():
    return render_template('testing.html')
###


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
