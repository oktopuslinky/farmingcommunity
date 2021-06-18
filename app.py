from flask import Flask, render_template, redirect, url_for, request, session, flash, g, jsonify
import sqlite3, cgi, cgitb, json


'''
TODO:
- handle logins
- give needs data
'''

app = Flask(__name__)

app.database='farmers.db'

app.secret_key = "opfasidn43rw908c"
def connect_db():
    return sqlite3.connect(app.database)

@app.route('/')
def home():
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

#ignore all of this, it is just testing.
@app.route('/testing')
def testing():
    return render_template('testing.html')
###

if __name__ == '__main__':
    app.run(debug=True)