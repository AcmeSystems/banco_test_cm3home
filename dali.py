#!/usr/bin/python
# Documentazione comandi DALI
# http://www.tanzolab.it/www/CM3-HOME_test/dali_commands.pdf

import RPi.GPIO as GPIO
import time
import sys

#GPIO line used for LIGHT-BUS
GPIO_TX_LINE=31

BIT_DELAY=0.00034
LED_RED=22
LED_GREEN=23
LED_BLUE=24
LED_WHITE=25


def send_start():
    global BIT_DELAY
    global GPIO_TX_LINE
    
    GPIO.output(GPIO_TX_LINE,GPIO.LOW)
    time.sleep(BIT_DELAY)
    GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
    time.sleep(BIT_DELAY)

def send_1():
    global BIT_DELAY
    global GPIO_TX_LINE

    GPIO.output(GPIO_TX_LINE,GPIO.LOW)
    time.sleep(BIT_DELAY)
    GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
    time.sleep(BIT_DELAY)

def send_0():
    global BIT_DELAY
    global GPIO_TX_LINE

    GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
    time.sleep(BIT_DELAY)
    GPIO.output(GPIO_TX_LINE,GPIO.LOW)
    time.sleep(BIT_DELAY)

def send_stop():
    global BIT_DELAY
    global GPIO_TX_LINE

    GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
    time.sleep(BIT_DELAY)
    GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
    time.sleep(BIT_DELAY)

def send_value(value):
	global BIT_DELAY
	global GPIO_TX_LINE

	for i in range(8):
		value=value&0xFF
		#print "%02x" % value 
		if (value & 0x80) == 0:
			send_0()
			#print "send 0"
		else:		
			send_1()
			#print "send 1"
		value=value<<1

def send_short_address(addr):
	global BIT_DELAY
	global GPIO_TX_LINE

	# Send first byte
	send_0() # Y=0 Short Address
	
	# Send 6 bit address. Most first
	if addr & 0x20:
		send_1()
	else:
		send_0()

	if addr & 0x10:
		send_1()
	else:
		send_0()

	if addr & 0x8:
		send_1()
	else:
		send_0()

	if addr & 0x4:
		send_1()
	else:
		send_0()
		
	if addr & 0x2:
		send_1()
	else:
		send_0()
	
	if addr & 0x1:
		send_1()
	else:
		send_0()
	
	send_0() # A=0 Direct arc power level


def send_color_value(led,value):
	if value>254:
		return

	if value<0:
		return

	send_start()
	send_short_address(led)
	send_value(value)
	send_stop()
	send_stop()
	time.sleep(0.001)
    
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GPIO_TX_LINE,GPIO.OUT)

# Initial state
GPIO.output(GPIO_TX_LINE,GPIO.HIGH)


send_start()
send_short_address(22)
send_value(0)
send_stop()
send_stop()
time.sleep(0.001)

send_start()
send_short_address(23)
send_value(0)
send_stop()
send_stop()
time.sleep(0.001)

send_start()
send_short_address(24)
send_value(0)
send_stop()
send_stop()
time.sleep(0.001)

send_start()
send_short_address(25)
send_value(0)
send_stop()
send_stop()

time.sleep(0.001)


#Demo mode
if len(sys.argv)==2:
	print "Demo mode"
	led=LED_WHITE
	
	for i in range(0,255,1):
		send_color_value(led,i)
		
	for i in range(255,-1,-1):
		send_color_value(led,i)

	#Final state 
	GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
	quit()

if len(sys.argv)<=5:
	print "dali.py red green blue white"
	print "        The color range is 0 to 254"

if len(sys.argv)==5:
	send_color_value(LED_RED,int(sys.argv[1]))
	send_color_value(LED_GREEN,int(sys.argv[2]))
	send_color_value(LED_BLUE,int(sys.argv[3]))
	send_color_value(LED_WHITE,int(sys.argv[4]))
    
#Final state 
GPIO.output(GPIO_TX_LINE,GPIO.HIGH)