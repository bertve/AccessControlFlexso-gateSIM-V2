import RPi.GPIO as GPIO
import time
import signal
from colorama import init,Fore,Back,Style
import network

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

init(convert=True)
signal.signal(signal.SIGINT, end_read)
continue_reading = True

# Welcome message
print(Fore.WHITE+ Back.GREEN + "aids")
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
print(Style.RESET_ALL)

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

#harcoded incoming message
incoming_nfc_message_succes = 3 #vaneebe@cronos.be
incoming_nfc_message_fail = 4
#change this to test
incoming_nfc_message = incoming_nfc_message_fail

#harcoded office id
office_id = 1

while continue_reading:
    # get authorized users
    auth_ids = network.get_auth_ids_by_office_id(office_id)
    print("incoming message: "+ str(incoming_nfc_message))
    if(check_if_user_auth(auth_ids,incoming_nfc_message)):
        print(Fore.GREEN)
        print("ACCESS GRANTED")
        GPIO.output(GREEN_LED, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(GREEN_LED, GPIO.LOW)
    else:
        print(Fore.RED)
        print("ACCESS DENIED")
        GPIO.output(RED_LED, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(RED_LED, GPIO.LOW)







