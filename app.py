import os
from flask import Flask, render_template, request, redirect
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            lng REAL,
            signature TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Handle file upload
    file = request.files.get('signature')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        return "Invalid or missing signature file", 400

    # Save form data + signature filename to DB
    data = (
        request.form['full_name'],
        request.form['student_id'],
        request.form['program'],
        request.form['location'],
        float(request.form['lat']),
        float(request.form['lng']),
        filename
    )
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO submissions 
        (full_name, student_id, program, location, lat, lng, signature) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', data)
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

