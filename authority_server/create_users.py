import requests
import json

CLOUD_DOMAIN = "http://cloud.laviem.xyz"

roles = {
    'neurology_doctor': ['neurology_doctor'],
    'dermatology_doctor': ['dermatology_doctor'],
    'otorhinolaryngology_doctor': ['otorhinolaryngology_doctor'],
    'psychiatry_doctor': ['psychiatry_doctor'],
    'rheumatology_doctor': ['rheumatology_doctor'],
    'pharmacist': ['pharmacist'],
    'researcher': ['researcher'],
    'financial': ['financial'],
    'nurse': ['nurse'],
    'patient': ['patient'],
    'doctor': ['doctor']
}

aes = SelfAES()

for username, attributes in roles.items():
    password = "123"
    
    attribute = '{{"ATTR": {}}}'.format(json.dumps(attributes))
    enc_attribute = aes.encrypt(attribute).hex()
    
    data = {
        'username': username,
        'password': Hash.hashing(password),
        'attribute': enc_attribute
    }
    
    response = requests.post(f'{CLOUD_DOMAIN}/api/add_user', data=data)
    
    if response.status_code == 201:
        print(f"✓ Created user: {username} (password: {password})")
    elif response.status_code == 400:
        print(f"✗ User {username} already exists")
    else:
        print(f"✗ Error creating user {username}: {response.text}")

print("\nAll users created successfully!")
print("\nUser credentials:")
print("-" * 50)
for username in roles.keys():
    print(f"Username: {username:<30} Password: 123")
