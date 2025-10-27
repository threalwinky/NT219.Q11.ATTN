from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.core.engine.util import objectToBytes, bytesToObject
from Crypto.Cipher import AES
from Crypto.Util.Padding import *
from hashlib import sha256
import os

class SelfAES:
    def __init__(self):
        self.key = os.urandom(32)

    def encrypt(self, data):
        if type(data) != type(b''):
            data = data.encode()
        
        Cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = Cipher.encrypt_and_digest(data)
        
        return Cipher.nonce + ciphertext + tag
    
    def decrypt(self, data, key):
        Cipher = AES.new(key, AES.MODE_GCM, data[:16])
        
        return Cipher.decrypt_and_verify(data[16:-16], data[-16:])

    def getKey(self):
        return self.key

class ABE:
    def __init__(self):
        self.group = PairingGroup('SS512')
        self.cpabe = CPabe_BSW07(self.group)
        self.sign = b'DEADBEEF'

    def encrypt(self, pk, key, policy):
        self.pk = bytesToObject(pk, self.group)
        rand_gt = self.group.random(GT)
        ct = self.cpabe.encrypt(self.pk, rand_gt, policy)
        
        key_seed = objectToBytes(rand_gt, self.group)
        derived_key = sha256(key_seed).digest()
        
        cipher = AES.new(derived_key, AES.MODE_GCM)
        enc_key, tag = cipher.encrypt_and_digest(key)
        
        return {'ct': ct, 'enc_key': cipher.nonce + enc_key + tag}
    
    def decrypt(self, pk, dk, ct_dict):
        self.pk = bytesToObject(pk, self.group)
        self.dk = bytesToObject(dk, self.group)
        
        try:
            rand_gt = self.cpabe.decrypt(self.pk, self.dk, ct_dict['ct'])
            
            # Check if decryption failed (returns False when attributes don't match policy)
            if rand_gt == False or rand_gt is False:
                return None
            
            key_seed = objectToBytes(rand_gt, self.group)
            derived_key = sha256(key_seed).digest()
            
            enc_key_data = ct_dict['enc_key']
            cipher = AES.new(derived_key, AES.MODE_GCM, enc_key_data[:16])
            key = cipher.decrypt_and_verify(enc_key_data[16:-16], enc_key_data[-16:])
            
            return key
        except Exception as e:
            print(f"ABE decrypt exception: {e}")
            return None