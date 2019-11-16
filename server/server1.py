from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import socket
import time

SERVER_ADDRESS = (HOST, PORT) = '', 8088
REQUEST_QUEUE_SIZE = 5

####------------------

file_out = open("encrypted_data.bin", "a")

recipient_key = RSA.import_key(open("receiver.pem").read())
session_key = open("aeskey.txt","r").read()



###---------------------

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind(SERVER_ADDRESS)
listen_socket.listen(REQUEST_QUEUE_SIZE)
print('Serving HTTP on port {port} ...'.format(port=PORT))

i=0

while True:
    client_connection, client_address = listen_socket.accept()
    print(i)

    request = client_connection.recv(1024)
    print(request.decode())
    ###### ENCRYPTING
    data = ("I" + str(i)).encode("utf-8")

    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    cipher = ciphertext + "join" + tag + "nonce" + cipher_aes.nonce + "key" + enc_session_key
    #cipher = [ x for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
    file_out.write(cipher)

    http_response = cipher

    client_connection.sendall(http_response)
    #####

    client_connection.close()
    time.sleep(2)
    i=i+1
