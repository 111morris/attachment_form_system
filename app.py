from flask import Flask, render_template, request, redirect
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
    conn.close
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
def submit():
    data = (
        request.form['full_name'],
        request.form['student_id'],
        request.form['program'],
        request.form['location'],
        request.form['lat'],
        request.form['lng']
    )
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO submissions (full_name, student_id, program, location, lat, lng) VALUES (?, ?, ?, ?, ?, ?)', data)
    conn.commit()
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

