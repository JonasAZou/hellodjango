from Crypto.Cipher import DES, AES
from Crypto import Random
from base64 import encodestring as b64encode, decodestring as b64decode

key = b'Sixteen byte key'
tp = b'attack at dawnxx'
iv = Random.new().read(AES.block_size)
print b64encode(iv+tp)
cipher = AES.new(key, AES.MODE_CBC, iv)
cipher2 = AES.new(key, AES.MODE_CBC, iv)
msg = cipher.encrypt(tp)
print cipher2.decrypt(msg)


