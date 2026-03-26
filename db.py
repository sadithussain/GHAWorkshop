import json
import os

DB_PATH = 'sample_db.json'

db = {
    'rooms': [],
    'devices': []
}

def load_db():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, 'r') as f:
            try:
                data = json.load(f)
                db.update(data)
            except:
                print('Failed to open file')

def save_db():
    with open(DB_PATH, 'w') as f:
        json.dump(db, f, indent=4)