from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            rating REAL,
            votes INTEGER
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute("SELECT * FROM movies ORDER BY votes DESC, rating DESC")
    movies = c.fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

@app.route('/rate/<int:movie_id>', methods=['GET', 'POST'])
def rate(movie_id):
    if request.method == 'POST':
        score = float(request.form['score'])

        conn = sqlite3.connect('movies.db')
        c = conn.cursor()

        c.execute("SELECT rating, votes FROM movies WHERE id=?", (movie_id,))
        rating, votes = c.fetchone()

        new_rating = (rating * votes + score) / (votes + 1)
        votes += 1

        c.execute("UPDATE movies SET rating=?, votes=? WHERE id=?",
                  (new_rating, votes, movie_id))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('rate.html', movie_id=movie_id)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']

    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute("INSERT INTO movies (name, rating, votes) VALUES (?, 0, 0)", (name,))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5000)
