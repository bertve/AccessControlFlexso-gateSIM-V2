import serial
import time

ser = serial.Serial("/dev/ttyACM0",9600)
ser.baudrate = 9600

def print_to_lcd(message):
    message = "PRINT;"+ message + "\n"
    ser.write(message.encode("ASCII"))

def print_address_to_lcd(address):
    message = "ADDRESS;" + address + "\n"
    ser.write(message.encode("ASCII"))

def open_servo_door():
    ser.write("SERVO;OPEN\n".encode("ASCII"))

def close_servo_door():
    ser.write("SERVO;CLOSE\n".encode("ASCII"))

def input_display():
    previous_message = "waiting"
    while True:
        print_to_lcd()
        input_user = input("prompt message:")
        if input_user != previous_message:
            previous_message = input_user

        print_to_lcd(previous_message)
        time.sleep(5)







