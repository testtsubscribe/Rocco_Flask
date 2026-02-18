import sqlite3
from werkzeug.security import generate_password_hash
import sys

def create_admin(username, password):
    conn = sqlite3.connect('website.db')
    cursor = conn.cursor()
    
    hashed_password = generate_password_hash(password)
    
    try:
        cursor.execute('INSERT INTO admins (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        print(f"Admin '{username}' created successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: Admin '{username}' already exists.")
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        create_admin(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python3 create_admin.py <username> <password>")
        # Default creation for initial setup if run without args
        create_admin('admin', 'admin123')
