#!/usr/bin/python
from Tkinter import *
from ttk import Treeview
import tkFont
from tkFileDialog import *
from datetime import datetime,date,timedelta
import tkMessageBox
import time
import re
import serial
import sqlite3
import serial.tools.list_ports
import os
import csv

def main():
	
	stk=STK()
				
	stk.t.focus_force()
	mainloop()				
	
class STK:
	def __init__(self):
		root = Tk()
		root.title("STK")
		root.protocol("WM_DELETE_WINDOW", self.on_closing)
		root.geometry("+100+100")
		
		img="""R0lGODlhgACAAPfhAAAAACm0cSm1cSu0cSq1cSu1cSq2cSu2cSm0cym1cyq1ciu1ciq0cyu0cyq1cyu1cym2cim2cyq2ciu2ciq2cyu2cyy2dC23dC23dS63dS+3dj
				C4djG4dzK4dzK5eDO5eDS5eTW5eja6eje6ezi7fDm7fDq7fTu7fTy8fjy8fz28fz69gD+9gEC9gUG9gUG+gkK+gkO+g0S/g0a/hUfAhkjAhkvBiEzBiU3Cik7Cik/C
				i1DDi1DDjFHDjFLDjVPEjVTEjlXEjlXFj1jFkVnGkVrGklvHk13HlF7HlF/IlV/IlmDIlmHJl2PJmGTJmGTKmWXKmWbKmmfLm2jLm2nLnGrMnWvMnW7Nn3DOoXHOoX
				LOonLPonTPo3XPpHbQpHfQpXfQpnjRpnvRqHzSqHzSqX3SqX7Tqn/TqoDTq4HTrILUrYPUrYTVroXVrojWsInWsYrXsovXs4zXs43YtI7YtI/YtZDZtZLZt5PauJTa
				uJXauZbbupfbupjcu5ncu5vdvZzdvp3dvp7ev5/ev57fv5/ewKDewKHfwaPfwqTgw6XgxKbgxKnixqrix6viyKziyK3jya7jya/kyrDky7Hky7LkzLPlzLPlzbTlzr
				Xmzrfmz7jn0Lnn0bzo077p1MDp1cLp1cHq1sLq18Pq18Tr2MXq2cXr2cbs2sfs2sjs28ns28rt3Mvt3Mvt3c7u38/u39Dv4NPu4tPw4tTw4tXw49bx5Nfx5djy5dny
				5try59vz59zz6N3z6N/z6d706d/06uD06+H16+L17OP17OT27eb17uf17uX27uf37+j38On48er48ev48uz48u358+759O/69fD69fH69vP79/T7+PX8+Pb8+ff8+v
				j8+vj9+/n9+/r9/Pv+/Pz+/f3+/f3+/v7//v///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
				AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAACAAIAAAAj+AAEIHEiwoMGDCBMqXMiwocOHECNKnEixosWLGDNq3Mixo8ePIEOKHEmypMmTKAU+kE
				CBQYWXMGNWaBAggoSUOC0eaCCzp8+eCxrkHJpwwoGfSJPKbPCA6FAFLpVKnVohggKnJiFQ3bp1AdaQBLiK3RrgK8cAY9NuPWD24gC1cLdSaCvxbdy7VK/SbRgBr9+p
				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"""
		
		self.icon= PhotoImage(data=img)
		root.call('wm', 'iconphoto', root._w, self.icon)
		
		#create status bar at the bottom of the window
		statusbar=Frame(root,borderwidth=1, relief=SUNKEN)
		statusbar.pack(side=BOTTOM, fill=X)
		statusicon = Canvas(statusbar,height=20, width=20)
		statusicon.create_oval(3, 3, 17, 17, outline="black", fill="red")
		statusicon.pack(side=LEFT)
		statustext = Label(statusbar, text="Not Connected", anchor=W)
		statustext.pack(side=LEFT)
		timetext=Label(statusbar, anchor=E)
		timetext.pack(side=RIGHT)
		
		#main text box w/ scrollbar
		t = Text(root, height=40, width=80)
		t.pack()
		scroll = Scrollbar(root)
		scroll.pack(side=RIGHT, fill=Y)
		t.pack(side=LEFT, fill=BOTH, expand=True)
		scroll.config(command=t.yview)
		t.configure(yscrollcommand=scroll.set)
		t.config(state=DISABLED)
		
		###Set up Menus###
		menubar = Menu(root)
		root.config(menu=menubar)
		
		#file menu
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Open Log File", command=self.open_logfile)
		filemenu.add_command(label="Collect Reports from Log File", command=self.process_logfile)
		filemenu.add_separator()
		filemenu.add_command(label="Clear Window", command=self.clear_window)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=self.exit)
		menubar.add_cascade(label="File", menu=filemenu)
		
		#Connect menu.  Filled in from update_ports
		connectmenu = Menu(menubar, tearoff=0)
		menubar.add_cascade(label="Connect", menu=connectmenu)
		
		#Analyze menu
		analyzemenu = Menu(menubar, tearoff=0)
		menubar.add_cascade(label="Analyze", menu=analyzemenu)
		analyzemenu.add_command(label="Data Numerical", command=self.analyze_numerical)
		
		#Setup menu
		setupmenu = Menu(menubar, tearoff=0)
		menubar.add_cascade(label="Setup", menu=setupmenu)
		setupmenu.add_command(label="Auto Report Config", command=self.report_config_auto)
		setupmenu.add_command(label="Manual Report Config", command=self.report_config_manual)
		
		#update window after all setup and complete and make that the minimum size
		root.update_idletasks()
		root.minsize(root.winfo_width(),root.winfo_height())
		root.geometry("%dx%d+%d+%d"%(root.winfo_width(),root.winfo_height(),100,100))
		
		###Initialize Variables###
		
		#assign Tk variables used externally
		self.root=root
		self.t=t
		self.filemenu=filemenu
		self.menubar=menubar
		self.statustext=statustext
		self.statusicon=statusicon
		self.connectmenu=connectmenu
		self.timetext=timetext
		
		#initialize filenames
		self.path=os.path.dirname(os.path.realpath(__file__))
		self.processfile=self.path+"/"+"process.log"
		self.errorfile=self.path+"/"+"error.log"
		self.dbfile=self.path+"/"+"stk.db"
		
		crashfile=self.path+"/"+"crash.log"
		sys.stderr = open(crashfile, 'a')
		
		if not os.path.isfile(self.dbfile):
			self.create_database()
		
		#initialize configuration.  Later this will probably come from config file
		self.config=Config(self.icon,self.dbfile)
		
		#initialize other variables
		self.report={}
		self.stringbuffer=""
		self.sublabels=[]
		self.logfile=None
		self.serial=None
		self.serialalarm=None
		self.learning=False
		
		#config
		self.maxrows=500
		#add serial parameters here
				
		###Startup Functions###
		self.update_ports()
		self.update_time()
	
	#function run when window closed from any way except File->Exit
	#uncomment one line and comment the other.  For testing its easier if the X closes the program
	def on_closing(self):
		if True:
			if hasattr(self, 'an_win') and self.an_win.winfo_exists():
				self.an_win.destroy()
				del self.an_win
			if hasattr(self, 'rc_win') and self.rc_win.winfo_exists():
				self.rc_win.destroy()
				del self.rc_win
			self.root.iconify()
			return
		self.exit()
	
	#function which runs on exit which makes sure everything is closed out.
	def exit(self):
		if not tkMessageBox.askyesno("Exit","Are you sure you would like to exit?"):
			return
		try:
			self.db.close()
		except:
			pass
		try:
			self.serial.close()
		except:
			pass
		try:
			self.logfile.close()
		except:
			pass
		self.root.destroy()
	
	#function to clear out the text display widget.
	def clear_window(self):
		self.t.configure(state=NORMAL)
		self.t.delete('1.0',END)
		self.t.configure(state=DISABLED	)
	
	#function which gets current list of serial ports and makes connect menu show them
	def update_ports(self):
		while self.connectmenu.index("end") is not None:
			self.connectmenu.delete(0)
		comports = sorted(serial.tools.list_ports.comports(), key=lambda x: x[0])
		for port,description,address in comports:
			self.connectmenu.add_command(label=port + " - " + description, command=lambda p=port: self.serial_connect(p))
		self.connectmenu.add_separator()
		self.connectmenu.add_command(label='Refresh Ports', command=self.update_ports)
	
	def update_time(self):
		"""Periodically called function run to update time in GUI"""
		timestr=datetime.now().strftime('%I:%M:%S %p')
		if timestr!=self.timetext['text']:
			self.timetext['text']=timestr
		self.timetext.after(20,self.update_time)
	
	#function to connect to a serial port and begin monitoring for reports
	def serial_connect(self,port):
		try:
			self.serial=serial.Serial(port, timeout=0)
		except serial.SerialException:
			tkMessageBox.showerror("Serial Error", "Error opening com port %s."%port)
			self.log_error("Error opening com port %s."%port)
			return
		self.serial.reset_input_buffer()
		
		self.log_process("Connected to %s" % (port,))
		self.menubar.entryconfigure(2, state=DISABLED)
		self.statusicon.itemconfigure(ALL, fill="green")
		self.statustext.config(text="Connected to port: %s at %s,%s,%s,%s"%(port,self.serial.baudrate,self.serial.bytesize,self.serial.parity,self.serial.stopbits))
		self.process_serial()
	
	#function to disconnect serial.  Done if there is a serial error.
	def serial_disconnect(self):
		self.serial.close()
		self.t.after_cancel(self.serialalarm)
		self.update_ports()
		self.menubar.entryconfigure(2, state=NORMAL)
		self.statusicon.itemconfigure(ALL, fill="red")
		self.statustext.config(text="Disconnected")
		
	#function to log timestamp and process string to process log file
	def log_process(self,message):
		processlog=open(self.processfile,"a")
		timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		logmessage = timestamp + " - " + message + "\n"
		processlog.write(logmessage)
		processlog.close()
	
	#function to log timestamp and error string to error log file
	def log_error(self,message):
		errorlog=open(self.errorfile,"a")
		timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		logmessage = timestamp + " - " + message + "\n"
		errorlog.write(logmessage)
		errorlog.close()	
	
	
	def analyze_numerical(self):
		"""Function to load the Analyze Numerical window"""
		if hasattr(self, 'an_win') and self.an_win.winfo_exists():
			self.an_win.deiconify()
			self.an_win.focus_force()
			self.an_win.lift()
			return
		self.an_win = Toplevel()
		DataNumerical(self.an_win,self.config)
		
	#function to open/close log file. One function to make tk binding easier
	def open_logfile(self):
		"""Function to open/close log file, depending on the current state"""
		if self.logfile:
			self.logfile.close()
			self.logfile=None
			self.filemenu.entryconfigure(0, label="Open Log File")
		else:
			self.logfile = asksaveasfilename(title='Select Output File',filetypes=[('Log File','*.log'),("All Files", "*.*"),],defaultextension = '.log')
			if not self.logfile:
				return
			#open logfile
			self.logfile=open(self.logfile,"wb")
			self.filemenu.entryconfigure(0, label="Close Log File")
	
	def report_config_auto(self):
		"""Function to learn report configuration from properly formatted log files."""
		tkMessageBox.showwarning("Select Valid Log File","When selecting a log file for learning it is vital to have only valid reports")
		self.learning=True
		self.process_logfile()
		self.learning=False
		
		
	def report_config_manual(self):
		"""Function to create gui to manually configure reports."""
		if hasattr(self, 'rc_win') and self.rc_win.winfo_exists():
			self.rc_win.deiconify()
			self.rc_win.focus_force()
			self.rc_win.lift()
			return
		self.rc_win = Toplevel()
		ReportConfig(self.rc_win,self.config)
	
	#function to process log file.  Can process multiple at the same time.  Used for both configuration and importing of reports
	def process_logfile(self):
		logfilenames = askopenfilenames(title='Select Log File',filetypes=[('Log File','*.log'),("All Files", "*.*"),],defaultextension = '.log')
		if not logfilenames:
			return
		oldstatus=self.statustext['text']
		oldcolor=self.statusicon.itemcget(ALL,"fill")
		self.statusicon.itemconfigure(ALL, fill="yellow")
		if self.serialalarm:
			self.t.after_cancel(self.serialalarm)
		temp_report=self.report.copy()
		for logfilename in logfilenames:
			self.log_process("Beginning import of file %s"%logfilename)
			self.statustext['text']="Importing log file %s"%logfilename
			self.root.update_idletasks()
			with open(logfilename,'rU') as file:
				for line in file:
					self.process_line(line)
			self.log_process("Import of file %s complete"%logfilename)
		
		self.report = temp_report.copy()
		if self.serialalarm:
			self.serialalarm = self.t.after(10,self.process_serial)
		self.statustext['text']=oldstatus
		self.statusicon.itemconfigure(ALL, fill=oldcolor)
		tkMessageBox.showinfo("Complete","Log File Import Complete")
		
	#function to process serial port.  Reads and combines bytes into lines for processing/
	#also logs data to logfile byte for byte
	def process_serial(self):
		try:
			while self.serial.inWaiting()>0:
					inbyte=self.serial.read()
					if self.logfile:
						self.logfile.write(inbyte)
					self.stringbuffer+=inbyte
					if self.stringbuffer[-2:]=='\r\n':
						line=self.stringbuffer
						self.stringbuffer=""
						self.root.update_idletasks()
						self.process_line(line)
						
			self.serialalarm = self.t.after(10,self.process_serial)
		except serial.SerialException:
			self.log_error("Error reading from serial port. Disconnecting.")
			self.serial_disconnect()
		
	#functions to display a line of text at the bottom of the text window and manage max size
	def display_line(self,line):
		line=re.sub(r'(\r|\f)',r'',line) #remove \r and \f for displaying (linux)
		self.t.config(state=NORMAL)
		self.t.insert(END,line)
		self.t.see(END)
		#remove extra rows so we are within the max.
		while int(eval(self.t.index('end-1c')))>self.maxrows:
			self.t.delete('1.0','2.0')
		self.t.config(state=DISABLED)
	
	#function to process a line of text from process_serial or process_logfile
	#creates and manages reports (self.report) and when a report is complete runs process_report
	def process_line(self,line,quick=False):
		if not quick:
			self.display_line(line)
		
		#report is empty.  means a new report is ready to begin.  Checks for line 1 of report header
		if not 'name' in self.report:
			m=re.search(r"(?:\bSAMPLE CHECK REPORT\b|\bSTANDARDIZE REPORT\b|\bCALIBRATE SAMPLE REPORT\b)",line)
			if m:
				self.report['name']=m.group(0)
		
		#checks for line 2 of report header.
		elif not 'machine' in self.report:
			m=re.split(r"\s{2,}",line.strip())
			if m:
				self.report['machine']=m[1]
				self.report['location']=m[2]
				self.report['timestamp']=datetime.strptime(m[3],"%Y-%m-%d %H:%M")
			else:
				self.report={}
		
		#checks for line 3 of report header
		elif not 'gradecode' in self.report:
			m=re.search(r"PRODUCT\s*([0-9]{7})\s*([a-zA-Z0-9_ ]+)",line)
			if m:
				self.report['gradecode']=m.group(1)
				self.report['gradename']=m.group(2).strip()
				self.report['data']=[]
		
		#means end of report.  Process previous report and clear out data
		elif re.search(r"END OF REPORT",line):
			error=False
			for sensor in self.report['data']:
				#print sensor['sensor'],
				test = sensor['sensor']
				#print len(self.report['data'][-1]['labels'])-len(self.report['data'][-1]['values'])
				for i,label in enumerate(sensor['labels']):
					try:
						#print "%s: %g" % (label,float(sensor['values'][i]))
						test = "%s: %g" % (label,float(sensor['values'][i]))
					except IndexError:
						error=True
						self.log_error(" Index Error: %s. Labels: %d, Values %d" % (label,len(sensor['labels']),len(sensor['values'])))
				if error:
					self.log_error("Index Error in report %s %s. Report discarded." % (self.report['name'],self.report['location']))
					self.report={}
					return
			self.process_report()
			self.report={}
			self.root.update()
		
		#if there's a report header, but it's not after an "END OF REPORT".  Means previous was partial.  Start over.
		elif re.search(r"(?:SAMPLE CHECK REPORT|STANDARDIZE REPORT|CALIBRATE SAMPLE REPORT|REEL REPORT)",line):
			self.log_error("Unexpected Report End")
			self.report={}
			m=re.search(r"(?:SAMPLE CHECK REPORT|STANDARDIZE REPORT|CALIBRATE SAMPLE REPORT|REEL REPORT|)",line)
			if m:
				self.report['name']=m.group(0)
		
		#word at beginning of line that is not report header or end of report.  Means it's a 'sensor' header
		elif re.search(r"^[a-zA-Z]+",line):
			#if data is empty or there are values than it can't be the first subreport
			if (not self.report['data']) or (len(self.report['data'][-1]['values']))>0:
				self.report['data'].append({'sensor': line.strip()})
				self.report['data'][-1]['labels']=[]
				self.report['data'][-1]['values']=[]
			else: # first sub report
				self.sublabels=list(self.report['data'][-1]['labels'])
				if line.strip() == 'IR1' or True:
					for i,label in enumerate(self.sublabels):
						self.report['data'][-1]['labels'][i]=line.strip() + "_" + label 
				
		#all numbers/characters used in numbers.  Means it's values
		elif re.search(r"^[0-9Ee\+\-\.]+[0-9Ee\+\-\.\s]+$",line.strip()):
			#check if there are no labels.  Means this is a 2nd more greater subreport
			if not self.report['data'][-1]['labels']:
				#delete the recently created sensor.  Get it to use it's 'sensor' name as new sub
				sub=self.report['data'].pop(-1)
				newsub = sub['sensor']
				
				#add same labels again with new sub to the newly current sensor
				for label in self.sublabels:
					self.report['data'][-1]['labels'].append(newsub + "_" + label)
			
			values=re.split(r"\s{2,}",line.strip())
			self.report['data'][-1]['values'].extend(values)
			
			#make sure there are not more values than labels.  Used in case of subreports
			if len(self.report['data'][-1]['values'])>len(self.report['data'][-1]['labels']):
				del(self.report['data'][-1]['values'][len(self.report['data'][-1]['labels']):len(self.report['data'][-1]['values'])])
		
		#almost an else.  If nothing else applies but it's not blank it's labels.
		elif re.search(r"\S+",line):
			self.sublabels=[] #if there are labels coming, no way you're in a subreport
			labels=[line[0:14],line[14:28],line[28:42],line[42:56],line[56:70]]
			labels=map(str.strip,labels)
			labels=filter(None, labels)
			self.report['data'][-1]['labels'].extend(labels)
		
		#not needed, but this SHOULD only be blank lines.
		else:
			pass

	#function to process a complete report. Included error checking against database
	#can function in learning==True which will update Report Type, Locations, Sensors and Labels but not reports, report data and grade.
	#or can function in learning==False where is logs reports, report data and grades if configuration exists.  This should help catch malformed reports.
	def process_report(self):
		self.db = sqlite3.connect(self.dbfile)
		c=self.db.cursor()
		
		#check/add reportType exists
		c.execute('''SELECT reportTypeID FROM reportTypes WHERE ReportTypeName = ?''',(self.report['name'],))
		result=c.fetchone()
		if result:
			ReportTypeID=result[0]
		elif self.learning:
			c.execute('''INSERT INTO reportTypes VALUES (NULL,?)''', (self.report['name'],))
			ReportTypeID=c.lastrowid
			self.log_process("New report type %s added to database"%self.report['name'])
		elif not result:
			self.log_error("Report Type Missing from Database: %s" % self.report['name'])
			self.db.commit()
			return
		
		#check/add location exists
		c.execute('''SELECT LocationID FROM locations WHERE LocationName = ?''',(self.report['location'],))
		result=c.fetchone()
		if result:
			LocationID=result[0]
		elif self.learning:
			c.execute('''INSERT INTO locations VALUES (NULL,?)''', (self.report['location'],))
			LocationID=c.lastrowid
			self.log_process("New location %s added to database"%self.report['location'])
		else:
			self.log_error("Location Missing from Database: %s" % self.report['location'])
			self.db.commit()
			return
		
		#check if grade exists.  This is always "learning", except when "learning"... (doesn't add grades when configuring)
		if not self.learning:
			c.execute('''SELECT GradeID,GradeName FROM grades WHERE GradeCode = ?''',(self.report['gradecode'],))
			result=c.fetchone()
			if result:
				GradeID=result[0]
				if result[1]!=self.report['gradename']:
					c.execute('''UPDATE grades SET GradeName=? WHERE GradeID = ?''',(self.report['gradename'],GradeID))
					self.log_process("Updated grade %s name from %s to %s"%(self.report['gradecode'],result[1],self.report['gradename']))
			else:
				c.execute('''INSERT INTO grades VALUES (NULL,?,?)''', (self.report['gradecode'],self.report['gradename']))
				GradeID=c.lastrowid
				self.log_process("Added missing grade %s %s"%(self.report['gradecode'],self.report['gradename']))
		
		#insert report here.  Do not do if learning
		if not self.learning:
			c.execute('''INSERT INTO reports VALUES (NULL,?,?,?,?)''', (self.report['timestamp'],ReportTypeID,LocationID,GradeID))
			ReportID=c.lastrowid
			self.log_process("%s: %s, %s, %s, %s" % (self.report['name'],self.report['machine'],self.report['location'],self.report['timestamp'].strftime('%Y-%m-%d %H:%M'),self.report['gradecode']))
		
		#check/add sensor(s) and label(s) exists
		for sensor in self.report['data']:
			c.execute('''SELECT SensorID FROM sensors WHERE SensorName = ? and LocationID = ?''',(sensor['sensor'],LocationID))
			result=c.fetchone()
			if result:
				SensorID = result[0]
			elif self.learning:
				c.execute('''INSERT INTO sensors VALUES (NULL,?,?)''', (sensor['sensor'],LocationID))
				SensorID=c.lastrowid
				self.log_process("New sensor %s at location %s added to database"%(sensor['sensor'],self.report['location']))
			else:
				self.db.commit()
				self.log_error("Sensor %s missing from Database at location %s" % (sensor['sensor'],self.report['location']))
				return
			for i,label in enumerate(sensor['labels']):
				c.execute('''SELECT LabelID FROM labels WHERE LabelName = ? and SensorID = ?''',(label,SensorID))
				result=c.fetchone()
				if result:
					LabelID = result[0]
				elif self.learning:
					c.execute('''INSERT INTO labels VALUES (NULL,?,?)''', (label,SensorID))
					LabelID=c.lastrowid
					self.log_process("New label %s for sensor %s at location %s added to database"%(label,sensor['sensor'],self.report['location']))
				else:
					self.db.commit()
					self.log_error("Label %s missing from Database in location %s, sensor %s" % (label,self.report['location'],sensor['sensor']))
					return
				if not self.learning:
					c.execute('''INSERT INTO reportData VALUES (?,?,?)''',(ReportID,LabelID,sensor['values'][i]))
				
		#commit and close every time. Most of the time we process 1-2 reports at a time.
		self.db.commit()
		self.db.close()
		
	def create_database(self):
		"""Method to create a blank database in the correct format.  Run if database does not exists"""
		
		tkMessageBox.showinfo("Database not found","Database not found\nCreating blank database at %s"%self.dbfile)
		self.db = sqlite3.connect(self.dbfile)
		c=self.db.cursor()		
		c.execute("""CREATE TABLE 'grades' ( `GradeID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `GradeCode` INTEGER NOT NULL, `GradeName` TEXT NOT NULL )""")
		c.execute("""CREATE TABLE 'labels' ( `LabelID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `LabelName` TEXT NOT NULL, `SensorID` INTEGER NOT NULL )""")
		c.execute("""CREATE TABLE 'locations' ( `LocationID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `LocationName` TEXT NOT NULL )""")
		c.execute("""CREATE TABLE 'reportData' ( `ReportDataID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,`ReportID` INTEGER NOT NULL, `LabelID` INTEGER NOT NULL, `Value` NUMERIC NOT NULL )""")
		c.execute("""CREATE TABLE 'reportTypes' ( `ReportTypeID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `ReportTypeName` TEXT NOT NULL )""")
		c.execute("""CREATE TABLE 'reports' ( `ReportID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `Timestamp` TEXT NOT NULL, `ReportTypeID` INTEGER NOT NULL, `LocationID` INTEGER NOT NULL, `GradeID` INTEGER NOT NULL )""")
		c.execute("""CREATE TABLE 'sensors' ( `SensorID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `SensorName` TEXT NOT NULL, `LocationID` INTEGER NOT NULL )""")
		c.execute("""CREATE VIEW v_reportData AS SELECT reports.ReportID as ReportID, timestamp, reports.ReportTypeID as ReportTypeID, ReportTypeName, reports.LocationID as LocationID, LocationName, reports.GradeID as GradeID, GradeCode, GradeName, sensors.SensorID as SensorID, sensors.SensorName as SensorName, labels.LabelID as LabelID, labels.LabelName as LabelName, Value, reportData.ReportDataID as ReportDataID FROM reports INNER JOIN reportTypes ON reportTypes.ReportTypeID = reports.ReportTypeID INNER JOIN locations ON locations.LocationID = reports.LocationID INNER JOIN grades ON grades.GradeID = reports.GradeID INNER JOIN reportData ON reportData.ReportID = reports.reportID INNER JOIN labels ON labels.LabelID = reportData.LabelID INNER JOIN sensors ON sensors.SensorID = labels.SensorID""")
		c.execute("""CREATE VIEW v_reports AS SELECT ReportID, timestamp, reports.ReportTypeID as ReportTypeID, ReportTypeName, reports.LocationID as LocationID, LocationName, reports.GradeID as GradeID, GradeCode GradeName FROM reports INNER JOIN reportTypes ON reportTypes.ReportTypeID = reports.ReportTypeID INNER JOIN locations ON locations.LocationID = reports.LocationID INNER JOIN grades ON grades.GradeID = reports.GradeID""")
		c.execute("""CREATE TABLE 'CONFIG' ( `MachineName` TEXT NOT NULL)""")
		#c.execute("""*""")
		self.db.commit()
		self.db.close()
		
		

class ReportConfig:
	def __init__(self,parent,config):
		self.dbfile=config.dbfile
		self.icon=config.icon
		self.win=parent
		
		self.win.tk.call('wm', 'iconphoto', self.win._w, self.icon)
		self.win.geometry("+100+100")
		self.win.geometry("800x600")
		self.win.minsize(800,600)
		
		#split window into two frames
		report_frame=Frame(self.win, width=270)
		report_frame.pack(fill=Y, side=LEFT)
		report_frame.grid_propagate(0)
		report_frame.columnconfigure(0, weight = 1)
		report_frame.columnconfigure(1, weight = 0)
		report_frame.rowconfigure(0, weight = 1)
		report_frame.rowconfigure(1, weight = 0)
		report_frame.rowconfigure(2, weight = 0)
		
		data_frame=LabelFrame(self.win,text="Report Configuration")
		data_frame.pack(fill=BOTH, side=RIGHT, expand=True)
		
		rt_lframe=LabelFrame(report_frame,text="Machine Structure")
		rt_lframe.grid(column=0,row=0,sticky=W+E+N+S,padx=2)
		rt_lframe.columnconfigure(0, weight = 1)
		rt_lframe.columnconfigure(1, weight = 1)
		rt_lframe.rowconfigure(0, weight = 1)
		rt_lframe.rowconfigure(1, weight = 0)
		structure_add_button=Button(rt_lframe,text="Add Item",width=1,state=DISABLED)
		structure_add_button.grid(column=0,row=1,sticky=W+E+N+S,padx=2,pady=2)
		structure_remove_button=Button(rt_lframe,text="Remove Item",width=1,state=DISABLED)
		structure_remove_button.grid(column=1,row=1,sticky=W+E+N+S,padx=2,pady=2)
		report_tree=StructureTree(rt_lframe,config.dbfile)
		report_tree.grid(column=0,row=0,columnspan=2,sticky=W+E+N+S,padx=2,pady=2)
		report_tree['show']='tree'
		
		
		tt_lframe=LabelFrame(report_frame,text="Report Types")
		tt_lframe.grid(column=0,row=1,sticky=W+E+N+S,padx=2)
		tt_lframe.columnconfigure(0, weight = 1)
		tt_lframe.columnconfigure(1, weight = 1)
		tt_lframe.rowconfigure(0, weight = 1)
		tt_lframe.rowconfigure(1, weight = 0)
		type_add_button=Button(tt_lframe,text="Add Item",width=1,state=DISABLED)
		type_add_button.grid(column=0,row=1,sticky=W+E+N+S,padx=2,pady=2)
		type_remove_button=Button(tt_lframe,text="Remove Item",width=1,state=DISABLED)
		type_remove_button.grid(column=1,row=1,sticky=W+E+N+S,padx=2,pady=2)
		type_tree=ReportTypeTree(tt_lframe,self.dbfile)
		type_tree['height']=5
		type_tree.grid(column=0,row=0,columnspan=2,sticky=W+E+N+S,padx=2,pady=2)
		type_tree['show']='tree'
		
		report_tree.bind("<<TreeviewSelect>>",type_tree.update_reports,add="+")
		report_tree.bind("<<TreeviewSelect>>",self.button_states,add="+")
		
		
		self.source = IntVar(value=0)
		rs_lframe=LabelFrame(report_frame,text="Report Source Type")
		rs_lframe.grid(column=0,row=2,sticky=W+E+N+S,padx=2)
		rs_lframe.columnconfigure(0, weight = 1)
		rs_lframe.columnconfigure(1, weight = 1)
		rs_lframe.rowconfigure(0, weight = 1)
		rs_lframe.rowconfigure(1, weight = 0)
		rs_lframe.rowconfigure(2, weight = 0)
		Radiobutton(rs_lframe, text="Serial Datalogger", variable=self.source, value=0,anchor=W).grid(row=0,column=0,columnspan=2,sticky=W+E+N+S)
		Radiobutton(rs_lframe, text="OPC Datalogger", variable=self.source, value=1,anchor=W).grid(row=1,column=0,columnspan=2,sticky=W+E+N+S)
		Button(rs_lframe,text="Create New Report",command=self.create_report).grid(column=0,row=2,columnspan=2,sticky=W+E+N+S,padx=2,pady=2)
		
		
		##Self Declarations##
		self.type_tree=type_tree
		self.type_add_button=type_add_button
		self.type_remove_button=type_remove_button
		self.structure_add_button=structure_add_button
		self.structure_remove_button=structure_remove_button		
	
	def button_states(self,event):
		"""Method that should be bound to run everytime ReportTypeTree is updated.  Sets the states of all the add/remove item buttons."""
		#update type_tree modification button states
		if self.type_tree.get_children(""):
			self.type_add_button['state']='active'
			self.type_remove_button['state']='active'
		else:
			self.type_add_button['state']='disabled'
			self.type_remove_button['state']='disabled'
		
		#update type_tree modification button states
		call_widget=event.widget
		item=call_widget.selection()[0]
		if call_widget.tag_has("Sensor",item):
			self.structure_add_button['state']=DISABLED
			self.structure_remove_button['state']=ACTIVE
		elif call_widget.tag_has("Machine",item): #doesn't exists yet
			self.structure_add_button['state']=ACTIVE
			self.structure_remove_button['state']=DISABLED		
		elif call_widget.tag_has("Location",item):
			if call_widget.get_children(item):
				self.structure_add_button['state']=ACTIVE
				self.structure_remove_button['state']=DISABLED
			else:
				self.structure_add_button['state']=ACTIVE
				self.structure_remove_button['state']=ACTIVE				
		else:	#no selection.  should never happen
			self.structure_add_button['state']=DISABLED
			self.structure_remove_button['state']=DISABLE
	
	def create_report(self):
		"""Placeholder for funtion which will generate the GUI for creating a new """
		print self.source.get()
		
class DataNumerical:
	def __init__(self,parent,config):
		self.dbfile=config.dbfile
		self.icon=config.icon
		self.an_win=parent
		
		self.an_win.tk.call('wm', 'iconphoto', self.an_win._w, self.icon)
		self.an_win.geometry("+100+100")
		self.an_win.geometry("800x600")
		self.an_win.minsize(800,600)
		
		#split window into two frames
		report_frame=Frame(self.an_win, width=225)
		report_frame.pack(fill=Y, side=LEFT)
		report_frame.pack_propagate(0)
		data_frame=Frame(self.an_win)
		data_frame.pack(fill=BOTH, side=RIGHT, expand=True)
		
		#data frame
		data_tree=Treeview(data_frame,selectmode="browse", show="tree")
		hscroll = Scrollbar(data_frame,orient=HORIZONTAL)
		hscroll.pack(side=BOTTOM, fill=X)
		vscroll = Scrollbar(data_frame)
		vscroll.pack(side=RIGHT, fill=Y)
		data_tree.pack(side=LEFT,fill=BOTH,anchor=N,expand=True)
		vscroll.config(command=data_tree.yview)
		data_tree.configure(yscrollcommand=vscroll.set)
		hscroll.config(command=data_tree.xview)
		data_tree.configure(xscrollcommand=hscroll.set)
		
		
		
		#report frame
		csv_button=Button(report_frame, text="Save as CSV", command=self.save_csv,state='disabled')#, relief="ridge"
		csv_button.pack(side=BOTTOM, fill=X)
		generate_button=Button(report_frame, text="Generate Report", command=self.generate_report,state='disabled')#, relief="ridge"
		generate_button.pack(side=BOTTOM, fill=X)
		
		##variable##
		self.filter_select = IntVar()
		self.filter_start = StringVar()
		self.filter_end = StringVar()
		
		filter_frame=Frame(report_frame,width=225,height=200, relief="sunken", borderwidth=1,bg="white")
		filter_frame.pack(side=BOTTOM, fill=X)
		filter_frame.pack_propagate(0)
		#move code starting here to new class
		filter_frame.columnconfigure(0, weight = 1)
		filter_frame.columnconfigure(1, weight = 1)
		Label(filter_frame,text="Filter",justify=LEFT).grid(row=0,column=0,columnspan=2,sticky=W+E+N+S)
		Radiobutton(filter_frame, text="Last 5 days", variable=self.filter_select, value=0,bg="white",command=self.change_filter).grid(row=1,column=0,sticky=W)
		Radiobutton(filter_frame, text="One Week", variable=self.filter_select, value=1,bg="white",command=self.change_filter).grid(row=1,column=1,sticky=W)
		Radiobutton(filter_frame, text="One Month", variable=self.filter_select, value=2,bg="white",command=self.change_filter).grid(row=2,column=0,sticky=W)
		Radiobutton(filter_frame, text="One Year", variable=self.filter_select, value=3,bg="white",command=self.change_filter).grid(row=2,column=1,sticky=W)
		Radiobutton(filter_frame, text="All Data", variable=self.filter_select, value=4,bg="white",command=self.change_filter).grid(row=3,column=0,sticky=W)
		Radiobutton(filter_frame, text="Custom Time", variable=self.filter_select, value=5,bg="white",command=self.change_filter).grid(row=3,column=1,sticky=W)
		self.filter_select.set(0)
		self.filter_start.set((date.today()-timedelta(days=5)).strftime("%Y-%m-%d"))
		self.filter_end.set(date.today().strftime("%Y-%m-%d"))
		Label(filter_frame, text="Start",bg="white").grid(row=4,column=0)
		Label(filter_frame, text="End",bg="white").grid(row=4,column=1)
		start_entry=Entry(filter_frame, textvariable=self.filter_start,bg="white",state='disabled',justify='center')
		start_entry.grid(row=5,column=0)
		end_entry=Entry(filter_frame, textvariable=self.filter_end,bg="white",state='disabled',justify='center')
		end_entry.grid(row=5,column=1)
		#move code ending here to new class
		
		type_tree=ReportTypeTree(report_frame,self.dbfile)
		type_tree.config(height=3)
		type_tree.column("#0", minwidth=223,width=223,stretch=False)
		type_tree.pack(side=BOTTOM,fill=X,anchor=S)
		type_tree.heading("#0",text="Select Report Type")
		
		report_tree=StructureTree(report_frame,self.dbfile)
		report_tree.column("#0", minwidth=223,width=223,stretch=False)
		report_tree.pack(side=BOTTOM,fill=Y,expand=True, anchor=S)
		report_tree.bind("<<TreeviewSelect>>",type_tree.update_reports,add="+")
		report_tree.bind("<<TreeviewSelect>>",lambda event: self.generate_button_state(),add="+")
		report_tree.heading("#0",text="Select Sensor")

		self.report_tree=report_tree
		self.type_tree=type_tree
		self.data_tree=data_tree
		self.generate_button=generate_button
		self.csv_button=csv_button
		self.start_entry=start_entry
		self.end_entry=end_entry
		
		
	#function called when radio buttons change.  Will make custom dates disabled/normal
	def change_filter(self):
		if self.filter_select.get()==5:
			self.start_entry.config(state='normal')
			self.end_entry.config(state='normal')
		else:
			self.start_entry.config(state='disabled')
			self.end_entry.config(state='disabled')
	
	def generate_button_state(self):
		if self.type_tree.get_children(""):
			self.generate_button['state']='active'
		else:
			self.generate_button['state']='disabled'
		
	def generate_report(self):
		"""Function to get report data from database and populate self.data_tree with results."""
		#clear out data_tree
		self.data_tree.delete(*self.data_tree.get_children())
		
		#should never happen now, but if sensor or type are not selected, don't do anything
		if not self.report_tree.selection() or not self.type_tree.selection():
			self.data_tree['show']='tree'
			return
		
		#check what filter is selected and calculate end date and duration to subtract in sql statement
		filter=self.filter_select.get()
		if filter==0:
			enddate=date.today()
			duration='-5 days'
		elif filter==1:
			enddate=date.today()
			duration='-1 week'
		elif filter==2:
			enddate=date.today()
			duration='-1 month'
		elif filter==3:
			enddate=date.today()
			duration='-1 year'
		elif filter==4:
			enddate=date.today()
			duration='-10000 years'
		elif filter==5:
			try:
				enddate=datetime.strptime(self.filter_end.get().strip(),"%Y-%m-%d")
			except ValueError:
				tkMessageBox.showerror("Invalid Date","Invalid End Date\nPlease select valid date using format YYYY-MM-DD", parent=self.an_win)
				return
			try:
				startdate=datetime.strptime(self.filter_start.get().strip(),"%Y-%m-%d")
			except ValueError:
				tkMessageBox.showerror("Invalid Date","Invalid Start Date\nPlease select valid date using format YYYY-MM-DD", parent=self.an_win)
				return
			days=enddate-startdate
			if days.days<1:
				tkMessageBox.showerror("Invalid Dates","End date must be after start date.", parent=self.an_win)
				return
			duration="-%s days"%days.days
		
		
		self.db = sqlite3.connect(self.dbfile)
		c=self.db.cursor()
		
		#get selected SensorID from tree id
		sensor=self.report_tree.selection()[0]
		SensorID=sensor.split("_")[1]
		
		#get selected sensor LocationID from tree id of parent
		LocationID=self.report_tree.parent(sensor).split("_")[1]
		
		#get ReportTypeID from  tree
		rtype=self.type_tree.selection()[0]
		ReportTypeID=rtype.split("_")[1]
		
		
		c.execute("""SELECT DISTINCT LabelName,LabelID from v_reportData WHERE LocationID=? and SensorID=? and ReportTypeID=? and timestamp>=date('now',?) and timestamp<=? ORDER BY reportDataID""",(LocationID,SensorID,ReportTypeID,duration,enddate)) 
		results=c.fetchall()
		if not results:
			self.data_tree['show']='tree'
			self.csv_button.config(state='disabled')
			return
		self.csv_button.config(state='active')
		self.data_tree['show']='tree headings'
		LabelNames,LabelIDs=zip(*results)
		LabelCount=len(LabelNames)
		self.data_tree["columns"]=LabelNames
		self.data_tree.column("#0",width=160)
		self.data_tree.heading("#0",text="TIMESTAMP")
		for LabelName in LabelNames:
			w=int(tkFont.nametofont('TkHeadingFont').measure(LabelName)*1.5)
			w=max(w,75)
			self.data_tree.column(LabelName,width=w)
			self.data_tree.heading(LabelName,text=LabelName)
		
		c.execute("""SELECT DISTINCT ReportID, timestamp from v_reportData WHERE LocationID=? and SensorID=? and ReportTypeID=? and timestamp>=date('now',?) and timestamp<=?""",(LocationID,SensorID,ReportTypeID,duration,enddate))
		for ReportID,timestamp in c.fetchall():
			c1=self.db.cursor()
			c1.execute("""SELECT DISTINCT LabelName,Value,LabelID from v_reportData WHERE ReportID=? and SensorID=?""",(ReportID,SensorID))
			values=[""] * LabelCount
			for result in c1.fetchall():
				i=LabelIDs.index(result[2])
				values[i]=result[1]
			c1.close()
			self.data_tree.insert("",END,text=timestamp,values=values)
		c.close()
		self.db.close()
		
		
	def save_csv(self):
		if not self.data_tree.get_children():
			return
		timestamp = [self.data_tree.heading("#0",option="text")]
		outfile=asksaveasfilename(parent=self.an_win, title='Select Output File',filetypes=[('Comma Separated Values','*.csv'),("All Files", "*.*"),],defaultextension = '.csv')
		if not outfile:
			return
		with open(outfile, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			writer.writerow(timestamp + list(self.data_tree['columns']))
			#print ".".join(self.data_tree['columns'])
			for report in self.data_tree.get_children():
				timestamp=[]
				timestamp.append(self.data_tree.item(report)['text'])
				row=list(str(x) for x in self.data_tree.item(report)['values'])
				line=','.join(timestamp+row)
				writer.writerow(timestamp+row)
				#print line
	
class StructureTree(Treeview):
	
	def __init__(self,parent,dbfile):
		Treeview.__init__(self,parent,selectmode="browse")
		self.column("#0",stretch=True)
		self.dbfile=dbfile
		self.update_structure()
		
		
	def update_structure(self):
		self.delete(*self.get_children())
		self.db = sqlite3.connect(self.dbfile)
		c=self.db.cursor()
		c.execute("""SELECT DISTINCT LocationID,LocationName,ReportTypeID,ReportTypeName,SensorID,SensorName from v_reportData ORDER BY LocationName, ReportTypeName,SensorID""")
		for LocationID,LocationName,ReportTypeID,ReportTypeName,SensorID,SensorName in c.fetchall():
			LocationLabel="Location_%d"%LocationID
			ReportTypeLabel="Location_%d"%LocationID
			LocationLabel="Location_%d"%LocationID
			if not self.exists("Location_%d"%LocationID):
				self.insert("", END, "Location_%d"%LocationID, text=LocationName, tags="Location")
			if not self.exists("Sensor_%d"%SensorID):
				self.insert("Location_%d"%LocationID, END, "Sensor_%d"%SensorID, text=SensorName,tags="Sensor")		
		c.close()
		self.db.close()
		
class ReportTypeTree(Treeview):
	
	def __init__(self,parent,dbfile):
		Treeview.__init__(self,parent,selectmode="browse")
		self.dbfile=dbfile
		self.column("#0",stretch=True)
		
	def update_reports(self,event):
		"""Method to be bound to by StructureTree <<Selection>> event.  Populates the ReportTypeTree with available report types."""
		self.delete(*self.get_children())
		self.db = sqlite3.connect(self.dbfile)
		c=self.db.cursor()
		call_widget=event.widget
		item=call_widget.selection()[0]
		
		if call_widget.tag_has("Sensor",item):
			SensorID=item.split("_")[1]
			LocationID=call_widget.parent(item).split("_")[1]
			ReportTypeID=1
			c.execute("""SELECT DISTINCT ReportTypeID,ReportTypeName FROM v_reportData WHERE LocationID=? and SensorID=? ORDER BY ReportTypeName""",(LocationID,SensorID))
			results=c.fetchall()
			if not results:
				self.generate_button.config(state='disabled')
				c.close()
				self.db.close()
				return
			for ReportTypeID,ReportTypeName in results:
				self.insert("", END, "ReportType_%d"%ReportTypeID, text=ReportTypeName)
			self.selection_set(self.get_children("")[0])
		elif call_widget.tag_has("Location",item):
			pass
		else:
			tkMessageBox.showerror("Error","Invalid item tag",parent=call_widget)
		c.close()
		self.db.close()
	
		
class Config:
	def __init__(self,icon,dbfile):
		self.icon=icon
		self.dbfile=dbfile
		
if __name__ == "__main__":
	main()
