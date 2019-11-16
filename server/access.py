from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import sys



#------------------ accessing real data------------------

file = open("encrypted_data.bin", "rb")
aeskey = open("aeskey.txt","r")
data = file.read()
session_key = aeskey.read()
ciphertext = data[:(data.find("join"))]
tag = data[(data.find("join")+4):(data.find("nonce"))]
nonce = data[(data.find("nonce")+5):(data.find("key"))]
cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
res = cipher_aes.decrypt_and_verify(ciphertext, tag)
print(res.decode("utf-8"))
file.close()

#------------------accessing fake data ----------------

file1 = open("encrypted_data_fake.bin", "rb")
faeskey = open("fakeaeskey.txt",'r')
data1 = file1.read()
fake_session_key = faeskey.read()
ciphertext1 = data1[:(data1.find("join"))]
tag1 = data1[(data1.find("join")+4):(data1.find("nonce"))]
nonce1 = data1[(data1.find("nonce")+5):]
cipher_aes1 = AES.new(fake_session_key, AES.MODE_EAX, nonce1)
res1 = cipher_aes1.decrypt_and_verify(ciphertext1, tag1)
print(res1.decode("utf-8"))