from flask import Blueprint, request, jsonify, send_file
from abac import checker
from authorize import check_token
import sqlite3
import os
from ast import literal_eval
import uuid

patient_api = Blueprint('patient_api', __name__)

DB_PATH = './opt/hospital.db'
UPLOAD_FOLDER = './uploads'

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def DBConnect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS health_record")
    cursor.execute("DROP TABLE IF EXISTS medicine_record")
    cursor.execute("DROP TABLE IF EXISTS financial_record")
    cursor.execute("DROP TABLE IF EXISTS research_record")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_record (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT NOT NULL,
            patient_name TEXT NOT NULL,
            file_name TEXT,
            file_id TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicine_record (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT NOT NULL,
            patient_name TEXT NOT NULL,
            file_name TEXT,
            file_id TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS financial_record (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT NOT NULL,
            patient_name TEXT NOT NULL,
            file_name TEXT,
            file_id TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS research_record (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT NOT NULL,
            patient_name TEXT NOT NULL,
            file_name TEXT,
            file_id TEXT
        )
    ''')
    
    conn.commit()
    return conn

db = DBConnect()

VIEW_POLICIES = {
    'health_record': ['doctor', 'nurse', 'patient'],
    'medicine_record': ['doctor', 'pharmacist', 'patient'],
    'financial_record': ['financial'],
    'research_record': ['doctor', 'researcher'],
}

UPDATE_POLICIES = {
    'health_record': ['doctor', 'nurse'],
    'medicine_record': ['doctor', 'pharmacist'],
    'financial_record': ['financial'],
    'research_record': ['doctor', 'researcher'],
}

@patient_api.route("/api/search_record", methods=["POST"])
@check_token
def searchRecord(user):
    data = request.json

    uid = data.get("uid", "")
    collection_name = data.get("collection_name", "")
    patient_name = data.get("patient_name", "")

    user_attr = literal_eval(user['attribute'])
    if collection_name in UPDATE_POLICIES:
        POLICY = UPDATE_POLICIES[collection_name]
        if not checker(user_attr, POLICY):
            return jsonify({"error": "You don't have permission to view this"}), 404
    else:
        return jsonify({"error": "Invalid collection name"}), 400
      
    cursor = db.cursor()
    query = f"SELECT patient_name, uid FROM {collection_name} WHERE 1=1"
    params = []
    
    if uid != "":
        query += " AND uid = ?"
        params.append(uid)
    if patient_name != "":
        query += " AND patient_name LIKE ?"
        params.append(f"%{patient_name}%")
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    
    result_list = [dict(row) for row in results]
    
    return jsonify(result_list), 200


@patient_api.route('/api/view_patient_record', methods=['POST'])
@check_token
def viewRecord(user):
    data = request.json

    collection_name = data.get('collection_name', '')
    uid = data.get('uid', '')

    user_attr = literal_eval(user['attribute'])
    if collection_name in VIEW_POLICIES:
        POLICY = VIEW_POLICIES[collection_name]
        if not checker(user_attr, POLICY):
            return jsonify({"error": "You don't have permission to view this"}), 404
    else:
        return jsonify({"error": "Invalid collection name"}), 400
    
    cursor = db.cursor()
    query = f"SELECT * FROM {collection_name} WHERE 1=1"
    params = []
    
    if uid != "":
        query += " AND uid = ?"
        params.append(uid)
    
    cursor.execute(query, params)
    patient_records = cursor.fetchall()
    
    if not patient_records:
        return jsonify({"error": "Patient record not found"}), 404

    patient_data = [dict(row) for row in patient_records]
    return jsonify({"message": "Record retrieved successfully", "patient_data": patient_data}), 200


@patient_api.route('/api/upload_patient_record', methods=['POST'])
@check_token
def uploadPatient(user):
    try:
        collection_name = request.form.get('collection_name')
        uid = request.form.get('uid')
        patient_name = request.form.get('patient_name')
        file_name = request.form.get('file_name')
        encrypted_file = request.files.get('encrypted_file')
        
        if not all([collection_name, uid, patient_name, file_name, encrypted_file]):
            return jsonify({"error": "Missing required fields"}), 400

        user_attr = literal_eval(user['attribute'])
        if collection_name in UPDATE_POLICIES:
            POLICY = UPDATE_POLICIES[collection_name]
            if not checker(user_attr, POLICY):
                return jsonify({"error": "You don't have permission to upload this"}), 403
        else:
            return jsonify({"error": "Invalid collection name"}), 400

        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {collection_name} WHERE uid = ?", (uid,))
        existing_record = cursor.fetchone()
        
        if existing_record is None:
            file_id = str(uuid.uuid4())
            file_path = os.path.join(UPLOAD_FOLDER, file_id)
            encrypted_file.save(file_path)
            
            cursor.execute(f'''
                INSERT INTO {collection_name} (uid, patient_name, file_name, file_id)
                VALUES (?, ?, ?, ?)
            ''', (uid, patient_name, file_name, file_id))
            db.commit()
            return jsonify({"message": "Record uploaded successfully", "inserted_id": uid}), 200
        else:
            return jsonify({"error": "Record with the provided UID already exists"}), 409
    except Exception as e:
        print(f"Upload error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@patient_api.route('/api/update_patient_record', methods=['POST'])
@check_token
def updateRecord(user):
    try:
        collection_name = request.form.get('collection_name')
        uid = request.form.get('uid')
        patient_name = request.form.get('patient_name')
        file_name = request.form.get('file_name')
        encrypted_file = request.files.get('encrypted_file')
        
        if not all([collection_name, uid, patient_name, file_name, encrypted_file]):
            return jsonify({"error": "Missing required fields"}), 400

        user_attr = literal_eval(user['attribute'])
        if collection_name in UPDATE_POLICIES:
            POLICY = UPDATE_POLICIES[collection_name]
            if not checker(user_attr, POLICY):
                return jsonify({"error": "You don't have permission to update this"}), 403
        else:
            return jsonify({"error": "Invalid collection name"}), 400

        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {collection_name} WHERE uid = ?", (uid,))
        existing_record = cursor.fetchone()
        
        if not existing_record:
            return jsonify({"error": "Patient record not found"}), 404
        
        if existing_record['file_id']:
            old_file_path = os.path.join(UPLOAD_FOLDER, existing_record['file_id'])
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_FOLDER, file_id)
        encrypted_file.save(file_path)
        
        cursor.execute(f'''
            UPDATE {collection_name}
            SET patient_name = ?, file_name = ?, file_id = ?
            WHERE uid = ?
        ''', (patient_name, file_name, file_id, uid))
        db.commit()

        return jsonify({"message": "Record updated successfully"}), 200
    except Exception as e:
        print(f"Update error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@patient_api.route('/api/download_file/<file_id>', methods=['GET'])
@check_token
def downloadFile(user, file_id):
    file_path = os.path.join(UPLOAD_FOLDER, file_id)
    
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    return send_file(file_path, as_attachment=True)