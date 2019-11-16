
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import time

import serial
ser = serial.Serial('/dev/ttyACM0', 9600)


#session_key = open("aeskey.txt","r").read()
private_key = RSA.import_key(open("private.pem").read())
#cipher_aes = AES.new(session_key, AES.MODE_EAX)
#nonce = cipher_aes.nonce

while(True):

    data = str(ser.readline())
    print("data recieved")

    ciphertext = data[:(data.find("join"))]
    tag = data[(data.find("join")+4):(data.find("nonce"))]
    nonce = data[(data.find("nonce")+5):(data.find("key"))]
    enc_session_key = data[(data.find("key")+3):]

    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)
    #(enc_session_key, cipher_aes_nonce, tag, ciphertext) = data
    cipher_aes = AES.new(session_key, AES.MODE_EAX,nonce)
    

    # Decrypt the data with the AES session key
    res = cipher_aes.decrypt_and_verify(ciphertext, tag)
    print(res.decode("utf-8"))


    ##--------------------string-matching--------------------------
    #s = "time_stamp=123456789|mod_id=sm_0001|temp=39.7|BPM=100|pos=28.1234,78.1234|btn=0"
    s = res.decode("utf-8")

    module_id= s[(s.find("mod_id")+7):(s.find("temp")-1)]
    temp= s[(s.find("temp")+5):(s.find("BPM")-1)]
    heart_rate= s[(s.find("BPM")+4):(s.find("pos")-1)]
    panic_btn= s[(s.find("btn")+4):]


    if (float(temp)>38.8):
        print("TEMPERATURE CRITICAL for module_id:" + module_id)


    if (int(heart_rate)>150):
        print("HEART-RATE CRITICAL for module_id:" + module_id)


    if (float(panic_btn)==1):
        print("PANIC BUTTON PRESSED on module_id:" + module_id)

    #--------------------------------------------------------------


    file = open("data.txt", "a")
    data = data.encode("base-64")
    file.write(data)
    file.close()
    #time.sleep(0.1)
