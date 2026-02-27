import sqlite3
import json
import os

class FaceDatabase:
    def __init__(self, db_path='data/facelock.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                embedding TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def add_user(self, username, embedding):
        """Stocke l'embedding sous forme de chaîne JSON."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        embedding_json = json.dumps(embedding.tolist() if hasattr(embedding, 'tolist') else embedding)
        try:
            cursor.execute('INSERT INTO users (username, embedding) VALUES (?, ?)', (username, embedding_json))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_all_users(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT username, embedding FROM users')
        rows = cursor.fetchall()
        conn.close()
        
        users = []
        for row in rows:
            users.append({
                'username': row[0],
                'embedding': json.loads(row[1])
            })
        return users

    def delete_user(self, username):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.commit()
        conn.close()
