#####################################################################
#                                                                   #
#  file name   : detect.py                                          #
#  file number : #1                                                 #  
#  brief       : detect the status of LDR and modify webpage        #
#  for more info and ref, pls visit https://hackmd.io/s/SyB9BfizZ   #
#                                                                   #
#####################################################################

#################### defines #####################
ALARM_LINE=100


import time
import RPi.GPIO as GPIO


#################### initialize ##################
GPIO.setmode(GPIO.BCM)
LDRPin=3


#################### read LDR data ###############
def RCtime(): 
	# black: >225
	reading=0
	GPIO.setup(LDRPin,GPIO.OUT)
	GPIO.output(LDRPin, GPIO.LOW)
	time.sleep(.1)
	GPIO.setup(LDRPin, GPIO.IN)
	while (GPIO.input(LDRPin)==GPIO.LOW):
		reading+=1
	return reading
	
try:
	while True:
		LDR_data=RCtime()
		print("RCtime=",end='')
		print(LDR_data)
		
		time.sleep(.1)
				
except KeyboardInterrupt:
	print("\nKeyboardInterrupt")
	GPIO.cleanup()
	