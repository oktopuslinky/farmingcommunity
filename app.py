from flask import Flask, render_template, redirect, url_for, request, session, flash, g, jsonify
import sqlite3, cgi, cgitb, json

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
    return render_template('farmers.html')

@app.route('/testing')
def testing():
    g.db = connect_db()
    cur = g.db.execute("SELECT * FROM farmers_list")
    print(cur.fetchall())
    return render_template('testing.html')

if __name__ == '__main__':
    app.run(debug=True)