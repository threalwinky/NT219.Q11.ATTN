from processing import ABE, SelfAES
from charm.core.engine.util import objectToBytes
from charm.toolbox.pairinggroup import PairingGroup
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os

os.makedirs('./opt', exist_ok=True)

pairing_group = PairingGroup("SS512")
abe = ABE()
pk, mk = abe.setupKey()

aes = SelfAES()
with open('./opt/pk_key', 'wb') as f:
    f.write(aes.encrypt(objectToBytes(pk, pairing_group)))
with open('./opt/mk_key', 'wb') as f:
    f.write(aes.encrypt(objectToBytes(mk, pairing_group)))
    
private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
public_key = private_key.public_key()

private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open('./opt/jwtkey_priv.pem.enc', 'wb') as f:
    f.write(aes.encrypt(private_key_pem))
with open('./opt/jwtkey_pub.pem', 'wb') as f:
    f.write(public_key_pem)

print("Keys generated successfully!")