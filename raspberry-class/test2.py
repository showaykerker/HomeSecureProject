import urllib.request
from bs4 import BeautifulSoup
import sys
import time


def Alarm(state):
	if state=="On":
		# do something
	else if state=="Off":
		# do something

url="http://140.113.123.151:80/FP/detect.html"
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'} # Fake web browser info
ButtonState=0

try:
	while True :
		
		while not(ButtonState):
			# read Button here
		
	
		# get website data
		req = urllib.request.Request(url = url,headers=headers)
		page = urllib.request.urlopen(req)
		contentBytes = page.read()

		# find tag h1
		soup = BeautifulSoup(str(contentBytes), "html.parser")
		matches =  str(soup.find("h1"))

		# process the string we just got
		alarm = "On" if matches.count("Alarm")==1 else "Off"
		print(alarm)
		
		Alarm(state)
		sleep(0.1)


except KeyboardInterrupt:
	# GPIO cleanup here
	print("\nKeyboardInterrupt")




