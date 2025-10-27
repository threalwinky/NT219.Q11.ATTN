from flask import Blueprint, request, jsonify
import sqlite3
import os

user_api = Blueprint('user_api', __name__)

DB_PATH = './opt/users.db'

def DBConnect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hash_password TEXT NOT NULL,
            attribute TEXT NOT NULL
        )
    ''')
    
    cursor.execute("SELECT * FROM users WHERE username = ?", ('admin',))
    admin_user = cursor.fetchone()
    if admin_user is None:
        cursor.execute('''
            INSERT INTO users (username, hash_password, attribute)
            VALUES (?, ?, ?)
        ''', ('admin', 'b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86', '{"ATTR": ["administrator"]}'))
        conn.commit()
    
    return conn

db_conn = DBConnect()

@user_api.route('/api/get_user_info', methods=['POST'])
def queryUser():
    if request.method == 'POST':
        username = request.form.get('username')
        
        cursor = db_conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()

        if user_data:
            server_response = {
                'user_id': user_data['user_id'],
                'username': user_data['username'],
                'hash_password': user_data['hash_password'],
                'attribute': user_data['attribute']
            }

            return jsonify(server_response), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    return "Method Not Allowed", 405

@user_api.route('/api/add_user', methods=['POST'])
def addUser():
    if request.method == 'POST':
        username = request.form.get('username')
        hash_password = request.form.get('password')
        attribute = request.form.get('attribute')

        cursor = db_conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_exists = cursor.fetchone()

        if user_exists:
            return jsonify({'error': 'User already exists'}), 400
        else:
            cursor.execute('''
                INSERT INTO users (username, hash_password, attribute)
                VALUES (?, ?, ?)
            ''', (username, hash_password, attribute))
            db_conn.commit()

            return jsonify({'status': 'success'}), 201
    
    return "Method Not Allowed", 405

@user_api.route('/api/change_password', methods=['POST'])
def changePassword():
    if request.method == 'POST':
        username = request.form.get('username')
        hash_password = request.form.get('new_passwd')

        cursor = db_conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_exists = cursor.fetchone()

        if user_exists:
            cursor.execute("UPDATE users SET hash_password = ? WHERE username = ?", (hash_password, username))
            db_conn.commit()
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    
    return "Method Not Allowed", 405