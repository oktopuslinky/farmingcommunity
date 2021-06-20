from flask import Flask, render_template, redirect, url_for, request, session, flash, g, jsonify
from functools import wraps
import sqlite3, cgi, cgitb, json, os
from werkzeug.utils import secure_filename

'''
TODO:
- handle logins
- give needs data
'''

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        g.db = connect_db()
        cur = g.db.execute('SELECT * FROM logins')
        data = cur.fetchall()

        reg_farmer_id=data[-1][0]

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print("filename:", file.filename)
        mimetype=file.mimetype
        mimetype = mimetype.replace('image/', '')
        print("mime:", mimetype)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return render_template('upload_file.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(str(reg_farmer_id)+'.'+str(mimetype))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            g.db.execute(
                '''
                UPDATE farmers_list
                SET picture = ?
                WHERE farmer_id = ?;
                ''', [filename, reg_farmer_id]
            )
            g.db.commit()

            return redirect(url_for('login'))
    else:
        print('method was get.')

    return render_template('upload_file.html')

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

@app.route('/deleteneed', methods=['GET', 'POST'])
@login_required
def deleteneed():
    g.db = connect_db()
    cur = g.db.execute(
        '''
        SELECT * FROM needs
        WHERE farmer_id=?
        ''', [session['id']]
    )
    data = cur.fetchall()
    print("current needs:", data)
    if request.method == 'POST':
        g.db.execute(
            '''
            DELETE FROM needs
            WHERE need_id=?
            ''', [request.form['get_id']]
        )
        g.db.commit()
        return redirect(url_for('dashboard'))

    return render_template('deleteneed.html', user_needs=data)

@app.route('/myneeds')
@login_required
def myneeds():
    g.db = connect_db()
    cur = g.db.execute(
        '''
        SELECT * FROM needs
        WHERE farmer_id=?
        ''', [session['id']]
    )
    data = cur.fetchall()
    return render_template('myneeds.html', my_needs=data)

@app.route('/createneed', methods=['GET', 'POST'])
@login_required
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
    if 'logged_in' in session:
        flash("You are already logged in. You will now be redirected to the dashboard.")
        return redirect(url_for('dashboard'))
    else:
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
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM farmers_list WHERE farmer_id=?',[session['id']])
    data = cur.fetchall()
    print(data)
    return render_template('dashboard.html', data=data)

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
                    request.form['chemicals']
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

            return redirect(url_for('upload_file'))

    return render_template('register.html')



#ignore all of this, it is just testing.
@app.route('/testing', methods=['GET', 'POST'])
def testing():
    if request.method == 'POST':
        print('hihi')
        print(request.files['file'])  
    return render_template('testing.html')
###


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)