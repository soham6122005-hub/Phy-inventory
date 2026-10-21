import sqlite3
from flask import Flask, render_template, request, flash
app = Flask(__name__)
app.secret_key = "linkkiwi2026"
# 2 functions to connect to the database and create the table if it doesn't exist

def connect_db():
    conn = sqlite3.connect('myproject.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    
    conn = connect_db()

    conn.execute('''
         CREATE TABLE IF NOT EXISTS Students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll INTEGER NOT NULL,
            mark INTEGER NOT NULL,
            subject TEXT NOT NULL,
            attendance INTEGER DEFAULT 0   
        )
    ''')
    conn.commit()
    conn.close()
 
if __name__ == "__main__":
    init_db()       
    app.run(debug=True)