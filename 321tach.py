import string
import time
import bluetooth #MAY NEED TO INSTALL python-bluez LIBRARY
import RPi.GPIO as GPIO 

class ConnectFailureError(Exception):
    pass

class StateError(Exception):
    pass

class InvalidCmdError(Exception):
    pass

class NoDataError(Exception):
	MACadd = "00:1D:A5:68:98:8C" #DAVE'S DONGLE (ELM327 v2.1)
	'''while 1:
    		try:
        		sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        		sock.connect((MACadd, 1))
        		break
    		except bluetooth.btcommon.BluetoothError as error:
        		sock.close()
        		print ("Could not connect: ", error, "; Retrying in 2 seconds...")
        		time.sleep(2)
	print("Socket successfully opened!")'''
	pass
class StoppedError(Exception):
    pass

def redline():      #FUNCTION TO MAKE BLUE LED FREAK OUT
	GPIO.output(8,GPIO.HIGH)
	time.sleep(0.05)
	GPIO.output(8,GPIO.LOW)
	
def sendrecv(cmd): #SENDS COMMAND TO DONGLE, RECEIVES DATA FROM DONGLE, IGNORES NON-USEFUL DATA
    
    sock.send(cmd + "\r\n")
    time.sleep(0.0525)      #SLEEP TO HELP YOUR DONGLE
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
		    #self.log.debug(''.join(("Command ", cmd, " is invalid.")) )
                   raise InvalidCmdError("Command '%s' is invalid." % cmd)
                if buffer == "NO DATA":
		   #self.log.debug(''.join(("Command ", cmd, " produced NO DATA.")) )
                    raise NoDataError("Dongle returned 'NO DATA'.")
                if buffer == "STOPPED":
		   #self.log.warning(''.join(("ELM returned STOPPED")) )
                    raise StoppedError("Dongle returned 'STOPPED'.")
                sock.recv(2) # get rid of "\r>" that's still waiting to be received
                return buffer

#INITALIZE LED GPIO PINS
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

MACadd = "00:1D:A5:68:98:8C" #DAVE'S DONGLE (ELM327 v2.1)
print("Opening Bluetooth device...")

while 1:
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((MACadd, 1))
        break
    except bluetooth.btcommon.BluetoothError as error:
        sock.close()
        print ("Could not connect: ", error, "; Retrying in 2 seconds...")
        time.sleep(2)

print("Socket successfully opened!")

#SEND COMMAND "atz" TO CLEAR COMMANDS
res = sendrecv("atz")
print("atz response is:")
print(res)

#SEND COMMAND "ate0" TO TURN OF ECHOES
res = sendrecv("ate0")
print("ate0 response is:")
print(res)

#SEND COMMAND "0100" TP READY DONLE FOR COMMS
#res = sendrecv("0100")
#print("0100 response is:")
#print(res)


#LOOP FOR RPM 
while 1:
    res = sendrecv("010C")
    data = res.split()
    #print(data)

#EXCEPTION (IGNORE) WHEN len(LIST) < 3
    try:
        a = int(data[2], 16)
        b = int(data[3], 16)
    except IndexError:
	continue
    
    RPM = ((256 * a) + b) / 4
   #print("RPM is %d" % rpm)
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
    elif(RPM > 1000) and (RPM <= 1500):
        GPIO.output(25,GPIO.LOW)
        GPIO.output(24,GPIO.LOW)
        GPIO.output(23,GPIO.LOW)
        GPIO.output(18,GPIO.LOW)
        GPIO.output(14,GPIO.HIGH)
        GPIO.output(15,GPIO.HIGH)
	#redline()
    elif(RPM > 1500) and (RPM <= 2000):
        GPIO.output(25,GPIO.LOW)
        GPIO.output(24,GPIO.LOW)
        GPIO.output(23,GPIO.LOW)
        GPIO.output(14,GPIO.HIGH) 
        GPIO.output(15,GPIO.HIGH)
        GPIO.output(18,GPIO.HIGH)
    elif(RPM > 2000) and (RPM <= 2500):
        GPIO.output(25,GPIO.LOW)
        GPIO.output(24,GPIO.LOW)
        GPIO.output(14,GPIO.HIGH)
        GPIO.output(15,GPIO.HIGH)
        GPIO.output(18,GPIO.HIGH)
        GPIO.output(23,GPIO.HIGH)
    elif(RPM > 2500) and (RPM <= 3000):
        GPIO.output(25,GPIO.LOW)
        GPIO.output(14,GPIO.HIGH)
        GPIO.output(15,GPIO.HIGH)
        GPIO.output(18,GPIO.HIGH)
        GPIO.output(23,GPIO.HIGH)
        GPIO.output(24,GPIO.HIGH)
    elif(RPM > 3000) and (RPM < 3500):
        GPIO.output(14,GPIO.HIGH)
        GPIO.output(15,GPIO.HIGH)
        GPIO.output(18,GPIO.HIGH)
        GPIO.output(23,GPIO.HIGH)
	GPIO.output(24,GPIO.HIGH)
        GPIO.output(25,GPIO.HIGH)	
    elif(RPM >= 3500) and (RPM <= 4000):
        GPIO.output(14,GPIO.HIGH)
        GPIO.output(15,GPIO.HIGH)
	GPIO.output(18,GPIO.HIGH)
        GPIO.output(23,GPIO.HIGH)
	GPIO.output(24,GPIO.HIGH)
        GPIO.output(25,GPIO.HIGH)
        GPIO.output(8,GPIO.HIGH)
	time.sleep(0.05)
	GPIO.output(8,GPIO.LOW)
	#redline()	 	
    else:
	continue
sock.close()
