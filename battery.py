# 															Battery Management Script

#Features :
	#	Check the Battery Percentage and Ac Plug-In Status
	#	Alert if Battery Percentage is below 30 and Charger isn't Connected 
	#	Alert if Battery Percentage is above 80 and Charger is Connected
	#	Store the Datas in a file named "data.txt"
	# Sample Data : 
	#		Time : 08:10:02		Percent : 84	Charger : True
	#		Time : 08:20:01		Percent : 82	Charger : False

# Add .Exe file of this Script to Windows Task Scheduler (Run every 10 min) 

#Import Necessary Modules
import os, sys, time, psutil, tkinter, csv, pyttsx3, json
from tkinter import messagebox
from datetime import datetime

data = {}

def getData(window,max_e,min_e):
	global data
	max_val = int(max_e.get())
	min_val =int( min_e.get())
	data['min'] = min_val
	data['max'] = max_val
	window.withdraw()
	with open('data.json', 'w') as json_file:
		json.dump(data, json_file)
	exit()

try:
	with open('data.json') as f:
		data = json.load(f)
except:
	data = {}
	window= tkinter.Tk()
	max_e = tkinter.Entry(window,width = 10,justify = "center",background= "#EBEBEB")
	max_e.pack()
	min_e = tkinter.Entry(window,width = 10,justify = "center",background= "#EBEBEB")
	min_e.pack()
	submit = tkinter.Button(window, text ="Submit", command = lambda:getData(window,max_e,min_e))
	submit.pack()
	window.mainloop()
	
bat_percent = psutil.sensors_battery()[0]		# Battery Percentage
charger_stat = psutil.sensors_battery()[2]		# Charger Plugin Status
now = datetime.now()							# Current Time
current_time = now.strftime("%H:%M:%S")
path = r"data.csv"  # r"data.csv" - normal run // 	#os.path.dirname(sys.argv)[0] + r"\data.txt"-  (use while scheduling task)	# File to Store Data
# Storing Datas in a csv file
with open(path,'a') as file:
	writer = csv.writer(file)
	writer.writerow([current_time,bat_percent,charger_stat])

# Creating Tkinter Window (GUI) 
root= tkinter.Tk()
root.attributes("-topmost", True)   # To Bring Window to Front
root.withdraw()						# To Hide Main Root Window

# Creating Voice engine
engine = pyttsx3.init()

# Check the Comdition and Show Warning Messages 
if((bat_percent < data['min']) and not(charger_stat)):
	engine.say('Warning, Please Connect your charger')
	engine.runAndWait()					
	messagebox.showerror(f"Warning", "Charge below {}, Connect Your Charger".format(data['min']))
	
elif((bat_percent > data['max']) and charger_stat):	
	engine.say('Warning, Please Disconnect your charger')
	engine.runAndWait()
	messagebox.showerror(f"Warning", "Charge above {}, Disconnect Your Charger".format(data['max']))
