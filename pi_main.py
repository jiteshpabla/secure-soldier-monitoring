from RPLCD.gpio import CharLCD
from RPi import GPIO
import time

#----
import serial
ser = serial.Serial('/dev/ttyACM0', 9600)
#----


########-------------------------
import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#--------------FILE--------------
fil = open('ou1.txt','w')
#fi.write("basb") 
#--------------------------------

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

gps_data = "0,0"
#gps_data = "23.12345,78.12345"

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c
##########-------------------------


lcd = CharLCD(pin_rs=26, pin_e=24, pins_data=[22, 18, 16, 12],
              numbering_mode=GPIO.BOARD,
              cols=20, rows=4, dotsize=8,
              charmap='A02',
              auto_linebreaks=True)

#--------button----------
import RPi.GPIO as GPIO
import time

#GPIO.setmode(GPIO.BCM)

GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO17
GPIO.setup(13, GPIO.OUT)  #LED to GPIO27
#------------------------



####-----------------------SERVER------------------------
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
####---------------------SERVER-END------------------------

#fi.write("honda")
try:
        while True:
                button_state = GPIO.input(11)
                butt_flag = "0"
                if button_state == False:
                        GPIO.output(13, True)
                        #print('Button Pressed...')
                        butt_flag = "1"
                        #time.sleep(0.01)
                else:
                        GPIO.output(13, False)
                        butt_flag = "0"
                temp_val = str(read_temp())
                bpm_val = str(ser.readline())

                dispText = "temp="+temp_val+"|"+"BPM="+bpm_val+"|"+"pos="+gps_data+"|"+"btn="+butt_flag
                print dispText
                fil.write(dispText+"\n")
                #fi.write("heeeloo")
                lcd.clear()
                lcd.clear()
                lcd.write_string(dispText)

                send_text ="time_stamp="+str(time.time())+"|"+"mod_id=sm_0001|"+dispText

                ###-----------SERVER---------------------
                # Enable Serial Communication
                port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
                 
                # Transmitting AT Commands to the Modem
                # '\r\n' indicates the Enter key
                ###### ENCRYPTING
                data = (send_text).encode("utf-8")

                cipher_rsa = PKCS1_OAEP.new(recipient_key)
                enc_session_key = cipher_rsa.encrypt(session_key)

                # Encrypt the data with the AES session key
                cipher_aes = AES.new(session_key, AES.MODE_EAX)
                ciphertext, tag = cipher_aes.encrypt_and_digest(data)
                cipher = ciphertext + "join" + tag + "nonce" + cipher_aes.nonce + "key" + enc_session_key
                #cipher = [ x for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
                file_out.write(cipher)

                port.write('AT'+'\r\n')
                #rcv = port.read(10)
                #print rcv
                #time.sleep(1)
                 
                port.write('ATE0'+'\r\n')      # Disable the Echo
                #rcv = port.read(10)
                #print rcv
                #time.sleep(1)
                 
                port.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode 
                #rcv = port.read(10)
                #print rcv
                #time.sleep(1)
                 
                port.write('AT+CNMI=2,1,0,0,0'+'\r\n')   # New SMS Message Indications
                #rcv = port.read(10)
                #print rcv
                #time.sleep(1)
                 
                # Sending a message to a particular Number
                 
                port.write('AT+CMGS="9953798329"'+'\r\n')
                #rcv = port.read(10)
                #print rcv
                #time.sleep(1)
                 
                port.write(send_text+'\r\n')  # Message
                #rcv = port.read(10)
                #print rcv
                 
                port.write("\x1A") # Enable to send SMS
                #for i in range(10):
                #    rcv = port.read(10)
                #    print rcv
                i=i+1

                ###-----------SERVER--END------------------
                time.sleep(5.0000)
except KeyboardInterrupt:
        pass
finally:
        lcd.clear()
        lcd.write_string(u'script stopped')
        time.sleep(1)
        lcd.clear()
        GPIO.cleanup()
