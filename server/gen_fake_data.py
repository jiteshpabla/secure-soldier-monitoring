from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

fake_data = "THHISSSS IS  ORIGINAL DATA!!!!!!!!!!!!!!! (WINK! WINK!)".encode("utf-8")

file_out = open("encrypted_data_fake.bin", "wb")

fake_session_key = open("fakeaeskey.txt","r").read()

# Encrypt the data with the AES session key
cipher_aes = AES.new(fake_session_key, AES.MODE_EAX)
ciphertext, tag = cipher_aes.encrypt_and_digest(fake_data)

cipher = ciphertext + "join" + tag + "nonce" + cipher_aes.nonce
file_out.write(cipher)



nonce = cipher_aes.nonce

cipher1 = AES.new(fake_session_key, AES.MODE_EAX, nonce)
data = cipher1.decrypt_and_verify(ciphertext, tag)

print(data)
