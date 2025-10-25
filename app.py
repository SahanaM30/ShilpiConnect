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
        
        # Check if "Other" was selected and use the custom skill
        if skill == 'Other':
            skill = request.form.get('other_skill', 'Other')
        
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
        
        # Check if "Other" was selected and use the custom interest
        if interest == 'Other':
            interest = request.form.get('other_interest', 'Other')
        
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

# SMART MATCHING SYSTEM
@app.route('/matches')
def matches():
    conn = get_db()
    
    # Get all learners and artisans
    learners = conn.execute('SELECT * FROM learners').fetchall()
    artisans = conn.execute('SELECT * FROM artisans').fetchall()
    
    match_results = []
    
    for learner in learners:
        for artisan in artisans:
            # Calculate match score
            score = 0
            
            # Skill match (most important)
            if learner['interest'].lower() == artisan['skill'].lower():
                score += 70
            elif learner['interest'].lower() in artisan['skill'].lower() or artisan['skill'].lower() in learner['interest'].lower():
                score += 40
            
            # Location match
            if learner['location'].lower() == artisan['location'].lower():
                score += 30
            elif learner['location'].lower() in artisan['location'].lower() or artisan['location'].lower() in learner['location'].lower():
                score += 15
            
            # Only show matches above 50%
            if score >= 50:
                match_results.append({
                    'learner_name': learner['name'],
                    'interest': learner['interest'],
                    'learner_location': learner['location'],
                    'artisan_name': artisan['name'],
                    'skill': artisan['skill'],
                    'experience': artisan['experience'],
                    'artisan_location': artisan['location'],
                    'phone': artisan['phone'],
                    'match_score': score
                })
    
    # Sort by match score (highest first)
    match_results.sort(key=lambda x: x['match_score'], reverse=True)
    
    conn.close()
    return render_template('matches.html', matches=match_results)

# STATISTICS PAGE
@app.route('/stats')
def stats():
    conn = get_db()
    
    # Get total counts
    total_artisans = conn.execute('SELECT COUNT(*) as count FROM artisans').fetchone()['count']
    total_learners = conn.execute('SELECT COUNT(*) as count FROM learners').fetchone()['count']
    
    # Get popular skills
    popular_skills = conn.execute('''
        SELECT skill, COUNT(*) as count 
        FROM artisans 
        GROUP BY skill 
        ORDER BY count DESC
    ''').fetchall()
    
    # Get average experience
    avg_exp = conn.execute('SELECT AVG(experience) as avg FROM artisans').fetchone()['avg']
    total_exp = conn.execute('SELECT SUM(experience) as total FROM artisans').fetchone()['total']
    
    conn.close()
    
    return render_template('stats.html',
                         total_artisans=total_artisans,
                         total_learners=total_learners,
                         total_matches=min(total_artisans, total_learners),  # Simple calculation
                         popular_skills=popular_skills,
                         avg_experience=round(avg_exp, 1) if avg_exp else 0,
                         total_experience=total_exp if total_exp else 0)



if __name__ == '__main__':
    app.run(debug=True)
