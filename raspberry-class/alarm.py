#####################################################################
#                                                                   #
#  file name   : alarm.py                                           #
#  file number : #2                                                 #  
#  brief       : check if the alarm state is changed                #
#  for more info and ref, pls visit https://hackmd.io/s/SyB9BfizZ   #
#                                                                   #
#####################################################################

print("Welcome to the Monitor System,")
print("please wait about 3 sec for the system to initialize.")
print("=====================================================================")

import urllib.request
from bs4 import BeautifulSoup
import sys
import time
import RPi.GPIO as GPIO



#################### Defines ##############################
AlarmLedPin=14
SwLedPin=15
ButtonPin=23
BzrPin=18
MonitorState = False # False: not to alarm, True: alarm mode
TriggedFlag = True # print Trigger OFF status if this value = "True"


#################### GPIO initialization ##################
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(AlarmLedPin, GPIO.OUT)
GPIO.setup(SwLedPin   , GPIO.OUT)
GPIO.setup(BzrPin     , GPIO.OUT)
GPIO.setup(ButtonPin  , GPIO.IN)

#################### BeautifulSoup here ####################
url="http://140.113.123.151:80/FP/detect.html"
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'} # Fake web browser info

def GetTrigger():
	# get website data
	req = urllib.request.Request(url = url,headers=headers)
	page = urllib.request.urlopen(req)
	contentBytes = page.read()
	
	# find tag h1
	soup = BeautifulSoup(str(contentBytes), "html.parser")
	matches =  str(soup.find("h1"))

	# process the string we just got
	return "On" if matches.count("Alarm")==1 else "Off"



def AlarmTrigged(count):
	for j in range(0,count):
		GPIO.output(AlarmLedPin, GPIO.HIGH)
		for i in range(0,100):
			GPIO.output(BzrPin, GPIO.HIGH)
			time.sleep(.001)
			GPIO.output(BzrPin, GPIO.LOW)
			time.sleep(.001)
		GPIO.output(AlarmLedPin, GPIO.LOW)
		time.sleep(0.2)
		

try:
	while True:
		GPIO.output(SwLedPin, GPIO.LOW)
		
		print("Monitor now OFFLINE. ", end='')
		print("To start monitor, just press the button.")
		
		while not GPIO.input(ButtonPin): # Button Pressed
			time.sleep(0.00001)
		MonitorState=True
		time.sleep(0.1)
		
		print("Monitor now ONLINE ")
		print("    Trigger now OFF")
		TriggedFlag = False
				
		while True :

			GPIO.output(SwLedPin, GPIO.HIGH)
			
			trigger = GetTrigger()
			
			if GPIO.input(ButtonPin):
				if trigger=="On":
					print("        ERROR: Unable to turn off the monitor during alarmed state")
				else:
					GPIO.output(SwLedPin, GPIO.LOW)
					print("=====================================================================")
					time.sleep(0.5)
					break	
			
			if MonitorState and trigger=="On" :
				if not (TriggedFlag):
					print("    Trigger now ON !!")
				AlarmTrigged(5)
				TriggedFlag = True
				
			if TriggedFlag and trigger=="Off" :
				print("    Trigger now OFF")
				TriggedFlag = False
			


except KeyboardInterrupt:
	GPIO.cleanup()
	print("\nKeyboardInterrupt")




