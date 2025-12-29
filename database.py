import os
import sqlite3
import psycopg2
import psycopg2.extras
from flask import g

DATABASE = 'habits.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db_url = os.environ.get('DATABASE_URL')
        if db_url:
            # PostgreSQL
            conn = psycopg2.connect(db_url, cursor_factory=psycopg2.extras.RealDictCursor)
            g._db_type = 'postgres'
            db = g._database = conn
        else:
            # SQLite
            conn = sqlite3.connect(DATABASE)
            conn.row_factory = sqlite3.Row
            g._db_type = 'sqlite'
            db = g._database = conn
    return db

def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    db = get_db()
    
    # Adapter for parameter placeholders
    if getattr(g, '_db_type', 'sqlite') == 'postgres':
        query = query.replace('?', '%s')
    
    cur = db.cursor()
    cur.execute(query, args)
    
    if query.strip().upper().startswith('SELECT'):
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
    else:
        db.commit()
        cur.close()
        return None

def init_db(app):
    with app.app_context():
        db = get_db()
        db_type = getattr(g, '_db_type', 'sqlite')
        
        if db_type == 'postgres':
            schema_file = 'schema_pg.sql'
        else:
            schema_file = 'schema.sql'
            
        with app.open_resource(schema_file, mode='r') as f:
            script = f.read()
            if db_type == 'sqlite':
                db.cursor().executescript(script)
            else:
                cur = db.cursor()
                cur.execute(script)
                db.commit()
                cur.close()
