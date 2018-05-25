import RPi.GPIO as GPIO
import time
import serial
import sys
import getopt
import string 
import datetime
import select
import termios
import sys
import tty
import os

def isData():
	return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def separator():
	print " "	
	print "=============================================================================="
	print " "	


INP_LEFT=28
INP_RIGHT=29
RELAY_LEFT=21
RELAY_RIGHT=22
WIFI_POWER=37

RED_LED=36
GREEN_LED=35
BLUE_LED=34

GROVE_1_SDA=44
GROVE_1_SCL=45

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RELAY_LEFT,GPIO.OUT)
GPIO.setup(RELAY_RIGHT,GPIO.OUT)
GPIO.setup(WIFI_POWER,GPIO.OUT)
GPIO.setup(INP_LEFT,GPIO.IN)
GPIO.setup(INP_RIGHT,GPIO.IN)

GPIO.setup(RED_LED,GPIO.OUT)
GPIO.setup(GREEN_LED,GPIO.OUT)
GPIO.setup(BLUE_LED,GPIO.OUT)

GPIO.output(RED_LED,GPIO.HIGH)
GPIO.output(GREEN_LED,GPIO.HIGH)
GPIO.output(BLUE_LED,GPIO.HIGH)

old_settings = termios.tcgetattr(sys.stdin)

try:
	tty.setcbreak(sys.stdin.fileno())

	step=0

	print "***********************"
	print " Megatest per CM3-Home "
	print "***********************"

	#*************************************************************************************

	step=step+1
	separator()
	print "Step %02d: Yarm" % (step)
	print "  g=Go l='ls /dev/ttyUSBx' n=Next"


	test_running=False
	tx_counter=0
	rx_counter=0
	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				if test_running==True:
					serial_yarm.close()
				break

			if c=="l":
				os.system("ls /dev/ttyUSB*")

			if c=="g":
				print "  a=SDL b=SCL n=Next"
				serial_yarm = serial.Serial(
					port='/dev/ttyUSB1',
					baudrate=115200,
					timeout=1,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					bytesize=serial.EIGHTBITS
				)
				serial_yarm.flushOutput()
				serial_yarm.flushInput()

				test_running=True

			serial_yarm.write("%c" % (c))

		if test_running==True:
			if serial_yarm.inWaiting() > 0:
				rx=serial_yarm.read(1);
				sys.stdout.write(rx)

	#*************************************************************************************

	separator()
	step=step+1
	print "Step %02d: FT4232H eeprom programming" % (step)
	print "  e=Erase p=Program l='ls /dev/ttyUSB*' n=Next"

	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				break

			if c=="e":
				os.system("sudo ftdi_eeprom --erase-eeprom cm3home.conf")

			if c=="p":
				os.system("sudo ftdi_eeprom --flash-eeprom cm3home.conf")

			if c=="l":
				os.system("ls /dev/ttyUSB*")

	#*************************************************************************************

	separator()
	step=step+1
	print "Step %02d: RGB led" % (step)
	print "  g=Go n=Next"

	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				break

			if c=="g":
				for i in range(2):
					GPIO.output(RED_LED,GPIO.LOW)
					GPIO.output(GREEN_LED,GPIO.HIGH)
					GPIO.output(BLUE_LED,GPIO.HIGH)
					time.sleep(0.5)

					GPIO.output(RED_LED,GPIO.HIGH)
					GPIO.output(GREEN_LED,GPIO.LOW)
					GPIO.output(BLUE_LED,GPIO.HIGH)
					time.sleep(0.5)

					GPIO.output(RED_LED,GPIO.HIGH)
					GPIO.output(GREEN_LED,GPIO.HIGH)
					GPIO.output(BLUE_LED,GPIO.LOW)
					time.sleep(0.5)

				GPIO.output(RED_LED,GPIO.HIGH)
				GPIO.output(GREEN_LED,GPIO.HIGH)
				GPIO.output(BLUE_LED,GPIO.HIGH)

	#*************************************************************************************

	separator()
	step=step+1
	print "Step %02d: Inp 1/2 test" % (step)
	print "  g=Go n=Next"

	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				break
				
			if c=="g":
				for i in range(2):
					GPIO.output(RELAY_LEFT,GPIO.HIGH)
					time.sleep(0.5)
					if not GPIO.input(INP_LEFT):
						print "LEFT IN/OUT +++OK+++"
					else:
						print "LEFT IN/OUT ---kO---"
					time.sleep(0.5)
					GPIO.output(RELAY_LEFT,GPIO.LOW)
					
					GPIO.output(RELAY_RIGHT,GPIO.HIGH)
					time.sleep(0.5)
					if not GPIO.input(INP_RIGHT):
						print "LEFT IN/OUT +++OK+++"
					else:
						print "LEFT IN/OUT ---kO---"
					time.sleep(0.5)
					GPIO.output(RELAY_RIGHT,GPIO.LOW)



	#*************************************************************************************

	separator()
	step=step+1
	print "Step %02d: Port Grove 1 - GPIO mode" % (step)
	print "  g=Go n=Next"

	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				break

			if c=="g":
			
				GPIO.setup(GROVE_1_SDA,GPIO.OUT)
				GPIO.setup(GROVE_1_SCL,GPIO.OUT)
				GPIO.output(GROVE_1_SDA,GPIO.LOW)
				GPIO.output(GROVE_1_SCL,GPIO.LOW)

				for i in range(2):
					GPIO.output(GROVE_1_SDA,GPIO.HIGH)
					GPIO.output(GROVE_1_SCL,GPIO.LOW)

					time.sleep(0.5)

					GPIO.output(GROVE_1_SDA,GPIO.LOW)
					GPIO.output(GROVE_1_SCL,GPIO.HIGH)

					time.sleep(0.5)

				GPIO.setup(GROVE_1_SDA,GPIO.IN)
				GPIO.setup(GROVE_1_SCL,GPIO.IN)

	#*************************************************************************************

	separator()
	step=step+1
	print "Step %02d: Grove connector 1 test in I2C mode" % (step)
	print "  g=Go n=Next"

	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				break

			if c=="g":
				os.system("i2cdetect -y 1")


	#*************************************************************************************

	separator()
	step=step+1
	print "Step %02d: Camera" % (step)
	print "  g=Go n=Next"

	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				break

			if c=="g":
				os.system("CAMERA=pi python /home/pi/flask-video-streaming/app.py &")
				print "http://cm3home.local:5000"

	#*************************************************************************************

	separator()
	step=step+1
	print "Step %02d: Serial 3V3 test" % (step)
	print "  g=Go l='ls /dev/ttyUSBx' n=Next"


	test_running=False
	tx_counter=0
	rx_counter=0
	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				if test_running==True:
					serial_usb.close()
					serial_ttl.close()
				break

			if c=="l":
				os.system("ls /dev/ttyUSB*")

			if c=="g":
				serial_usb = serial.Serial(
					port='/dev/ttyUSB4',
					baudrate=115200,
					timeout=1,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					bytesize=serial.EIGHTBITS
				)
				serial_usb.flushOutput()
				serial_usb.flushInput()

				serial_ttl = serial.Serial(
					port='/dev/ttyUSB3',
					baudrate=115200,
					timeout=0.1,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					bytesize=serial.EIGHTBITS
				)
				serial_ttl.flushOutput()
				serial_ttl.flushInput()

				test_running=True

		if test_running==True:	
			tx_counter=tx_counter+1
			serial_usb.write("USB to Serial: %08d" % (tx_counter))
			time.sleep(0.1)
			print serial_ttl.read(23)

			rx_counter=rx_counter+1
			serial_ttl.write("Serial to USB: %08d" % (rx_counter))
			time.sleep(0.1)
			print serial_usb.read(23)

			if tx_counter==10:
				test_running=False

					
	#*************************************************************************************

	separator()
	step=step+1
	print "Step %02d: RS485-left test" % (step)
	print "  g=Start l='ls /dev/ttyUSBx' n=Next"

	test_running=False
	tx_counter=0
	rx_counter=0
	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				if test_running==True:
					serial_usb.close()
					serial_ttl.close()
				break

			if c=="l":
				os.system("ls /dev/ttyUSB*")

			if c=="g":
				serial_usb = serial.Serial(
					port='/dev/ttyUSB5',
					baudrate=115200,
					timeout=1,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					bytesize=serial.EIGHTBITS
				)
				serial_usb.flushOutput()
				serial_usb.flushInput()

				serial_ttl = serial.Serial(
					port='/dev/ttyUSB0',
					baudrate=115200,
					timeout=0.1,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					bytesize=serial.EIGHTBITS
				)
				serial_ttl.flushOutput()
				serial_ttl.flushInput()

				test_running=True

		if test_running==True:	
			tx_counter=tx_counter+1
			serial_usb.write("USB to RS485L: %08d" % (tx_counter))
			time.sleep(0.1)
			print serial_ttl.read(23)

			rx_counter=rx_counter+1
			serial_ttl.write("RS485L to USB: %08d" % (rx_counter))
			time.sleep(0.1)
			print serial_usb.read(23)
			
			if tx_counter==10:
				test_running=False

					
	#*************************************************************************************

	separator()
	step=step+1
	print "Step %02d: RS485-right test" % (step)
	print "  g=Start l='ls /dev/ttyUSBx' n=Next"

	test_running=False
	tx_counter=0
	rx_counter=0
	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				if test_running==True:
					serial_usb.close()
					serial_ttl.close()
				break

			if c=="l":
				os.system("ls /dev/ttyUSB*")

			if c=="g":
				serial_usb = serial.Serial(
					port='/dev/ttyUSB5',
					baudrate=115200,
					timeout=1,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					bytesize=serial.EIGHTBITS
				)
				serial_usb.flushOutput()
				serial_usb.flushInput()

				serial_ttl = serial.Serial(
					port='/dev/ttyUSB2',
					baudrate=115200,
					timeout=0.1,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					bytesize=serial.EIGHTBITS
				)
				serial_ttl.flushOutput()
				serial_ttl.flushInput()

				test_running=True

		if test_running==True:	
			tx_counter=tx_counter+1
			serial_usb.write("USB to RS485R: %08d" % (tx_counter))
			time.sleep(0.1)
			print serial_ttl.read(23)

			rx_counter=rx_counter+1
			serial_ttl.write("RS485R to USB: %08d" % (rx_counter))
			time.sleep(0.1)
			print serial_usb.read(23)

			if tx_counter==10:
				test_running=False

					
	#*************************************************************************************

	separator()
	step=step+1
	print "Step %02d: WiFi test" % (step)
	print "  1=On 0=Off i=ifconfig n=Next"

	test_running=False
	tx_counter=0
	rx_counter=0
	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				break

			if c=="1":
				GPIO.output(WIFI_POWER,GPIO.HIGH)
				continue

			if c=="0":
				GPIO.output(WIFI_POWER,GPIO.LOW)
				continue

			if c=="i":
				os.system("ifconfig")
				continue

	#*************************************************************************************

	separator()
	step=step+1
	print "Step %02d: Audio test" % (step)
	print "  g=Go n=Next"

	test_running=False
	tx_counter=0
	rx_counter=0
	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				break

			if c=="g":
				os.system("omxplayer -o local speaker_test.wav")
				continue
					
	#*************************************************************************************

	separator()
	step=step+1
	print "Step %02d: 1-wire test" % (step)
	print "  g=Go n=Next"

	test_running=False
	tx_counter=0
	rx_counter=0
	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				break

			if c=="g":
				for i in range(2):
					os.system("ls /sys/bus/w1/devices/")
					continue
					
	#*************************************************************************************

	separator()
	step=step+1
	print "Step %02d: IR test" % (step)
	print "  g=Go n=Next"

	test_running=False
	tx_counter=0
	rx_counter=0
	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				break

			if c=="g":
				os.system("sudo ir-keytable -p rc-5")
				os.system("ir-keytable -t -v &")
				continue

	#*************************************************************************************

	separator()
	step=step+1
	print "Step %02d: Ethernet test" % (step)
	print "  g=Go n=Next"

	test_running=False
	tx_counter=0
	rx_counter=0
	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				break

			if c=="g":
				os.system("ping -c 4 www.acmesystems.it")
				continue

	#*************************************************************************************

	separator()
	step=step+1
	print "Step %02d: Light bus test" % (step)
	print "  g=Go n=Next"

	test_running=False
	tx_counter=0
	rx_counter=0
	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				break

			if c=="g":
				for i in range(10):
					os.system("python dali.py 254 254 254 254")
					continue
					time.sleep(0.1)
					os.system("python dali.py 0 0 0 0")
					continue
					time.sleep(0.1)

					
	#*************************************************************************************

	separator()
	step=step+1
	print "Step %02d: TP-Bus test" % (step)
	print "  1=On 0=Off n=Next"

	while True:
		if isData():
			c = sys.stdin.read(1)

			if c=="n":
				break

			if c=="1":
				os.system("knxtool on ip:localhost 1/6/105")

			if c=="0":
				os.system("knxtool off ip:localhost 1/6/105")

	#*************************************************************************************

finally:
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
	
