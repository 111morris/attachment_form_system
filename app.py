from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, render_template, send_from_directory, flash

import sqlite3

app = Flask(__name__)

def insert_submission(data): 
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            student_id TEXT,
            program TEXT,
            location TEXT,
            lat REAL,
            lng REAL
        )
    ''')
    conn.commit()
    conn.close() 

def get_all_submissions():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM submissions')
    entries = c.fetchall()
    conn.close()
    return entries


def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            student_id TEXT,
            program TEXT,
            location TEXT,
            lat REAL,
            lng REAL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = (
            request.form['full_name'],
            request.form['student_id'],
            request.form['program'],
            request.form['location'],
            float(request.form['lat']),
            float(request.form['lng'])
        )
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO submissions (full_name, student_id, program, location, lat, lng)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        conn.close()
    return redirect('/')


@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM submissions')
    entries = c.fetchall()
    conn.close()
    return render_template('admin.html', entries=entries)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

