import sqlite3

# Create database connection
conn = sqlite3.connect('shilpiconnect.db')
cursor = conn.cursor()

# Create Artisans table
cursor.execute('''
CREATE TABLE IF NOT EXISTS artisans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    skill TEXT NOT NULL,
    location TEXT NOT NULL,
    experience INTEGER,
    phone TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create Learners table
cursor.execute('''
CREATE TABLE IF NOT EXISTS learners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    interest TEXT NOT NULL,
    location TEXT NOT NULL,
    phone TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Add some sample data so you have something to show
cursor.execute('''
INSERT INTO artisans (name, skill, location, experience, phone, description)
VALUES 
('Ravi Kumar', 'Pottery', 'Mysore', 25, '9876543210', 'Traditional pottery maker with 25 years experience'),
('Lakshmi Devi', 'Weaving', 'Bangalore', 30, '9876543211', 'Expert in silk weaving and traditional textiles'),
('Mohan Raj', 'Wood Carving', 'Channapatna', 40, '9876543212', 'Master craftsman in wooden toys and sculptures')
''')

cursor.execute('''
INSERT INTO learners (name, interest, location, phone)
VALUES 
('Priya Sharma', 'Pottery', 'Bangalore', '8765432109'),
('Arjun Kumar', 'Weaving', 'Mysore', '8765432108')
''')

conn.commit()
conn.close()

print("✅ Database created successfully!")
