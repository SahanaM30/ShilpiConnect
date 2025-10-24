import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Function to connect to database
def get_db():
    conn = sqlite3.connect('shilpiconnect.db')
    conn.row_factory = sqlite3.Row  # This lets us access columns by name
    return conn

# HOME PAGE
@app.route('/')
def home():
    return render_template('home.html')

# VIEW ALL ARTISANS
@app.route('/artisans')
def artisans():
    conn = get_db()
    artisans = conn.execute('SELECT * FROM artisans').fetchall()
    conn.close()
    return render_template('artisans.html', artisans=artisans)

# VIEW ALL LEARNERS
@app.route('/learners')
def learners():
    conn = get_db()
    learners = conn.execute('SELECT * FROM learners').fetchall()
    conn.close()
    return render_template('learners.html', learners=learners)

# REGISTER AS ARTISAN
@app.route('/register-artisan', methods=['GET', 'POST'])
def register_artisan():
    if request.method == 'POST':
        name = request.form['name']
        skill = request.form['skill']
        location = request.form['location']
        experience = request.form['experience']
        phone = request.form['phone']
        description = request.form['description']
        
        conn = get_db()
        conn.execute('''INSERT INTO artisans (name, skill, location, experience, phone, description)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                     (name, skill, location, experience, phone, description))
        conn.commit()
        conn.close()
        
        return redirect(url_for('artisans'))
    
    return render_template('register_artisan.html')

# REGISTER AS LEARNER
@app.route('/register-learner', methods=['GET', 'POST'])
def register_learner():
    if request.method == 'POST':
        name = request.form['name']
        interest = request.form['interest']
        location = request.form['location']
        phone = request.form['phone']
        
        conn = get_db()
        conn.execute('''INSERT INTO learners (name, interest, location, phone)
                        VALUES (?, ?, ?, ?)''',
                     (name, interest, location, phone))
        conn.commit()
        conn.close()
        
        return redirect(url_for('learners'))
    
    return render_template('register_learner.html')

# SEARCH ARTISANS BY SKILL
@app.route('/search')
def search():
    skill = request.args.get('skill', '')
    
    conn = get_db()
    if skill:
        artisans = conn.execute('SELECT * FROM artisans WHERE skill LIKE ?', 
                                ('%' + skill + '%',)).fetchall()
    else:
        artisans = conn.execute('SELECT * FROM artisans').fetchall()
    conn.close()
    
    return render_template('search.html', artisans=artisans, skill=skill)

if __name__ == '__main__':
    app.run(debug=True)
