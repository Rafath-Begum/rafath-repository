from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"
DATABASE = 'database.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    # Students table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            gender TEXT,
            course TEXT
        )
    """)

    # Users table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------- AUTH ---------------- #

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(
    request.form['password'],
    method='pbkdf2:sha256'
)

        try:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()
            flash("Registration successful! Please login.")
            return redirect(url_for('login'))
        except:
            flash("Username already exists")

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user'] = user['username']
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# --------- LOGIN REQUIRED DECORATOR -------- #

def login_required(route):
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return route(*args, **kwargs)
    wrapper.__name__ = route.__name__
    return wrapper


# ---------------- CRUD ---------------- #

@app.route('/')
@login_required
def index():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template('index.html', students=students)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['email'],
            request.form['gender'],
            request.form['course']
        )

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO students (name, email, gender, course) VALUES (?, ?, ?, ?)",
            data
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_edit.html', student=None)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE id=?", (id,)
    ).fetchone()

    if request.method == 'POST':
        conn.execute("""
            UPDATE students SET name=?, email=?, gender=?, course=?
            WHERE id=?
        """, (
            request.form['name'],
            request.form['email'],
            request.form['gender'],
            request.form['course'],
            id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('add_edit.html', student=student)


@app.route('/delete/<int:id>')
@login_required
def delete_student(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
