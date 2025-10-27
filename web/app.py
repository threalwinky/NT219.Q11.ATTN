from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
from urllib.parse import urljoin
import requests
import os
from io import BytesIO
import json
from base64 import b64encode, b64decode
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'client'))
from abe_core import SelfAES, ABE, objectToBytes, bytesToObject

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

TRUSTED_AUTHORITY = "http://127.0.0.1:8000"
CLOUD_DOMAIN = "http://127.0.0.1:5000"
DOWNLOAD_PATH = './downloads/'
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Create a session for each user
def get_session():
    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()
    return requests.Session()

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('menu'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        data = {
            'username': username,
            'password': password
        }
        
        try:
            req_session = get_session()
            response = req_session.post(urljoin(TRUSTED_AUTHORITY, '/login'), data=data)
            
            if response.status_code == 200:
                data = response.json()
                
                session['logged_in'] = True
                session['uid'] = str(data['ID'])
                session['username'] = username
                
                # Initialize keys
                init_keys(data, req_session)
                
                return redirect(url_for('menu'))
            else:
                flash(response.text, 'error')
        except Exception as e:
            flash(f"Login failed: {str(e)}", 'error')
    
    return render_template('login.html')

def init_keys(data, req_session):
    response = req_session.post(urljoin(TRUSTED_AUTHORITY, '/token'), json=data)
    session['token'] = response.text
    
    attribute = data['attribute']
    temp = []
    for attr in attribute:
        if attr == 'ent' or attr.lower() == 'patient':
            temp.append('PATIENT'+str(data['ID']))
        else:
            temp.append(attr)
    session['attribute'] = [attr.upper().replace('_', '') for attr in temp]
    
    response = req_session.post(urljoin(TRUSTED_AUTHORITY, '/get_keys'), json={'attribute': str(session['attribute'])})
    keys = response.json()
    session['dk_key'] = keys['dk_key']
    session['pk_key'] = keys['pk_key']

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/menu')
def menu():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('menu.html', uid=session.get('uid'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        uid = request.form.get('uid')
        patient_name = request.form.get('patient_name')
        collection = request.form.get('collection')
        
        headers = {'Authorization': session['token']}
        data = {
            'uid': uid,
            'patient_name': patient_name,
            'collection_name': collection
        }
        
        try:
            req_session = get_session()
            response = req_session.post(urljoin(CLOUD_DOMAIN, '/api/search_record'), json=data, headers=headers)
            
            if response.status_code == 200:
                results = response.json()
                if len(results) == 0:
                    flash('No records found matching your search criteria.', 'info')
                    return render_template('search.html', results=[])
                return render_template('search.html', results=results)
            else:
                data = response.json()
                flash(data.get('error', 'Search failed'), 'error')
        except Exception as e:
            flash(f"Search failed: {str(e)}", 'error')
    
    return render_template('search.html', results=None)

@app.route('/view', methods=['GET', 'POST'])
def view():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        uid = request.form.get('uid')
        collection = request.form.get('collection')
        
        headers = {'Authorization': session['token']}
        data = {
            'uid': uid,
            'collection_name': collection
        }
        
        try:
            req_session = get_session()
            response = req_session.post(urljoin(CLOUD_DOMAIN, '/api/view_patient_record'), json=data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if not data['patient_data'] or len(data['patient_data']) == 0:
                    flash("There's no data with the provided UID.", 'error')
                    return render_template('view.html')
                
                patient_data = data['patient_data'][0]
                file_id = patient_data.get('file_id')
                
                if not file_id:
                    flash("No file associated with this record", 'error')
                    return render_template('view.html')
                
                download_response = req_session.get(
                    urljoin(CLOUD_DOMAIN, f'/api/download_file/{file_id}'),
                    headers=headers
                )
                
                if download_response.status_code == 200:
                    enc_data = download_response.content
                    plain, msg = decrypt_file(enc_data)
                    
                    if plain:
                        file_name = patient_data['file_name']
                        file_path = os.path.join(DOWNLOAD_PATH, file_name)
                        
                        with open(file_path, 'wb') as file:
                            file.write(plain)
                        
                        flash(f"File downloaded successfully: {file_name}", 'success')
                        return send_file(file_path, as_attachment=True, download_name=file_name)
                    else:
                        flash(msg, 'error')
                else:
                    flash("Failed to download file from server", 'error')
            else:
                data = response.json()
                flash(data.get('error', 'View failed'), 'error')
        except Exception as e:
            flash(f"View failed: {str(e)}", 'error')
    
    return render_template('view.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        uid = request.form.get('uid')
        patient_name = request.form.get('patient_name')
        collection = request.form.get('collection')
        file = request.files.get('file')
        
        if not file:
            flash("Please select a file first!", 'error')
            return render_template('upload.html')
        
        try:
            headers = {'Authorization': session['token']}
            
            UPDATE_POLICIES = {
                'health_record': ['doctor', 'nurse', 'patient'],
                'medicine_record': ['doctor', 'pharmacist', 'patient'],
                'financial_record': ['financial'],
                'research_record': ['doctor', 'researcher'],
            }
            
            POLICY = UPDATE_POLICIES[collection]
            user_attr = [attr.lower() for attr in session['attribute']]
            final_policy = convert_policy(POLICY, user_attr, uid)
            
            file_data = file.read()
            enc_data = encrypt_file_to_bytes(final_policy, file_data)
            
            files = {'encrypted_file': ('encrypted.json', enc_data, 'application/json')}
            form_data = {
                'uid': uid,
                'patient_name': patient_name,
                'file_name': file.filename,
                'collection_name': collection
            }
            
            req_session = get_session()
            response = req_session.post(urljoin(CLOUD_DOMAIN, '/api/upload_patient_record'),
                                      data=form_data, files=files, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                flash(data.get('message', 'Upload successful'), 'success')
            else:
                data = response.json()
                flash(data.get('error', 'Upload failed'), 'error')
        except Exception as e:
            flash(f"Upload failed: {str(e)}", 'error')
    
    return render_template('upload.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        uid = request.form.get('uid')
        patient_name = request.form.get('patient_name')
        collection = request.form.get('collection')
        file = request.files.get('file')
        
        if not file:
            flash("Please select a file first!", 'error')
            return render_template('update.html')
        
        try:
            headers = {'Authorization': session['token']}
            
            # First, check if user can decrypt existing file
            data = {
                'uid': uid,
                'collection_name': collection
            }
            
            req_session = get_session()
            response = req_session.post(urljoin(CLOUD_DOMAIN, '/api/view_patient_record'), json=data, headers=headers)
            
            if response.status_code != 200:
                data = response.json()
                flash(data.get('error', 'Failed to verify permissions'), 'error')
                return render_template('update.html')
            
            data = response.json()
            patient_data = data['patient_data'][0]
            file_id = patient_data.get('file_id')
            
            if not file_id:
                flash("No file associated with this record", 'error')
                return render_template('update.html')
            
            download_response = req_session.get(
                urljoin(CLOUD_DOMAIN, f'/api/download_file/{file_id}'),
                headers=headers
            )
            
            if download_response.status_code == 200:
                enc_data = download_response.content
                plain, msg = decrypt_file(enc_data)
                
                if plain is False:
                    flash("You don't have permission to update the data!", 'error')
                    return render_template('update.html')
                
                # If we can decrypt, proceed with update
                UPDATE_POLICIES = {
                    'health_record': ['doctor', 'nurse', 'patient'],
                    'medicine_record': ['doctor', 'pharmacist', 'patient'],
                    'financial_record': ['financial'],
                    'research_record': ['doctor', 'researcher'],
                }
                
                POLICY = UPDATE_POLICIES[collection]
                user_attr = [attr.lower() for attr in session['attribute']]
                final_policy = convert_policy(POLICY, user_attr, uid)
                
                file_data = file.read()
                enc_data = encrypt_file_to_bytes(final_policy, file_data)
                
                files = {'encrypted_file': ('encrypted.json', enc_data, 'application/json')}
                form_data = {
                    'uid': uid,
                    'patient_name': patient_name,
                    'file_name': file.filename,
                    'collection_name': collection
                }
                
                response = req_session.post(urljoin(CLOUD_DOMAIN, '/api/update_patient_record'),
                                          data=form_data, files=files, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    flash(data.get('message', 'Update successful'), 'success')
                else:
                    data = response.json()
                    flash(data.get('error', 'Update failed'), 'error')
        except Exception as e:
            flash(f"Update failed: {str(e)}", 'error')
    
    return render_template('update.html')

def convert_policy(policy, user_attr, text):
    final_policy = []
    for p in policy:
        tmp = 0
        for p2 in user_attr:
            if p in p2:
                final_policy.append(p2)
                tmp = 1
                continue
        if p == 'patient':
            p = "{}_{}".format(p, text)
        if tmp == 0:
            final_policy.append(p)
    
    final_policy = [p.replace('_', '').lower() for p in list(set(final_policy))]
    final_policy = ' or '.join(final_policy)
    
    return final_policy

def encrypt_file_to_bytes(final_policy, file_data):
    aes = SelfAES()
    abe = ABE()
    
    enc_file_data = aes.encrypt(file_data)
    key = aes.getKey()
    
    ct_dict = abe.encrypt(session['pk_key'].encode(), key, final_policy)
    ct_bytes = objectToBytes(ct_dict['ct'], abe.group)
    enc_key_bytes = ct_dict['enc_key']
    
    encrypted_package = {
        'ct': b64encode(ct_bytes).decode(),
        'enc_key': b64encode(enc_key_bytes).decode(),
        'enc_data': b64encode(enc_file_data).decode()
    }
    
    json_data = json.dumps(encrypted_package)
    return BytesIO(json_data.encode())

def decrypt_file(enc_file_content):
    aes = SelfAES()
    abe = ABE()
    
    try:
        encrypted_package = json.loads(enc_file_content.decode())
        
        ct_bytes = b64decode(encrypted_package['ct'])
        enc_key_bytes = b64decode(encrypted_package['enc_key'])
        enc_data = b64decode(encrypted_package['enc_data'])
        
        ct_obj = bytesToObject(ct_bytes, abe.group)
        ct_dict = {'ct': ct_obj, 'enc_key': enc_key_bytes}
        
        key = abe.decrypt(session['pk_key'].encode(), session['dk_key'].encode(), ct_dict)
        
        if key is None:
            return False, "You don't have permission to access this file. Your attributes don't match the access policy."
        
        plain = aes.decrypt(enc_data, key)
        
        return plain, "SUCCESS"
    except Exception as e:
        print(f"Decryption error: {e}")
        return False, "Failed to decrypt the file. You may not have permission."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
