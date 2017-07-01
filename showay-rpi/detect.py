#####################################################################
#                                                                   #
#  file name   : detect.py                                          #
#  file number : #1                                                 #  
#  brief       : detect the status of LDR and modify webpage        #
#  for more info and ref, pls visit https://hackmd.io/s/SyB9BfizZ   #
#                                                                   #
#####################################################################

import time
import RPi.GPIO as GPIO
from optparse import OptionParser

#################### initialization ##################
GPIO.setmode(GPIO.BCM)
LDRPin=3
LastState=0 # 0: safe,  1: alarm
NowState=0  # 0: safe,  1: alarm


#################### get optparse ##################
parser=OptionParser()
parser.add_option("-l", "--line", action="store", dest="AlarmLine", type="int", default=100, help="Used to set the alarm line, default=100")
options, args = parser.parse_args()
ALARM_LINE=options.AlarmLine
print(ALARM_LINE)


#################### make a file #################
def ModFile(state):
	f=open('detect.html','w',encoding='UTF-8')
	f.write('<!DOCTYPE html>')
	f.write('<head>')
	#f.write('<meta http-equiv="refresh" content="1" />')
	f.write('</head>')
	f.write('<body>')
	f.write('<h1>')
	f.write(state)
	f.write('</h1>')
	f.write('<iframe src="http://192.168.0.6:8081/" width="250px" height="300px" frameborder="0" scrolling="no"></iframe>')
	f.write('</body>')
	f.close()
	return 0


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
	ModFile("Start")
	while True:
		LDR_data=RCtime()
		print("RCtime=",end='')
		print(LDR_data)
		if LDR_data<ALARM_LINE :
			NowState=1
		else :
			NowState=0
		if NowState!=LastState :
			if NowState==1 : # alarm
				ModFile("Alarm!!!")
				LastState=1
				print("ALARM!!!!!!!!!")
			else : # safe
				ModFile("Safe")
				LastState=0
				print("SAFE")
		
		time.sleep(.1)
				
except KeyboardInterrupt:
	print("\nKeyboardInterrupt")
	GPIO.cleanup()
	

