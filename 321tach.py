import string
import time
import bluetooth #MAY NEED TO INSTALL python-bluez LIBRARY
import RPi.GPIO as GPIO
import sys

MACadd = "00:1D:A5:68:98:8C" #DAVE'S DONGLE (ELM327 v2.1) CHANGE THIS TO YOUR MAC ADDRESS 

def connect():
    print("Opening Bluetooth socket...")
    count = 0
    while 1:
        try:
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((MACadd, 1))
            break
        except bluetooth.btcommon.BluetoothError as error:
            sock.close()
            count += 1
            if count == 5:
                sys.exit()
            print ("Could not connect: ", error, "; Retrying in 2 seconds...")
            time.sleep(2)
    print("Socket successfully opened!")
    return sock
	
def sendrecv(cmd, sock): #SENDS COMMAND TO DONGLE, RECEIVES DATA FROM DONGLE 
    sock.send(cmd + "\r\n")
    time.sleep(0.05)      #SLEEP TO HELP YOUR DONGLE
    while 1:
        buffer = ''
        while 1:
   	    sym = sock.recv(1)
            #print("sym is: %s", sym)
            if(sym == '\r' or sym == '>') and (len(buffer) > 0):
                break
            else:
                if (sym != '\r') and (sym != '>'):
                    buffer = buffer + sym
        #print("Here!")
        #print(buffer)
	if buffer != "" and buffer != "\r" and buffer != cmd and buffer != (">" + cmd):
            if buffer == "SEARCHING...":
                continue
            if buffer == "?":
                print('Received "?" because an invalid command was sent.')
                sys.exit()
            if buffer == "UNABLE TO CONNECT":
                print('Received "UNABLE TO CONNECT"')
                connect()
            sock.recv(2) #REMOVES THE "\r>" WAITING TO BE RECEIVED
            return buffer


if __name__ == "__main__":
	
        sock = connect()
	#INITIALIZE LED GPIO PINS
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(14,GPIO.OUT)
	GPIO.setup(15,GPIO.OUT)
	GPIO.setup(18,GPIO.OUT)
	GPIO.setup(23,GPIO.OUT)
	GPIO.setup(24,GPIO.OUT)
	GPIO.setup(25,GPIO.OUT)
	GPIO.setup(8,GPIO.OUT)
	#CHECK THAT LED's ARE OFF
	GPIO.output(14,GPIO.LOW)
	GPIO.output(15,GPIO.LOW)
	GPIO.output(18,GPIO.LOW)
	GPIO.output(23,GPIO.LOW)
	GPIO.output(24,GPIO.LOW)
	GPIO.output(25,GPIO.LOW)
	GPIO.output(8,GPIO.LOW)

	#TEST-LED SEQUENCE
	GPIO.output(14,GPIO.HIGH)
	time.sleep(.1)
	GPIO.output(15,GPIO.HIGH)
	time.sleep(.1)
	GPIO.output(18,GPIO.HIGH)
	time.sleep(.1)
	GPIO.output(23,GPIO.HIGH)
	time.sleep(.1)
	GPIO.output(24,GPIO.HIGH)
	time.sleep(.1)
	GPIO.output(25,GPIO.HIGH)
	time.sleep(.1)
	GPIO.output(8,GPIO.HIGH)
	time.sleep(.3)
	GPIO.output(8,GPIO.LOW)
	time.sleep(.09)
	GPIO.output(25,GPIO.LOW)
	time.sleep(.09)
	GPIO.output(24,GPIO.LOW)
	time.sleep(.09)
	GPIO.output(23,GPIO.LOW)
	time.sleep(.09)
	GPIO.output(18,GPIO.LOW)
	time.sleep(.09)
	GPIO.output(15,GPIO.LOW)
	time.sleep(.09)
	GPIO.output(14,GPIO.LOW)

	#SEND COMMAND "atz" TO RESET DONGLE
	res = sendrecv("atz", sock)
	print("atz response is:")
	print(res)

	#SEND COMMAND "ate0" TO TURN OFF ECHOES
	res = sendrecv("ate0", sock)
	print("ate0 response is:")
	print(res)

	#LOOP FOR RPM 
	while 1:
		res = sendrecv("010C", sock)
		if (res == "NO DATA"):
		    sock.close()
		    connect()
		    sendrecv("atz", sock)
		    sendrecv("ate0", sock)
		    continue
		elif (res == "STOPPED"):
		    sock.close()
		    connect()
		    sendrecv("atz", sock)
		    sendrecv("ate0")
		    continue
		data = res.split()

	#EXCEPTION (IGNORE) WHEN len(LIST) < 3
		try:
		    a = int(data[2], 16)
		    b = int(data[3], 16)
		except IndexError:
		    print("IndexError occurred. data is:")
		    print(data)
		    continue
		
		RPM = ((256 * a) + b) / 4
	       #print("RPM is %d" % RPM)
	   #time.sleep(.1)
		
	   # if(rpm > 0) and (rpm <= 800):
		   # GPIO.output(25,GPIO.LOW)
		   # GPIO.output(24,GPIO.LOW)
		   # GPIO.output(23,GPIO.LOW)
		   # GPIO.output(18,GPIO.LOW)
		   # GPIO.output(15,GPIO.LOW)
		   # GPIO.output(14,GPIO.LOW)
		if(RPM <= 1000):
		    GPIO.output(25,GPIO.LOW)
		    GPIO.output(24,GPIO.LOW)
		    GPIO.output(23,GPIO.LOW)
		    GPIO.output(18,GPIO.LOW)
		    GPIO.output(15,GPIO.LOW)
		    GPIO.output(14,GPIO.HIGH)
		    GPIO.output(8,GPIO.LOW)
		elif(RPM > 1000) and (RPM <= 1500):
		    GPIO.output(25,GPIO.LOW)
		    GPIO.output(24,GPIO.LOW)
		    GPIO.output(23,GPIO.LOW)
		    GPIO.output(18,GPIO.LOW)
		    GPIO.output(14,GPIO.HIGH)
		    GPIO.output(15,GPIO.HIGH)
		    GPIO.output(8,GPIO.LOW)
		elif(RPM > 1500) and (RPM <= 2000):
		    GPIO.output(25,GPIO.LOW)
		    GPIO.output(24,GPIO.LOW)
		    GPIO.output(23,GPIO.LOW)
		    GPIO.output(14,GPIO.HIGH) 
		    GPIO.output(15,GPIO.HIGH)
		    GPIO.output(18,GPIO.HIGH)
		    GPIO.output(8,GPIO.LOW)
		elif(RPM > 2000) and (RPM <= 2500):
		    GPIO.output(25,GPIO.LOW)
		    GPIO.output(24,GPIO.LOW)
		    GPIO.output(14,GPIO.HIGH)
		    GPIO.output(15,GPIO.HIGH)
		    GPIO.output(18,GPIO.HIGH)
		    GPIO.output(23,GPIO.HIGH)
		    GPIO.output(8,GPIO.LOW)
		elif(RPM > 2500) and (RPM <= 3000):
		    GPIO.output(25,GPIO.LOW)
		    GPIO.output(14,GPIO.HIGH)
		    GPIO.output(15,GPIO.HIGH)
		    GPIO.output(18,GPIO.HIGH)
		    GPIO.output(23,GPIO.HIGH)
		    GPIO.output(24,GPIO.HIGH)
		    GPIO.output(8,GPIO.LOW)
		elif(RPM > 3000) and (RPM < 3900):
		    GPIO.output(14,GPIO.HIGH)
		    GPIO.output(15,GPIO.HIGH)
		    GPIO.output(18,GPIO.HIGH)
		    GPIO.output(23,GPIO.HIGH)
		    GPIO.output(24,GPIO.HIGH)
		    GPIO.output(25,GPIO.HIGH)
		    GPIO.output(8,GPIO.LOW)
		elif(RPM >= 3900 and RPM <= 6000):
		    GPIO.output(14,GPIO.HIGH)
		    GPIO.output(15,GPIO.HIGH)
		    GPIO.output(18,GPIO.HIGH)
		    GPIO.output(23,GPIO.HIGH)
		    GPIO.output(24,GPIO.HIGH)
		    GPIO.output(25,GPIO.HIGH)
		    GPIO.output(8,GPIO.HIGH)
		    time.sleep(0.05)
		    GPIO.output(8,GPIO.LOW)
		    time.sleep(0.04)
		elif(RPM > 6000):
		    continue
                else:
		    print("Something went horribly wrong...")
		
        sock.close()
