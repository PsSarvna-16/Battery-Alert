# 			   BATTERY MONITOR AND ALERT 												Battery Management Script

#Features :
	#	heck the Battery Percentage and Ac Plug-In Status
	#	Alert if Battery Percentage is below 30 and Charger isn't Connected 
	#	Alert if Battery Percentage is above 80 and Charger is Connected
	#	Store the Datas in a file named "data.txt"
	# Sample Data : 
	#		Time : 08:10:02		Percent : 84	Charger : True
	#		Time : 08:20:01		Percent : 82	Charger : False

# Add .Exe file of this Script to Windows Task Scheduler (Run every 10 min) 

#Import Necessary Modules
import os, sys, time, psutil, tkinter, csv,pyttsx3
from tkinter import messagebox
from datetime import datetime

bat_percent = 85 #psutil.sensors_battery()[0]		# Battery Percentage
charger_stat = psutil.sensors_battery()[2]		# Charger Plugin Status
now = datetime.now()							# Current Time
current_time = now.strftime("%H:%M:%S")
path = r"data.csv" 	#os.path.dirname(sys.argv)[0] + r"\data.txt"  (use while scheduling task)	# File to Store Data

# Storing Datas in a csv file
with open(path,'a') as file:
	writer = csv.writer(file)
	writer.writerow([current_time, bat_percent, charger_stat])

# Creating Tkinter Window (GUI) 
root= tkinter.Tk()
root.attributes("-topmost", True)   # To Bring Window to Front
root.withdraw()						# To Hide Main Root Window

# Create Voice engine
engine = pyttsx3.init()

# Check the Comdition and Show Warning Messages
if((bat_percent < 30) and not(charger_stat)):
	engine.say('Warning, Please Connect your charger')					
	messagebox.showerror("Warning", "Charge below 30, Connect Your Charger")
	engine.runAndWait()
	
elif((bat_percent > 80) and charger_stat):	
	engine.say('Warning, Please Disconnect your charger')
	engine.runAndWait()
	messagebox.showerror("Warning", "Charge above 80, DisConnect Your Charger")