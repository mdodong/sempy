import bcrypt
from Crypto.Cipher import AES

__all__ = ["encrypt", "decrypt", "KDF_ROUNDS"]

KDF_ROUNDS = 1<<12

def encrypt(password, salt, iv, raw_data):
    key = bcrypt.kdf(password, salt, 24, KDF_ROUNDS)    
    length = 16 - (len(raw_data) % 16)
    raw_data += bytes([length]) * length
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    enc_data = cipher.encrypt(raw_data)
    
    return enc_data


def decrypt(password, salt, iv, enc_data):
    key = bcrypt.kdf(password, salt, 24, KDF_ROUNDS)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    raw_pad = cipher.decrypt(enc_data)
    
    raw = raw_pad[0:-raw_pad[-1]]
    
    return raw


