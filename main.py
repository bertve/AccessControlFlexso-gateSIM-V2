import RPi.GPIO as GPIO
import time
import signal
import network
from PN532 import PN532

def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

def check_if_user_auth(auth_ids,incoming_nfc_message):
    for id in auth_ids:
        if(id == incoming_nfc_message):
            return True
    return False

def callbackPN532(tag, data):
    global incoming_data
    incoming_data = data


# ctrl + c stop
signal.signal(signal.SIGINT, end_read)
continue_reading = True

# device uart, aid for android, callback
pn532 = PN532('tty:S0', 'A0000001020304', callbackPN532)
incoming_data = ""


# Welcome message
print(" _______________________________ ")
print("|                               |")
print("|  Welcome to GATESIMBIRT v2.0  |")
print("|_______________________________|")
print("|             _____             |")
print("|            |\    |            |")
print("|            | \   |            |")
print("|            |  |  |            |")
print("|            | \|  |            |")
print("|            \  |__|            |")
print("|             \ |               |")
print("|              \|               |")
print("|                               |")
print("|     Press Ctrl-C to stop.     |")
print("|_______________________________|")
print("")

# setup mode gpio (according to gpio numbers)
GPIO.setmode(GPIO.BCM)

# Configure GREEN LED Output Pin
GREEN_LED = 5
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.output(GREEN_LED, GPIO.LOW)

# configure RED LED Output Pin
RED_LED = 6
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.output(RED_LED, GPIO.LOW)

#harcoded office id
office_id = 1

while continue_reading:
    listen = pn532.listen()
    if not listen:
        break

    # get authorized users
    auth_ids = network.get_auth_ids_by_office_id(office_id)

    #convert hexstring to asci string
    incoming_data_ascii = bytes.fromhex(str(incoming_data)).decode("ASCII")
    print("incoming message hex: "+ str(incoming_data))
    print("incoming message ascii: " + incoming_data_ascii)

    if(check_if_user_auth(auth_ids,incoming_data)):
        print("ACCESS GRANTED")
        GPIO.output(GREEN_LED, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(GREEN_LED, GPIO.LOW)
    else:
        print("ACCESS DENIED")
        GPIO.output(RED_LED, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(RED_LED, GPIO.LOW)
    print("")


pn532.close()





