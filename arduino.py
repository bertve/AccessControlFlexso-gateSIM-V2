import serial
import RPi.GPIO as GPIO
import signal

def end_read(signal,frame):
    global loop
    print("Ctrl+C captured, ending read from arduino.")
    loop = False
    GPIO.cleanup()

signal.signal(signal.SIGINT, end_read)


ser = serial.Serial("/dev/ttyACM0",9600)
ser.baudrate = 9600

loop = True

while loop:
    read_ser = ser.readline().decode('utf-8')
    print(read_ser)

