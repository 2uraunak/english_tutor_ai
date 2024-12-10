import sqlite3
import json
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.db_path = 'english_tutor.db'
        self.init_db()
        
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Create tables if they don't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user_input TEXT,
                assistant_response TEXT,
                analysis TEXT,
                improvement_score REAL
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def store_interaction(self, user_input, response, analysis):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Calculate simple improvement score based on number of errors
        improvement_score = 10 - min(len(analysis), 10)  # 0-10 scale
        
        c.execute('''
            INSERT INTO interactions 
            (timestamp, user_input, assistant_response, analysis, improvement_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            user_input,
            response,
            json.dumps(analysis),
            improvement_score
        ))
        
        conn.commit()
        conn.close()
        
    def get_progress_report(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Get average improvement score over time
        c.execute('''
            SELECT 
                date(timestamp),
                AVG(improvement_score) as avg_score,
                COUNT(*) as interaction_count
            FROM interactions 
            GROUP BY date(timestamp)
            ORDER BY date(timestamp) DESC
            LIMIT 30
        ''')
        
        progress_data = [
            {
                'date': row[0],
                'average_score': row[1],
                'interactions': row[2]
            }
            for row in c.fetchall()
        ]
        
        conn.close()
        return progress_data
