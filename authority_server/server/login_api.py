from processing import SelfAES, Hash
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from urllib.parse import urljoin
import requests, json

CLOUD_DOMAIN = "https://cloud9116.duckdns.org"

login_api = Blueprint('login_api', __name__, template_folder='template')

@login_api.route('/')
def home():
    return redirect('/login')

@login_api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        response = requests.post(urljoin(CLOUD_DOMAIN, '/api/get_user_info'), data={'username': username})
        
        if response.status_code == 200:
            user_info = response.json()

            if user_info['hash_password'] == Hash.hashing(password):
                session['ID'] = user_info['user_id']
                session['username'] = username
                if session['username'] != 'admin':
                    attribute = bytes.fromhex(user_info['attribute'])
                    aes = SelfAES()
                    attribute = json.loads(aes.decrypt(attribute).decode())
                else:
                    attribute = json.loads(user_info['attribute'])
                    
                session['attribute'] = attribute['ATTR']
                
                if session['attribute'] == ['administrator']:
                    return redirect('/register')
                else:
                    return jsonify({'ID':user_info['user_id'], 'attribute': attribute['ATTR']}), 200
            else:
                return 'Invalid password', 400
        else:
            return 'Invalid username', 400

    return render_template('login.html')

@login_api.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' not in session:
        return redirect('/login')
    if ('admin' not in session['username']) or ('administrator' not in session['attribute']):
        return redirect('/login')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        attribute = request.form['attribute']

        aes = SelfAES()
        attribute = '{{"ATTR": {}}}'.format(json.dumps([attr.strip() for attr in attribute.split(',')]))
        enc_attribute = aes.encrypt(attribute).hex()

        data = {
            'username': username,
            'password': Hash.hashing(password),
            'attribute': enc_attribute
        }
        
        response = requests.post(urljoin(CLOUD_DOMAIN, '/api/add_user'), data=data)

        if response.status_code == 200:
            return "Success", 200
        elif response.status_code == 400 and response.json().get('error') == 'User already exists':
            return render_template('register.html', error='Username already exists')

    return render_template('register.html')

@login_api.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    
    return redirect('/login')