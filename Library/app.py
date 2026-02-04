from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "library_secret"
DATABASE = "database.db"


# ---------------- DATABASE ---------------- #

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        available INTEGER
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS borrowed (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        book_id INTEGER
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
        role = request.form['role']

        try:
            conn = get_db()
            conn.execute(
                "INSERT INTO users (username, password, role) VALUES (?,?,?)",
                (username, password, role)
            )
            conn.commit()
            conn.close()
            flash("Registration successful")
            return redirect(url_for('login'))
        except:
            flash("Username already exists")

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user'] = user['username']
            session['user_id'] = user['id']
            session['role'] = user['role'] if 'role' in user.keys() else None
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------------- DECORATORS ---------------- #

def login_required(route):
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return route(*args, **kwargs)
    wrapper.__name__ = route.__name__
    return wrapper


def publisher_only(route):
    def wrapper(*args, **kwargs):
        if session.get('role') != 'publisher':
            flash("Access denied")
            return redirect(url_for('dashboard'))
        return route(*args, **kwargs)
    wrapper.__name__ = route.__name__
    return wrapper


# ---------------- DASHBOARD ---------------- #

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return render_template('dashboard.html', books=books)


# ---------------- PUBLISHER ---------------- #

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
@publisher_only
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        conn = get_db()
        conn.execute(
            "INSERT INTO books (title, author, available) VALUES (?,?,1)",
            (title, author)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

    return render_template('add_book.html')


# ---------------- READER ---------------- #

@app.route('/borrow/<int:book_id>')
@login_required
def borrow(book_id):
    conn = get_db()

    conn.execute(
        "INSERT INTO borrowed (user_id, book_id) VALUES (?,?)",
        (session['user_id'], book_id)
    )
    conn.execute(
        "UPDATE books SET available=0 WHERE id=?",
        (book_id,)
    )

    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))


@app.route('/return/<int:book_id>')
@login_required
def return_book(book_id):
    conn = get_db()

    conn.execute(
        "DELETE FROM borrowed WHERE user_id=? AND book_id=?",
        (session['user_id'], book_id)
    )
    conn.execute(
        "UPDATE books SET available=1 WHERE id=?",
        (book_id,)
    )

    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))


# ---------------- START ---------------- #

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
