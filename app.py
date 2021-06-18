from flask import Flask, render_template, redirect, url_for, request, session, flash, g, jsonify
import sqlite3, cgi, cgitb, json

app = Flask(__name__)

app.database='farmers.db'

app.secret_key = "opfasidn43rw908c"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/farmers')
def farmers():
    return render_template('farmers.html')

if __name__ == '__main__':
    app.run(debug=True)