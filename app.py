from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
DB_PATH = 'attendance.db'

# Create database if it doesn't exist
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_no TEXT NOT NULL,
                status TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    roll_no = request.form['roll_no']
    status = request.form['status']
    date = datetime.now().strftime('%Y-%m-%d')
    time = datetime.now().strftime('%H:%M:%S')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO attendance (name, roll_no, status, date, time) VALUES (?, ?, ?, ?, ?)",
              (name, roll_no, status, date, time))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)