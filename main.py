import RPi.GPIO as GPIO
import time
import signal
import network
import arduino
from PN532 import PN532
from models import KeyId
from tabulate import tabulate
import input

def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
    pn532.close()

def callbackPN532(tag, data):
    global incoming_data
    incoming_data = data

def check_token(token,id):
    keyValidation = network.validate_token(token,id)
    print( "\t"+keyValidation.message)
    return keyValidation.succes

def is_authorized(incoming_user_id,device_id,token):
    global office_id
    print("VALIDATION:")
    keyId = KeyId(int(incoming_user_id),office_id,device_id)
    return check_token(token,keyId)

def print_office_selection_menu():
    menu = network.get_offices_menu()
    list_offices_by_company_name = []
    currentName = " "
    count=-1
    for item in menu:
        if currentName != item[1]:
            currentName = item[1]
            list_offices_by_company_name.append([currentName,[]])
            count+=1
        list_offices_by_company_name[count][1].append([item[0],item[2].to_format_string()])

    for item in list_offices_by_company_name:
        print(str(item[0]).upper())
        line = ""
        for i in item[0]:
            line+="-"
        print(line)
        print( tabulate(item[1], headers=['ID', 'address']))
        print(" ")
    print(" ")



# ctrl + c stop
signal.signal(signal.SIGINT, end_read)
continue_reading = True

# device uart, aid for android, callback
pn532 = PN532('tty:S0', 'A0000001020304', callbackPN532)
incoming_data = ""

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

def open_door():
    message = "ACCESS GRANTED"
    print(message)
    arduino.open_servo_door()
    GPIO.output(GREEN_LED, GPIO.HIGH)
    time.sleep(10)
    arduino.close_servo_door()
    GPIO.output(GREEN_LED, GPIO.LOW)

def access_denied():
    message = "ACCESS DENIED"
    arduino.print_to_lcd(message)
    print(message)
    GPIO.output(RED_LED, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(RED_LED, GPIO.LOW)


# Welcome message
print(" _______________________________ ")
print("|                               |")
print("|    Welcome to GATESIM v2.0    |")
print("|                               |")
print("|          ~ By BVE ~           |")
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

print_office_selection_menu()
office_id = input.inputNumber("What office do you want to simulate:")

info_array = network.get_office_info(office_id)

print("")
print("simulated gate:")
print("")
for i in info_array:
    print("\t\t"+ i)
print("")
arduino.print_address_to_lcd(info_array[0])

while continue_reading:
    listen = pn532.listen()
    if not listen:
        break

    #convert hexstring to asci string and split data
    print("incoming data hex: "+ str(incoming_data))
    incoming_data_string = str(incoming_data)

    if incoming_data_string[len(incoming_data_string) - 4: len(incoming_data_string)] == "9000":
        incoming_ids_hex = incoming_data_string[0:len(incoming_data_string)-4]
        incoming_ids_ascii = bytes.fromhex(incoming_ids_hex).decode("ASCII").split(";")

        incoming_user_id = incoming_ids_ascii[0]
        incoming_device_id = incoming_ids_ascii[1]
        incoming_token = incoming_ids_ascii[2]
        incoming_data=""
        print("incoming user id: "+str(incoming_user_id))
        print("incoming device id: "+str(incoming_device_id))
        print("incoming token: " + str(incoming_token))
        print("")
        message = ""
        if(is_authorized(incoming_user_id,incoming_device_id,incoming_token)):
            open_door()
        else:
            access_denied()

    else:
        print("response APDU not supported or interrupted")
        access_denied()
    print("_________________________________")
    print("")