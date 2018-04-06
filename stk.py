#!/usr/bin/python
#from Tkinter import *
import Tkinter
from ttk import Treeview, Combobox, Style
import tkFont
from tkFileDialog import *
from datetime import datetime,date,timedelta
import xml.etree.ElementTree as etree
from xml.dom import minidom

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates

import tkMessageBox
import time
import re
import serial #requires version 2.7/3.4
import sqlite3
import serial.tools.list_ports
import os
import csv
import sys

def main():
	
	stk=STK()
	try:
		stk.t.focus_force()
	except:
		return
	Tkinter.mainloop()
	
class STK:
	def __init__(self):
		root = Tkinter.Tk()
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
				Qvcm/EuYalPBBSkUXqwUAeKBCBhLRspW8IPJmJFOoJu5808CZnl6Hh0TAla0pFO/DJxzgurXFebivAz7td6Tomu/3mxSgm7dt0f+/l0y8vDalUMePa47Qki7zHUf9h
				j9+Mfc1Wsz6Ggg+/HtG73+H2eNEbt4uCngTr943i+eEXAz9m1/l5UVuOQp0r/bQRuiuBeZt59YSoSTS1zOVTRgXHqEE84KAFI0H1UfQLEgTMQ4SEZcCejH1RqLXFhB
				Bw6G80lc+Tmk2FYYCFPLYhhIlkSJw+AlUQFcZRHONyEQdsN9jOVRYjgzxMUbRFxZcIuDTRCGSIiMqTLkGHdFRBtVMzrIx18gTBMMYx1kM+Qld/UAkYBJfVKiKH+d4S
				ANi2VZ4jIWwGWBKUhulcOQ0lyAlwXWOLjGYkKG84g0DuIA1w7h5ElVJEOGo+hdRZTYymJShtNFJw6yAdcd4RDiEHRStbCNg9E4WAZelpRIjQb+hHEgZjgusOFgJ3DR
				Ek4pDqH50x8OvmKHg5HclcKpJSJBGBIO/lLBDQ5KE+NYMThojENbiTCNg1cs4aAvd9ERqR+E4eFgIxVYsIyDQqRlq4PYUgVHsxeA4I2DJsCFQYbheOLgLISl4mAXL7
				UajhxpnVJivFJpgIyDaLykazhUwEUFqizcC056eMnqoAsvieEgKWOV0E2JlzB0pVJgOOhMBy8l4iC5aoXi4CAVuOKgF34xGw4wMMng4DUbiPWFg8RwAwpDC0xlAS4O
				3gETFw6qotYM4DhYQwXmhkOJew46ElMwDirLFScO2sFJLAytqBQUQ58Q9NAZpAWIg6O8NIT+g8zUeZfA4fAMEyMO6sFVB4FKCkUxbU+lcDiJxGSBMg4GMVYHzzhYxU
				sYpBqOD3d5HM4LMW3h4KVbXRzOLxZc0AtDUwHh4DdFxoR2OG2M1XI4x0xbgSYOznGXz0DHlEKJf9yh/PLMN19iIC/dAbtUmDioSU9vOJjJWLA4WEdMYziYyl2ghiO2
				TEtGqv76DhbxEgwMLaHDDPTXb3+B7PZEBNJiyR7ONiqIyQsctA0QxAUVO+vJIdjHwBI1w08vYUgDI2W1nmxAGx/jiiMcRCaZ5MJBFVMLB7DhINLJ5Ad+SKEKV8hCFh
				IMJhKcYImm8BOdhQMLMTGYDI3Qk0I4KHL+ajmCg740mRge44hITOIRV+G3ngjCQYaACQe2JUNbNBEmT2jWpxz0CMxMLy5XcBAsYKI6GUasJx0gIZHUgsBwfMGLC8HL
				ChzEDZhVABIOKoRaRuGgNKRlhA6CARwV4hdhOIiHGYBG+9Tihlv5pBC3iKQkJ5m+cBCxiHHESyUcFIcKMMFByoDgWHDgoGnASnLOkCEXM8OQ5cRFDY5chIOglBYLPC
				wcR5AJD1TpIDBgxjELwdFdfOCgB1IuHEyIyyMc1AeZNDIcwviBNKdJTWkacDJHSoivuIKBajjoaOF4Rt3goqNwyEImagqHGoaTnIQ0DS+PY8Yq41KCb4QDHCj+gEkG
				qOEgGwwHPJm8yx4iRcO7dC8cXIBJpcKRjCvChmFxkcKQplG0uzQoHJKASfkmYZ2G+IUEQ7KEXxZKp5eswkFh6Ggr/aKLEl3BLxhAVDh6UIEPIAtkvwEmQyYUl0yF4w
				N/2YSDEJbFcPDiOOsJaFxEFo5TEKYMDkJFBe4WDkWo1KN4sYGDEvoXGBAQBBN76XAg4ko7PWMb8CHMLr6ZtW+QgJ0QcQ1ePBGKxSwwHLc851WxGq4NFSYKkfrDXhuy
				za0UIZ+F8cCsHOQEuEbEbXaSjClKpA0PDMcrEqHPvMQ3nBQ5RADt0UGJ8jCcDnlIPBYokfuIU5HC/gaP0xj+Z2086yjvaCEcuGKtRcIinnrmTrcWaQ8sbgBci7i2Nm
				ZwaGpoO5HzyPY1zJ0IZEWEmQJ05J3UnUyCOpLdQXbEN91dDGavE97CjKSs5VXLAEqS3iqVRK7tHYsDTrKy+E4lqSRRgH2p0s6TYHe/P4nuSI7b3rI4RSsAlglAncLb
				BFcgm1iB734hbBb0hne9jwGAham73QxPV0SyyTBBstthEROEwJ3Fr4kJImHvlHjFCGlwdPoLY6X+xrQ1jghPVTPeHE9EAcL0TAB67GOLPKDFhDlAiIvcEQWgOCkFEA
				CTUWIACCDgwzGhAAIasOQpe/nLYA6zmMdM5jKb+cwmCQgAOw=="""
		
		self.icon=Tkinter.PhotoImage(data=img)
		root.call('wm', 'iconphoto', root._w, self.icon)
		
		#color fix for XP
		style=Style()
		style.map('TCombobox', fieldbackground=[('readonly','white')])
		style.map('TCombobox', background=[('readonly','white')])
		
		#create status bar at the bottom of the window
		statusbar=Tkinter.Frame(root,borderwidth=1, relief='sunken')
		statusbar.pack(side='bottom', fill='x')
		statusicon=Tkinter.Canvas(statusbar,height=20, width=20)
		statusicon.create_oval(3, 3, 17, 17, outline="black", fill="red")
		statusicon.pack(side='left')
		statustext=Tkinter.Label(statusbar, text="Not Connected", anchor='w')
		statustext.pack(side='left')
		timetext=Tkinter.Label(statusbar, anchor='e')
		timetext.pack(side='right')
		
		#main text box w/ scrollbar
		t=Tkinter.Text(root, height=40, width=80)
		t.pack()
		scroll = Tkinter.Scrollbar(root)
		scroll.pack(side='right', fill='y')
		t.pack(side='left', fill='both', expand=True)
		scroll.config(command=t.yview)
		t.configure(yscrollcommand=scroll.set)
		t.config(state='disabled')
		
		###Set up Menus###
		menubar = Tkinter.Menu(root)
		root.config(menu=menubar)
		
		#file menu
		filemenu = Tkinter.Menu(menubar, tearoff=0)
		filemenu.add_command(label="Open Log File", command=self.open_logfile)
		filemenu.add_command(label="Collect Reports from Log File", command=self.process_logfile)
		filemenu.add_separator()
		filemenu.add_command(label="Clear Window", command=self.clear_window)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=self.exit)
		menubar.add_cascade(label="File", menu=filemenu)
		
		#Connect menu.  Filled in from update_ports
		serialmenu = Tkinter.Menu(menubar, tearoff=0)
		menubar.add_cascade(label="Serial", menu=serialmenu)
		
		#Analyze menu
		analyzemenu = Tkinter.Menu(menubar, tearoff=0)
		menubar.add_cascade(label="Analyze", menu=analyzemenu)
		analyzemenu.add_command(label="Data Numerical", command=self.analyze_numerical)
		analyzemenu.add_command(label="Data Graphical", command=self.analyze_graphical)
		
		#Setup menu
		setupmenu = Tkinter.Menu(menubar, tearoff=0)
		menubar.add_cascade(label="Setup", menu=setupmenu)
		setupmenu.add_command(label="Auto Serial Report Config", command=self.report_config_auto)
		setupmenu.add_command(label="Manual Report Config", command=self.report_config_manual)
		setupmenu.add_command(label='Options', command=self.edit_options)
		
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
		self.serialmenu=serialmenu
		self.timetext=timetext
		
		#initialize configuration.
		self.options=Options()			
		
		#initialize filenames
		self.path=os.path.dirname(os.path.realpath(__file__))
		self.path = '/'.join(self.path.split('\\'))
		self.processfile=self.path+"/"+"process.log"
		self.errorfile=self.path+"/"+"error.log"
		
		crashfile=self.path+"/"+"crash.log"
		#sys.stderr = open(crashfile, 'a')

		
		#initialize other variables
		self.report={}
		self.stringbuffer=""
		self.sublabels=[]
		self.logfile=None
		self.serial=None
		self.serialalarm=None
		self.learning=False
		
		#config
		#self.dbversion=dbversion
		if not self.init_database():
			self.exit(confirm=False)
			return
		
		###Startup Functions###
		
		#initialize serial
		if self.options.serial_autoconnect and self.options.serial_port:
			self.serial_connect()
		else:
			if self.options.serial_autoconnect:
				tkMessageBox.showinfo("Serial Autoconnect Failed","Serial Autoconnect Failed.\nAutoconnect is enabled but no port was specified")
			self.update_ports()
		
		self.update_time()
		
	
	#function run when window closed from any way except File->Exit
	
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
	def exit(self,confirm=True):
		if confirm:
			if not tkMessageBox.askyesno("Exit","Are you sure you would like to exit?"):
				return
		#self.t.after_cancel(self.serialalarm)
		#self.timetext.after_cancel(self.timealarm)
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
		self.t.configure(state='normal')
		self.t.delete('1.0','end')
		self.t.configure(state='disabled')
	
	#function which gets current list of serial ports and makes connect menu show them
	def update_ports(self):
		while self.serialmenu.index("end") is not None:
			self.serialmenu.delete(0)
		comports = sorted(serial.tools.list_ports.comports(), key=lambda x: x[0])
		for port,description,address in comports:
			self.serialmenu.add_command(label=port + " - " + description, command=lambda p=port: self.serial_connect(p))
		self.serialmenu.add_separator()
		self.serialmenu.add_command(label='Refresh Ports', command=self.update_ports)
	
	def update_time(self):
		"""Periodically called function run to update time in GUI"""
		timestr=datetime.now().strftime('%I:%M:%S %p')
		if timestr!=self.timetext['text']:
			self.timetext['text']=timestr
		self.timealarm=self.timetext.after(20,self.update_time)
	
	#function to connect to a serial port and begin monitoring for reports
	def serial_connect(self,port=None):
		if port is not None:
			self.options.serial_port=port
		port=self.options.serial_port
		baudrate=self.options.serial_baudrate
		bytesize=self.options.serial_bytesize
		parity=self.options.serial_parity
		stopbits=self.options.serial_stopbits
		
		#needed for pyserial 2.7. If is for Windows, else is for Linux
		m=re.search(r"\ACOM(\d+)\Z",port)
		if m:
			portno=int(m.group(1))-1
		else:
			portno=port
		
		try:
			#serial 3.4/2.7 support respectively
			try:
				self.serial=serial.Serial(port,baudrate=baudrate, bytesize=bytesize,parity=parity, stopbits=stopbits, timeout=0)
			except:
				self.serial=serial.Serial(portno,baudrate=baudrate, bytesize=bytesize,parity=parity, stopbits=stopbits, timeout=0)
		except serial.SerialException:
			tkMessageBox.showerror("Serial Error", "Error opening com port %s."%port)
			self.log_error("Error opening com port %s."%port)
			return
		except ValueError:
			tkMessageBox.showerror("Serial Error", "Error opening com port %s."%port)
			self.log_error("Error opening com port %s."%port)
			return
		
		#serial 2.7/3.4 support
		try:
			self.serial.flushInput()
		except:
			self.serial.reset_input_buffer()
		
		while self.serialmenu.index("end") is not None:
			self.serialmenu.delete(0)
		self.serialmenu.add_command(label='Disconnect', command=self.serial_disconnect)	
		
		self.log_process("Connected to %s" % (port,))
		#self.menubar.entryconfigure(2, state=DISABLED)
		self.statusicon.itemconfigure('all', fill="green")
		self.statustext.config(text="Connected to port: %s at %s,%s,%s,%s"%(port,self.serial.baudrate,self.serial.bytesize,self.serial.parity,self.serial.stopbits))
		self.process_serial()
	
	#function to disconnect serial.  Done if there is a serial error.
	def serial_disconnect(self):
		self.serial.close()
		self.t.after_cancel(self.serialalarm)
		self.update_ports()
		self.menubar.entryconfigure(2, state='normal')
		self.statusicon.itemconfigure('all', fill="red")
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
		self.an_win = Tkinter.Toplevel()
		self.an_win.tk.call('wm', 'iconphoto', self.an_win._w, self.icon)
		DataNumerical(self.an_win,self.options)

	def analyze_graphical(self):
		"""Function to load the Analyze Graphical window"""
		if hasattr(self, 'ag_win') and self.ag_win.winfo_exists():
			self.ag_win.deiconify()
			self.ag_win.focus_force()
			self.ag_win.lift()
			return
		self.ag_win = Tkinter.Toplevel(height=800,width=1100)
		self.ag_win.tk.call('wm', 'iconphoto', self.ag_win._w, self.icon)
		DataGraphical(self.ag_win,self.options)
		
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
		self.rc_win = Tkinter.Toplevel()
		self.rc_win.tk.call('wm', 'iconphoto', self.rc_win._w, self.icon)
		ReportConfig(self.rc_win,self.options)
	
	#function to process log file.  Can process multiple at the same time.  Used for both configuration and importing of reports
	def process_logfile(self):
		logfilenames = askopenfilenames(title='Select Log File',filetypes=[('Log File','*.log'),("All Files", "*.*"),],defaultextension = '.log')
		if not logfilenames:
			return
		oldstatus=self.statustext['text']
		oldcolor=self.statusicon.itemcget('all',"fill")
		self.statusicon.itemconfigure('all', fill="yellow")
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
		self.statusicon.itemconfigure('all', fill=oldcolor)
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
		self.t.config(state='normal')
		self.t.insert('end',line)
		self.t.see('end')
		#remove extra rows so we are within the max.
		while int(eval(self.t.index('end-1c')))>self.options.maxlines:
			self.t.delete('1.0','2.0')
		self.t.config(state='disabled')
	
	#function to process a line of text from process_serial or process_logfile
	#creates and manages reports (self.report) and when a report is complete runs process_report
	def process_line(self,line):
		
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
			self.process_serial_report()
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
	
	
	def process_serial_report(self):
		"""Function to break up a full serial report into individual sensor reports and process those."""
		while self.report['data']:
			report=Report(self.report)
			self.report['data'].pop(0)
			if self.learning:
				self.learn_report(report)
			else:
				self.process_report(report)
				

	def process_report(self,report):
		"""Function to process an individual sensor report including error checking. """
		self.db = sqlite3.connect(self.options.dbfile)
		c=self.db.cursor()
		
		#check if number of values=number of labels
		if len(report.Values)!=len(report.LabelNames):
			#self.log_process("Label and Value count do not match. Labels=%d, Values=%d"%(len(report.LabelNames),len(report.Values)))
			print "Label/Error count mismatch"
			#add error logging here
			return
			
		#check if report exists in database
		c.execute("""SELECT ReportConfigID from v_structure WHERE LocationName=? and SensorName=? and ReportTypeName=?""",(report.LocationName,report.SensorName,report.ReportTypeName))
		result=c.fetchone()
		if result is None:
			print "report config not found"
			#add error logging
			return
		else:
			ReportConfigID=result[0]
			#print ReportConfigID,
		
		#check if labels are configured in database and they match the current report labels
		c.execute("""SELECT LabelID,LabelName from v_structure WHERE ReportConfigID=?""",(ReportConfigID,))
		labels=c.fetchall()
		if len(labels)==0:
			print "no labels"
			#add error logging
			return				
		if sorted(report.LabelNames)!=sorted([x[1] for x in labels]):
			print "labels do not match"
			#add error logging
			return
		
		#check if grade exists and has correct name
		c.execute('''SELECT GradeID,GradeName FROM grades WHERE GradeCode = ?''',(report.GradeCode,))
		result=c.fetchone()
		if result:
			GradeID=result[0]
			if result[1]!=report.GradeName:
				c.execute('''UPDATE grades SET GradeName=? WHERE GradeID = ?''',(report.GradeName,GradeID))
				self.log_process("Updated grade %s name from %s to %s"%(report.GradeCode,result[1],report.GradeName))
		else:
			c.execute('''INSERT INTO grades (GradeID, GradeCode, GradeName) VALUES (NULL,?,?)''', (report.GradeCode,report.GradeName))
			GradeID=c.lastrowid
			self.log_process("Added missing grade %s %s"%(report.GradeCode,report.GradeName))		
		
		c.execute('''INSERT INTO reports (ReportID, Timestamp, ReportConfigID, GradeID) VALUES (NULL,?,?,?)''', (report.Timestamp,ReportConfigID,GradeID))
		ReportID=c.lastrowid
		
		for LabelID,LabelName in labels:
			i=report.LabelNames.index(LabelName)
			c.execute('''INSERT INTO reportData (ReportDataID, ReportID, LabelID, Value) VALUES (NULL,?,?,?)''',(ReportID,LabelID,report.Values[i]))
		self.db.commit()
		self.db.close()			
		self.log_process("%s: %s, %s, %s, %s" % (report.ReportTypeName,report.LocationName,report.SensorName,report.Timestamp.strftime('%Y-%m-%d %H:%M'),report.GradeCode))
		
	def learn_report(self,report):
		"""Function to process an individual sensor report to modify the configuration in the database."""
		#need to update this to take in a Report class as an argument
		
		self.db = sqlite3.connect(self.options.dbfile)
		c=self.db.cursor()
		
		#check/add reportType exists
		c.execute('''SELECT reportTypeID FROM reportTypes WHERE ReportTypeName = ?''',(report.ReportTypeName,))
		result=c.fetchone()
		if result:
			ReportTypeID=result[0]
		else:
			c.execute('''INSERT INTO reportTypes (ReportTypeID, ReportTypeName) VALUES (NULL,?)''', (report.ReportTypeName,))
			ReportTypeID=c.lastrowid
			self.log_process("New report type %s added to database"%report.ReportTypeName)
		
		#check/add location exists
		c.execute('''SELECT LocationID FROM locations WHERE LocationName = ?''',(report.LocationName,))
		result=c.fetchone()
		if result:
			LocationID=result[0]
		else:
			c.execute('''INSERT INTO locations (LocationID, LocationName) VALUES (NULL,?)''', (report.LocationName,))
			LocationID=c.lastrowid
			self.log_process("New location %s added to database"%report.LocationName)
			
		#check if sensor exists
		c.execute('''SELECT SensorID FROM sensors WHERE SensorName = ? and LocationID = ?''',(report.SensorName,LocationID))
		result=c.fetchone()
		if result:
			SensorID = result[0]
		else:
			c.execute('''INSERT INTO sensors (SensorID,SensorName,LocationID) VALUES (NULL,?,?)''', (report.SensorName,LocationID))
			SensorID=c.lastrowid
			self.log_process("New sensor %s at location %s added to database"%(report.SensorName,report.LocationName))
		
		#check/add reportConfig exists
		c.execute('''SELECT reportConfigID FROM reportConfig WHERE ReportTypeID = ? AND SensorID=? and ReportSource=?''',(ReportTypeID,SensorID,0))
		result=c.fetchone()
		if result:
			ReportConfigID=result[0]
		else:
			c.execute('''INSERT INTO reportConfig (ReportConfigID, SensorID, ReportTypeID, ReportSource, Active, TriggerTagID) VALUES (NULL,?,?,0,1,NULL)''', (SensorID,ReportTypeID))
			ReportConfigID=c.lastrowid
			self.log_process("New report configuration for sensor %s at location %s with type %s added to database"%(report.SensorName,report.LocationName,report.ReportTypeName))
			
		for LabelName in report.LabelNames:
			c.execute('''SELECT LabelID FROM labels WHERE LabelName = ? and ReportConfigID = ?''',(LabelName,ReportConfigID))
			result=c.fetchone()
			if result:
				LabelID = result[0]
			else:
				c.execute('''INSERT INTO labels (LabelID, LabelName, ReportConfigID, TagID) VALUES (NULL,?,?,NULL)''', (LabelName,ReportConfigID))
				LabelID=c.lastrowid
				self.log_process("New label %s for sensor %s at location %s added to database"%(LabelName,report.SensorName,report.LocationName))
			
		#close every time. Most of the time we process multple reports at a time.
		self.db.commit()
		self.db.close()
		
	def init_database(self):
		"""Method to create a blank database in the correct format.  Run if database does not exists"""
		changed=False
		while not self.check_database(self.options.dbfile):
			changed=True
			if not os.path.isfile(self.options.dbfile):
				answer=tkMessageBox.askyesno("Database not found","Database not found\nWould you like to browse for a current database?")
				if answer:
					self.options.dbfile=askopenfilename(title='Select Database',filetypes=[('Database File','*.db'),("All Files", "*.*"),],defaultextension = '.db')
					if self.check_database(self.options.dbfile):
						continue
	
			answer=tkMessageBox.askyesno("Invalid Database","Would you like to create a new database?")
			if answer:
				dbfile=asksaveasfilename(title='Select Database',filetypes=[('Database File','*.db'),("All Files", "*.*"),],defaultextension = '.db',confirmoverwrite=False)
				if not dbfile:
					tkMessageBox.showerror("Database Error","No Database Selected")
					return False
				if os.path.isfile(dbfile):
					tkMessageBox.showerror("Database Error","Cannot Overwrite Existing Database")
					continue
				self.options.dbfile=dbfile
				self.create_database()
				continue
			else:
				return False
			
		if changed:
			answer=tkMessageBox.askyesno("Save Default Database?","Would you like this to be your new default database?")
			if answer:
				self.options.save('dbfile')
		return True
			
	def check_database(self,dbfile):
		if os.path.isfile(dbfile):
			#check if db version matches STK version
			db=sqlite3.connect(dbfile)
			c=db.cursor()				
			c.execute("""SELECT DatabaseVersion FROM config WHERE rowid=1""")
			result=c.fetchone()
			if result is not None:
				version=result[0]
			else:
				return False
			if version==self.options.dbversion:
				return True
			else:
				tkMessageBox.showinfo("Incorrect Database Version","Database Version does not match application version.")
				return False
		else:
			tkMessageBox.showinfo("File Not Found","Database File Not Found")
			return False
		
	def create_database(self):
		#tkMessageBox.showinfo("Database not found","Database not found\nCreating blank database at %s"%self.options.dbfile)
		db = sqlite3.connect(self.options.dbfile)
		c=db.cursor()		
		c.execute("""CREATE TABLE "config" ( `DatabaseVersion` TEXT NOT NULL, `MachineName` TEXT DEFAULT NULL, `CustomerName` TEXT DEFAULT NULL, `CustomerLocation` TEXT DEFAULT NULL )""")
		c.execute("""CREATE TABLE "grades" ( `GradeID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `GradeCode` INTEGER NOT NULL, `GradeName` TEXT NOT NULL )""")
		c.execute("""CREATE TABLE "labels" ( `LabelID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `LabelName` TEXT NOT NULL, `ReportConfigID` INTEGER NOT NULL , TagID TEXT DEFAULT NULL)""")
		c.execute("""CREATE TABLE "locations" ( `LocationID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `LocationName` TEXT NOT NULL )""")
		c.execute("""CREATE TABLE "reportConfig" ( `ReportConfigID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `SensorID` INTEGER NOT NULL, `ReportTypeID` INTEGER, `ReportSource` INTEGER , Active INTEGER DEFAULT 1, TriggerTagID INTEGER DEFAULT NULL)""")
		c.execute("""CREATE TABLE "reportData" ( `ReportDataID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `ReportID` INTEGER NOT NULL, `LabelID` INTEGER NOT NULL, `Value` NUMERIC NOT NULL )""")
		c.execute("""CREATE TABLE "reportTypes" ( `ReportTypeID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `ReportTypeName` TEXT NOT NULL )""")
		c.execute("""CREATE TABLE "reports" ( `ReportID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `Timestamp` TEXT NOT NULL, `ReportConfigID` INTEGER NOT NULL, `GradeID` INTEGER DEFAULT NULL )""")
		c.execute("""CREATE TABLE "sensors" ( `SensorID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `SensorName` TEXT NOT NULL, `LocationID` INTEGER NOT NULL )""")
		c.execute("""CREATE VIEW v_reportData AS SELECT reports.ReportID as ReportID, timestamp, reportConfig.ReportConfigID as ReportConfigID, ReportTypeName, locations.LocationID as LocationID, LocationName, reports.GradeID as GradeID, GradeCode, GradeName, sensors.SensorID as SensorID, sensors.SensorName as SensorName, labels.LabelID as LabelID, labels.LabelName as LabelName, Value, reportData.ReportDataID as ReportDataID FROM reports INNER JOIN reportConfig ON reportConfig.ReportConfigID = reports.ReportConfigID INNER JOIN grades ON grades.GradeID = reports.GradeID INNER JOIN reportData ON reportData.ReportID = reports.reportID INNER JOIN labels ON labels.LabelID = reportData.LabelID INNER JOIN sensors ON sensors.SensorID = reportConfig.SensorID INNER JOIN locations ON locations.LocationID = sensors.LocationID INNER JOIN reportTypes ON reportTypes.ReportTypeID = reportConfig.ReportTypeID""")
		c.execute("""CREATE VIEW v_structure AS SELECT reportConfig.reportConfigID as ReportConfigID, reportConfig.ReportSource as ReportSource, reportConfig.Active AS Active, reportConfig.TriggerTagID as TriggerTagID, locations.LocationID as LocationID, locations.LocationName as LocationName, sensors.SensorID as SensorID, sensors.SensorName as SensorName, reportTypes.ReportTypeID as ReportTypeID, reportTypes.ReportTypeName as ReportTypeName, labels.LabelID as LabelID, labels.LabelName as LabelName, labels.TagID as TagID FROM reportConfig INNER JOIN sensors on sensors.SensorID = reportConfig.SensorID INNER JOIN locations on locations.LocationID = sensors.LocationID INNER JOIN reportTypes on reportTypes.ReportTypeID = reportConfig.ReportTypeID INNER JOIN labels on labels.ReportConfigID = reportConfig.ReportConfigID;""")
		c.execute("""INSERT INTO config (DatabaseVersion, MachineName, CustomerName, CustomerLocation) VALUES (?,NULL,NULL,NULL)""",(self.options.dbversion,))
		db.commit()
		db.close()		
		
	def edit_options(self):
		if hasattr(self, 'option_win') and self.option_win.winfo_exists():
			self.option_win.deiconify()
			self.option_win.focus_force()
			self.option_win.lift()
			return
		self.option_win = Tkinter.Toplevel()
		self.option_win.withdraw()
		self.option_win.tk.call('wm', 'iconphoto', self.option_win._w, self.icon)
		OptionWindow(self.option_win,self.options)

class ReportConfig:
	def __init__(self,parent,options):
		self.options=options
		#self.icon=config.icon
		self.win=parent
	
		self.win.geometry("+100+100")
		self.win.geometry("800x600")
		self.win.minsize(800,600)
		
		#split window into two panes
		paned=Tkinter.PanedWindow(self.win,orient='horizontal')
		paned.pack(fill='both',expand=1)
		
		report_frame=Tkinter.Frame(paned, width=270)
		paned.add(report_frame, minsize=270)
		report_frame.grid_propagate(0)
		report_frame.columnconfigure(0, weight = 1)
		report_frame.columnconfigure(1, weight = 0)
		report_frame.rowconfigure(0, weight = 1)
		report_frame.rowconfigure(1, weight = 0)
		report_frame.rowconfigure(2, weight = 0)
		
		data_frame=Tkinter.LabelFrame(paned,text="Report Configuration")
		paned.add(data_frame)
		
		rt_lframe=Tkinter.LabelFrame(report_frame,text="Machine Structure")
		rt_lframe.grid(column=0,row=0,sticky='wens',padx=2)
		rt_lframe.columnconfigure(0, weight = 1)
		rt_lframe.columnconfigure(1, weight = 1)
		rt_lframe.rowconfigure(0, weight = 1)
		rt_lframe.rowconfigure(1, weight = 0)
		structure_add_button=Tkinter.Button(rt_lframe,text="Add Item",width=1,state='disabled')
		structure_add_button.grid(column=0,row=1,sticky='wens',padx=2,pady=2)
		structure_remove_button=Tkinter.Button(rt_lframe,text="Remove Item",width=1,state='disabled')
		structure_remove_button.grid(column=1,row=1,sticky='wens',padx=2,pady=2)
		rt_sframe=Tkinter.Frame(rt_lframe)
		rt_sframe.grid(column=0,row=0,columnspan=2,sticky='wens',padx=2,pady=2)
		rt_vscroll = Tkinter.Scrollbar(rt_sframe)
		rt_vscroll.pack(side='right', fill='y', padx=(0,2))			
		report_tree=StructureTree(rt_sframe,options)
		report_tree.pack(side='bottom', fill='both', expand=True, padx=(2,0))
		report_tree['show']='tree'
		rt_vscroll.config(command=report_tree.yview)
		report_tree.configure(yscrollcommand=rt_vscroll.set)		
		
		tt_lframe=Tkinter.LabelFrame(report_frame,text="Report Types")
		tt_lframe.grid(column=0,row=1,sticky='wens',padx=2)
		tt_lframe.columnconfigure(0, weight = 1)
		tt_lframe.columnconfigure(1, weight = 1)
		tt_lframe.rowconfigure(0, weight = 1)
		tt_lframe.rowconfigure(1, weight = 0)
		type_add_button=Tkinter.Button(tt_lframe,text="Add Item",width=1,state='disabled')
		type_add_button.grid(column=0,row=1,sticky='wens',padx=2,pady=2)
		type_remove_button=Tkinter.Button(tt_lframe,text="Remove Item",width=1,state='disabled')
		type_remove_button.grid(column=1,row=1,sticky='wens',padx=2,pady=2)
		tt_sframe=Tkinter.Frame(tt_lframe)
		tt_sframe.grid(column=0,row=0,columnspan=2,sticky='wens',padx=2,pady=2)
		tt_vscroll = Tkinter.Scrollbar(tt_sframe)
		tt_vscroll.pack(side='right', fill='y', padx=(0,2))							
		type_tree=ReportTypeTree(tt_sframe,self.options)
		type_tree['height']=5
		type_tree.pack(side='bottom', fill='both', expand=True, padx=(2,0))
		type_tree['show']='tree'
		tt_vscroll.config(command=type_tree.yview)
		type_tree.configure(yscrollcommand=tt_vscroll.set)		
			
		
		report_tree.bind("<<TreeviewSelect>>",type_tree.update_reports,add="+")
		report_tree.bind("<<TreeviewSelect>>",self.button_states,add="+")
		
		
		self.source = Tkinter.IntVar(value=0)
		rs_lframe=Tkinter.LabelFrame(report_frame,text="Report Source Type")
		rs_lframe.grid(column=0,row=2,sticky='wens',padx=2)
		rs_lframe.columnconfigure(0, weight = 1)
		rs_lframe.columnconfigure(1, weight = 1)
		rs_lframe.rowconfigure(0, weight = 1)
		rs_lframe.rowconfigure(1, weight = 0)
		rs_lframe.rowconfigure(2, weight = 0)
		Tkinter.Radiobutton(rs_lframe, text="Serial Datalogger", variable=self.source, value=0,anchor='w').grid(row=0,column=0,columnspan=2,sticky='wens')
		Tkinter.Radiobutton(rs_lframe, text="OPC Datalogger", variable=self.source, value=1,anchor='w').grid(row=1,column=0,columnspan=2,sticky='wens')
		Tkinter.Button(rs_lframe,text="Create New Report",command=self.create_report).grid(column=0,row=2,columnspan=2,sticky='wens',padx=2,pady=2)
		
		
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
			self.structure_add_button['state']='disabled'
			self.structure_remove_button['state']='active'
		elif call_widget.tag_has("Machine",item): #doesn't exists yet
			self.structure_add_button['state']='active'
			self.structure_remove_button['state']='disabled'		
		elif call_widget.tag_has("Location",item):
			if call_widget.get_children(item):
				self.structure_add_button['state']='active'
				self.structure_remove_button['state']='disabled'
			else:
				self.structure_add_button['state']='active'
				self.structure_remove_button['state']='active'				
		else:	#no selection.  should never happen
			self.structure_add_button['state']='disabled'
			self.structure_remove_button['state']='disabled'
	
	def create_report(self):
		"""Placeholder for funtion which will generate the GUI for creating a new """
		print self.source.get()
		
class DataNumerical:
	def __init__(self,parent,options):
		self.options=options
		self.an_win=parent
		
		self.an_win.geometry("+100+100")
		self.an_win.geometry("800x600")
		self.an_win.minsize(800,600)
		
		#create status bar at the bottom of the window
		statusbar=Tkinter.Frame(self.an_win,borderwidth=1, relief='sunken')
		statusbar.pack(side='bottom', fill='x')
		self.statustext = Tkinter.StringVar()
		#self.statustext.set('Status');
		Tkinter.Label(statusbar, textvariable=self.statustext, anchor='w').pack(side='left')		
		
		#split window into two panes
		paned=Tkinter.PanedWindow(self.an_win,orient='horizontal')
		paned.pack(fill='both',expand=1)		
		
		report_frame=Tkinter.Frame(paned)
		paned.add(report_frame, minsize=250, padx=2)
		report_frame.pack_propagate(0)
		data_frame=Tkinter.Frame(paned)
		paned.add(data_frame, padx=2)
		
		#data frame
		data_tree=Treeview(data_frame,selectmode="browse", show="tree")
		hscroll = Tkinter.Scrollbar(data_frame,orient="horizontal")
		hscroll.pack(side="bottom", fill="x")
		vscroll = Tkinter.Scrollbar(data_frame)
		vscroll.pack(side="right", fill="y")
		data_tree.pack(side="left",fill="both",anchor="n",expand=True)
		vscroll.config(command=data_tree.yview)
		data_tree.configure(yscrollcommand=vscroll.set)
		hscroll.config(command=data_tree.xview)
		data_tree.configure(xscrollcommand=hscroll.set)
		
		#report frame
		csv_button=Tkinter.Button(report_frame, text="Save as CSV", command=self.save_csv,state='disabled')#, relief="ridge"
		csv_button.pack(side="bottom", fill="x", padx=1,pady=(0,2))
		generate_button=Tkinter.Button(report_frame, text="Generate Report", command=self.generate_report,state='disabled')#, relief="ridge"
		generate_button.pack(side="bottom", fill="x", padx=1,pady=2)
		
		##variable##
		self.filter_select = Tkinter.IntVar()
		self.filter_start = Tkinter.StringVar()
		self.filter_end = Tkinter.StringVar()
		
		#filter_frame=Frame(report_frame,width=225,height=200, relief="sunken", borderwidth=1,bg="white")
		ff_lframe=Tkinter.LabelFrame(report_frame,text="Time Filter")
		ff_lframe.pack(side='bottom', fill='x')
		filter_frame=Tkinter.Frame(ff_lframe,width=225,height=200)
		filter_frame.pack(side='bottom', fill='both', padx=2, pady=2)
		filter_frame.pack_propagate(0)
		#move code starting here to new class
		filter_frame.columnconfigure(0, weight = 1)
		filter_frame.columnconfigure(1, weight = 1)
		Tkinter.Radiobutton(filter_frame, text="Prior Day", variable=self.filter_select, value=0,command=self.change_filter).grid(row=1,column=0,sticky='w')
		Tkinter.Radiobutton(filter_frame, text="Prior Week", variable=self.filter_select, value=1,command=self.change_filter).grid(row=1,column=1,sticky='w')
		Tkinter.Radiobutton(filter_frame, text="Prior Month", variable=self.filter_select, value=2,command=self.change_filter).grid(row=2,column=0,sticky='w')
		Tkinter.Radiobutton(filter_frame, text="Prior Year", variable=self.filter_select, value=3,command=self.change_filter).grid(row=2,column=1,sticky='w')
		Tkinter.Radiobutton(filter_frame, text="All Data", variable=self.filter_select, value=4,command=self.change_filter).grid(row=3,column=0,sticky='w')
		Tkinter.Radiobutton(filter_frame, text="Custom Time", variable=self.filter_select, value=5,command=self.change_filter).grid(row=3,column=1,sticky='w')
		self.filter_select.set(0)
		self.filter_start.set((datetime.now()-timedelta(days=7)).strftime("%Y-%m-%d %H:%M"))
		self.filter_end.set(datetime.now().strftime("%Y-%m-%d %H:%M"))
		Tkinter.Label(filter_frame, text="Start").grid(row=4,column=0)
		Tkinter.Label(filter_frame, text="End").grid(row=4,column=1)
		start_entry=Tkinter.Entry(filter_frame, textvariable=self.filter_start,bg="white",state='disabled',justify='center')
		start_entry.grid(row=5,column=0)
		end_entry=Tkinter.Entry(filter_frame, textvariable=self.filter_end,bg="white",state='disabled',justify='center')
		end_entry.grid(row=5,column=1)
		#move code ending here to new class
		
		tt_lframe=Tkinter.LabelFrame(report_frame,text="Report Types")
		tt_lframe.pack(side='bottom', fill='x')		
		tt_vscroll = Tkinter.Scrollbar(tt_lframe)
		tt_vscroll.pack(side='right', fill='y', padx=(0,2), pady=(0,2))			
		type_tree=ReportTypeTree(tt_lframe,self.options)
		tt_lframe.pack(side='bottom', fill='both')		
		type_tree.config(height=5)
		type_tree.column("#0",stretch=True)
		type_tree.pack(side='bottom',fill='x',anchor='s', padx=(2,0), pady=(0,2))
		tt_vscroll.config(command=type_tree.yview)
		type_tree.configure(yscrollcommand=tt_vscroll.set)		
		
		rt_lframe=Tkinter.LabelFrame(report_frame,text="Machine Structure")
		rt_lframe.pack(side='bottom', fill='both', expand=True)	
		rt_vscroll = Tkinter.Scrollbar(rt_lframe)
		rt_vscroll.pack(side='right', fill='y', padx=(0,2), pady=(0,2))				
		report_tree=StructureTree(rt_lframe,self.options)
		report_tree.column("#0",stretch=True)
		report_tree.pack(side='left',fill='both',expand=True, anchor='s', padx=(2,0), pady=(0,2))
		rt_vscroll.config(command=report_tree.yview)
		report_tree.configure(yscrollcommand=rt_vscroll.set)		
		
		report_tree.bind("<<TreeviewSelect>>",type_tree.update_reports,add="+")
		report_tree.bind("<<TreeviewSelect>>",lambda event: self.generate_button_state(),add="+")

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
			enddate=datetime.now()
			startdate=enddate-timedelta(days=1)
		elif filter==1:
			enddate=datetime.now()
			startdate=enddate-timedelta(days=7)
		elif filter==2:
			enddate=datetime.now()
			startdate=enddate-timedelta(days=30)
		elif filter==3:
			enddate=datetime.now()
			startdate=enddate-timedelta(days=365)
		elif filter==4:
			enddate=datetime.now()
			startdate=datetime.strptime("1970-01-01 00:00","%Y-%m-%d %H:%M")
		elif filter==5:
			try:
				enddate=datetime.strptime(self.filter_end.get().strip(),"%Y-%m-%d %H:%M")
			except ValueError:
				tkMessageBox.showerror("Invalid Date","Invalid End Date\nPlease select valid date using format YYYY-MM-DD HH:MM", parent=self.an_win)
				return
			try:
				startdate=datetime.strptime(self.filter_start.get().strip(),"%Y-%m-%d %H:%M")
			except ValueError:
				tkMessageBox.showerror("Invalid Date","Invalid Start Date\nPlease select valid date using format YYYY-MM-DD HH:MM", parent=self.an_win)
				return
			if enddate<=startdate:
				tkMessageBox.showerror("Invalid Dates","End date must be after start date.", parent=self.an_win)
				return
		
		#set starttime.seconds to zero just to avoid confusion
		startdate=startdate.replace(second=0)
		
		#get selected SensorID from tree id
		sensor=self.report_tree.selection()[0]
		SensorID=sensor.split("_")[1]
		
		#get selected sensor LocationID from tree id of parent
		LocationID=self.report_tree.parent(sensor).split("_")[1]
		
		#get ReportTypeID from  tree
		rtype=self.type_tree.selection()[0]
		ReportConfigID=rtype.split("_")[1]
		
		self.csv_button.config(state='disabled')
		
		starttime=datetime.now()
		
		self.db = sqlite3.connect(self.options.dbfile)
		c=self.db.cursor()
		
		c.execute("""SELECT DISTINCT LabelName,LabelID from v_structure WHERE ReportConfigID=? ORDER BY labelID""",(ReportConfigID,)) 
		results=c.fetchall()		
		
		LabelNames,LabelIDs=zip(*results)
		LabelCount=len(LabelNames)
		LabelNames=list(LabelNames)
		LabelIDs=list(LabelIDs)
	
		
		c.execute("""SELECT ReportSource from v_structure WHERE ReportConfigID=?""",(ReportConfigID,)) 
		source=c.fetchone()[0]
		
		if source==0:
			LabelNames.insert(0,'GRADE CODE')
			LabelCount=len(LabelNames)
			LabelIDs.insert(0,0)

		self.data_tree["columns"]=LabelIDs
		self.data_tree.column("#0",width=160)
		self.data_tree.heading("#0",text="TIMESTAMP")				
		
		
		for i,LabelName in enumerate(LabelNames):
			w=int(tkFont.nametofont('TkHeadingFont').measure(LabelName)*1.25)
			w=max(w,75)
			self.data_tree.column(LabelIDs[i],width=w)
			self.data_tree.heading(LabelIDs[i],text=LabelName)
		
		lastReportID=-1
		c.execute("""SELECT ReportID, timestamp, LabelID, Value, GradeCode from v_reportData WHERE ReportConfigID=? and timestamp>=? and timestamp<=? ORDER BY timestamp DESC, ReportID DESC""",(ReportConfigID,startdate,enddate))
		for ReportID, timestamp, LabelID, Value, GradeCode in c.fetchall():
			if ReportID!=lastReportID:
				if lastReportID!=-1:
					self.data_tree.insert("",'end',text=lastTimestamp,values=values)
				values=[""] * LabelCount
				if source==0:
					values[0]=GradeCode				
			i=LabelIDs.index(LabelID)
			values[i]=Value
			lastReportID=ReportID
			lastTimestamp=timestamp
		self.data_tree.insert("",'end',text=timestamp,values=values)
		
		c.close()
		self.db.close()
		
		records = len(self.data_tree.get_children())
		
		if records==0:
			self.data_tree.insert("",'end',text="No data found")
			self.data_tree['show']='tree'
			self.csv_button.config(state='disabled')
		else:
			self.csv_button.config(state='active')
			self.data_tree['show']='tree headings'
			
		endtime=datetime.now()
		elapsed=endtime-starttime
		status="%d records found in %s seconds." % (records,elapsed.total_seconds())
		self.statustext.set(status)
		
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
			for report in self.data_tree.get_children():
				timestamp=[]
				timestamp.append(self.data_tree.item(report)['text'])
				row=list(str(x) for x in self.data_tree.item(report)['values'])
				line=','.join(timestamp+row)
				writer.writerow(timestamp+row)

class DataGraphical:
	def __init__(self,parent,options):
		self.options=options
		self.win=parent
	
		#self.win.geometry("+100+100")
		#self.win.geometry("1000x800")
		self.win.minsize(1000,800)
		
		#create status bar at the bottom of the window
		statusbar=Tkinter.Frame(self.win,borderwidth=1, relief='sunken')
		statusbar.pack(side='bottom', fill='x')
		self.statustext = Tkinter.StringVar()
		#self.statustext.set('Status');
		Tkinter.Label(statusbar, textvariable=self.statustext, anchor='w').pack(side='left')		
		
		#split window into two panes
		paned=Tkinter.PanedWindow(self.win,orient='horizontal')
		paned.pack(fill='both',expand=1)		
		
		report_frame=Tkinter.Frame(paned)
		paned.add(report_frame, minsize=250, padx=2)
		report_frame.pack_propagate(0)
		data_frame=Tkinter.Frame(paned)
		paned.add(data_frame, padx=2)
		
		#data frame
		f = Figure()
		self.ax=f.add_subplot(111)
		self.canvas = FigureCanvasTkAgg(f, data_frame)
		self.canvas.get_tk_widget().pack(side='bottom', fill='both', expand=True)			
		
		#report frame
		generate_button=Tkinter.Button(report_frame, text="Generate Report", command=self.generate_graph,state='disabled')#, relief="ridge"
		generate_button.pack(side="bottom", fill="x", padx=1,pady=2)
		
		##variable##
		self.filter_select = Tkinter.IntVar()
		self.filter_start = Tkinter.StringVar()
		self.filter_end = Tkinter.StringVar()
		
		#filter_frame=Frame(report_frame,width=225,height=200, relief="sunken", borderwidth=1,bg="white")
		ff_lframe=Tkinter.LabelFrame(report_frame,text="Time Filter")
		ff_lframe.pack(side='bottom', fill='x')
		filter_frame=Tkinter.Frame(ff_lframe,width=225,height=200)
		filter_frame.pack(side='bottom', fill='both', padx=2, pady=2)
		filter_frame.pack_propagate(0)
		#move code starting here to new class
		filter_frame.columnconfigure(0, weight = 1)
		filter_frame.columnconfigure(1, weight = 1)
		Tkinter.Radiobutton(filter_frame, text="Prior Day", variable=self.filter_select, value=0,command=self.change_filter).grid(row=1,column=0,sticky='w')
		Tkinter.Radiobutton(filter_frame, text="Prior Week", variable=self.filter_select, value=1,command=self.change_filter).grid(row=1,column=1,sticky='w')
		Tkinter.Radiobutton(filter_frame, text="Prior Month", variable=self.filter_select, value=2,command=self.change_filter).grid(row=2,column=0,sticky='w')
		Tkinter.Radiobutton(filter_frame, text="Prior Year", variable=self.filter_select, value=3,command=self.change_filter).grid(row=2,column=1,sticky='w')
		Tkinter.Radiobutton(filter_frame, text="All Data", variable=self.filter_select, value=4,command=self.change_filter).grid(row=3,column=0,sticky='w')
		Tkinter.Radiobutton(filter_frame, text="Custom Time", variable=self.filter_select, value=5,command=self.change_filter).grid(row=3,column=1,sticky='w')
		self.filter_select.set(0)
		self.filter_start.set((datetime.now()-timedelta(days=7)).strftime("%Y-%m-%d %H:%M"))
		self.filter_end.set(datetime.now().strftime("%Y-%m-%d %H:%M"))
		Tkinter.Label(filter_frame, text="Start").grid(row=4,column=0)
		Tkinter.Label(filter_frame, text="End").grid(row=4,column=1)
		start_entry=Tkinter.Entry(filter_frame, textvariable=self.filter_start,bg="white",state='disabled',justify='center')
		start_entry.grid(row=5,column=0)
		end_entry=Tkinter.Entry(filter_frame, textvariable=self.filter_end,bg="white",state='disabled',justify='center')
		end_entry.grid(row=5,column=1)
		#move code ending here to new class
		
		lt_lframe=Tkinter.LabelFrame(report_frame,text="Labels")
		lt_lframe.pack(side='bottom', fill='x')		
		lt_vscroll = Tkinter.Scrollbar(lt_lframe)
		lt_vscroll.pack(side='right', fill='y', padx=(0,2), pady=(0,2))			
		label_tree=LabelTree(lt_lframe,self.options)
		lt_lframe.pack(side='bottom', fill='both')		
		label_tree.config(height=8)
		label_tree.column("#0",stretch=True)
		label_tree.pack(side='bottom',fill='x',anchor='s', padx=(2,0), pady=(0,2))
		lt_vscroll.config(command=label_tree.yview)
		label_tree.configure(yscrollcommand=lt_vscroll.set)			
		
		tt_lframe=Tkinter.LabelFrame(report_frame,text="Report Types")
		tt_lframe.pack(side='bottom', fill='x')		
		tt_vscroll = Tkinter.Scrollbar(tt_lframe)
		tt_vscroll.pack(side='right', fill='y', padx=(0,2), pady=(0,2))			
		type_tree=ReportTypeTree(tt_lframe,self.options)
		tt_lframe.pack(side='bottom', fill='both')		
		type_tree.config(height=4)
		type_tree.column("#0",stretch=True)
		type_tree.pack(side='bottom',fill='x',anchor='s', padx=(2,0), pady=(0,2))
		tt_vscroll.config(command=type_tree.yview)
		type_tree.configure(yscrollcommand=tt_vscroll.set)		
		
		rt_lframe=Tkinter.LabelFrame(report_frame,text="Machine Structure")
		rt_lframe.pack(side='bottom', fill='both', expand=True)	
		rt_vscroll = Tkinter.Scrollbar(rt_lframe)
		rt_vscroll.pack(side='right', fill='y', padx=(0,2), pady=(0,2))				
		report_tree=StructureTree(rt_lframe,self.options)
		report_tree.column("#0",stretch=True)
		report_tree.pack(side='left',fill='both',expand=True, anchor='s', padx=(2,0), pady=(0,2))
		rt_vscroll.config(command=report_tree.yview)
		report_tree.configure(yscrollcommand=rt_vscroll.set)		
		
		report_tree.bind("<<TreeviewSelect>>",type_tree.update_reports,add="+")
		report_tree.bind("<<TreeviewSelect>>",lambda event: self.generate_button_state(),add="+")
		
		type_tree.bind("<<TreeviewSelect>>",label_tree.update_labels,add="+")
		type_tree.bind("<<TreeviewSelect>>",lambda event: self.generate_button_state(),add="+")		

		self.report_tree=report_tree
		self.type_tree=type_tree
		self.label_tree=label_tree
		self.generate_button=generate_button
		self.start_entry=start_entry
		self.end_entry=end_entry
		self.data_frame=data_frame
		#self.graph=None

	#function called when radio buttons change.  Will make custom dates disabled/normal
	def change_filter(self):
		if self.filter_select.get()==5:
			self.start_entry.config(state='normal')
			self.end_entry.config(state='normal')
		else:
			self.start_entry.config(state='disabled')
			self.end_entry.config(state='disabled')

	def generate_button_state(self):
		if self.label_tree.get_children(""):
			self.generate_button['state']='active'
		else:
			self.generate_button['state']='disabled'
		
	
	def generate_graph(self):
		
		#check what filter is selected and calculate end date and duration to subtract in sql statement
		filter=self.filter_select.get()
		if filter==0:
			enddate=datetime.now()
			startdate=enddate-timedelta(days=1)
		elif filter==1:
			enddate=datetime.now()
			startdate=enddate-timedelta(days=7)
		elif filter==2:
			enddate=datetime.now()
			startdate=enddate-timedelta(days=30)
		elif filter==3:
			enddate=datetime.now()
			startdate=enddate-timedelta(days=365)
		elif filter==4:
			enddate=datetime.now()
			startdate=datetime.strptime("1970-01-01 00:00","%Y-%m-%d %H:%M")
		elif filter==5:
			try:
				enddate=datetime.strptime(self.filter_end.get().strip(),"%Y-%m-%d %H:%M")
			except ValueError:
				tkMessageBox.showerror("Invalid Date","Invalid End Date\nPlease select valid date using format YYYY-MM-DD HH:MM", parent=self.an_win)
				return
			try:
				startdate=datetime.strptime(self.filter_start.get().strip(),"%Y-%m-%d %H:%M")
			except ValueError:
				tkMessageBox.showerror("Invalid Date","Invalid Start Date\nPlease select valid date using format YYYY-MM-DD HH:MM", parent=self.an_win)
				return
			if enddate<=startdate:
				tkMessageBox.showerror("Invalid Dates","End date must be after start date.", parent=self.an_win)
				return
	
		#set starttime.seconds to zero just to avoid confusion
		startdate=startdate.replace(second=0)
	
		#get selected LabelID/LabelName from label_tree id
		label=self.label_tree.selection()[0]
		LabelID=label.split("_")[1]
		LabelName=self.label_tree.item(label,'text')
		
		#get selected SensorName from structure_tree id
		sensor=self.report_tree.selection()[0]
		SensorName=self.report_tree.item(sensor,'text')
		#SensorID=sensor.split("_")[1]
	
		#get selected sensor LocationID from structure_tree id of parent
		location=self.report_tree.parent(sensor)
		#LocationID=location.split("_")[1]
		LocationName=self.report_tree.item(location,'text')
	
		#get ReportTypeID from report_type_tree
		rtype=self.type_tree.selection()[0]
		#ReportConfigID=rtype.split("_")[1]
		ReportTypeName=self.type_tree.item(rtype,'text')
	
		starttime=datetime.now()
	
		self.db = sqlite3.connect(self.options.dbfile)
		c=self.db.cursor()

		c.execute("""SELECT Timestamp, Value from v_reportData WHERE LabelID=? and timestamp>=? and timestamp<=? ORDER BY timestamp DESC, ReportID DESC""",(LabelID,startdate,enddate))
		results=c.fetchall()
		records=len(results)
		#need at least two results to make a GradeName
		if records<2:
			status="Plot failed. %d records found and two or more are required." % (records,)
			self.statustext.set(status)
			c.close()
			self.db.close()			
			return
		x,y=zip(*results)
		x=list(x)
		x=map(lambda j: datetime.strptime(j,"%Y-%m-%d %H:%M:%S"),x)
		y=list(y)
		c.close()
		self.db.close()
	
		endtime=datetime.now()
		elapsed=endtime-starttime
		status="%d records found in %s seconds." % (records,elapsed.total_seconds())
		self.statustext.set(status)		
		
		self.ax.clear()
		self.ax.plot(x,y)
		for tick in self.ax.get_xticklabels():
			tick.set_rotation(30)
			tick.set_horizontalalignment('right')		
		self.ax.set_title('%s - %s, %s'%(ReportTypeName,LocationName,SensorName))
		self.ax.set_ylabel(LabelName)
		
		#a.xaxis.set_major_locator(mdates.DayLocator())
		self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M:%S'))
		#a.xaxis.set_minor_locator(months)
		
		self.canvas.draw()
		
class OptionWindow:
	def __init__(self,parent,options):
		self.win=parent
		self.options=options
		self.win.geometry("+100+100")
		self.win.resizable(False,False)
		self.win.deiconify()
		
		self.gen_lframe=Tkinter.LabelFrame(self.win,text="General Options")
		self.gen_lframe.pack(padx=2, fill='x', expand=True)
		
		self.serial_lframe=Tkinter.LabelFrame(self.win,text="Serial Options")
		self.serial_lframe.pack(padx=2, fill='x', expand=True)
		
		self.button_frame=Tkinter.Frame(self.win)
		self.button_frame.pack(pady=2)
		
		self.gen_lframe.rowconfigure(0,weight=1,uniform='all')
		self.gen_lframe.rowconfigure(1,weight=1,uniform='all')
		#self.gen_lframe.rowconfigure(2,weight=1,uniform='all')
		self.serial_lframe.rowconfigure(0,weight=1,uniform='all')
		self.serial_lframe.rowconfigure(1,weight=1,uniform='all')
		self.serial_lframe.rowconfigure(2,weight=1,uniform='all')
		self.serial_lframe.rowconfigure(3,weight=1,uniform='all')
		
		self.entries={}
		self.variables={}

		Tkinter.Label(self.gen_lframe,text="Database File:", anchor='w').grid(row=0,column=0, sticky='wens', padx=2, pady=2)
		Tkinter.Label(self.gen_lframe,text="Display Max Lines:", anchor='w').grid(row=1,column=0, sticky='wens', padx=2, pady=2)
		Tkinter.Label(self.serial_lframe,text="COM Port:", anchor='w').grid(row=0,column=0, sticky='wens', padx=2, pady=2)
		Tkinter.Label(self.serial_lframe,text="Baud Rate:", anchor='w').grid(row=1,column=0, sticky='wens', padx=2, pady=2)
		Tkinter.Label(self.serial_lframe,text="Byte Size:", anchor='w').grid(row=1,column=2, sticky='wens', padx=2, pady=2)
		Tkinter.Label(self.serial_lframe,text="Parity:", anchor='w').grid(row=2,column=0, sticky='wens', padx=2, pady=2)
		Tkinter.Label(self.serial_lframe,text="Stop Bits:", anchor='w').grid(row=2,column=2, sticky='wens', padx=2, pady=2)
		Tkinter.Button(self.gen_lframe,text="Browse", command=self.browse_database, width=8,).grid(row=0,column=3, sticky='w', padx=1, pady=2)		
		Tkinter.Button(self.serial_lframe,text="Refresh", command=self.refresh_ports, width=8).grid(row=0,column=3, sticky='w', padx=1, pady=2)		
		Tkinter.Button(self.button_frame,text="Save", command=self.save, width=8).pack(side='left', padx=1)
		Tkinter.Button(self.button_frame,text="Cancel", command=self.cancel, width=8).pack(side='left', padx=1)
		
		self.entries['dbfile']=Tkinter.Entry(self.gen_lframe,state='readonly', readonlybackground='white', width=30)
		self.entries['dbfile'].grid(row=0,column=1,columnspan=2, sticky='wens', padx=2, pady=2)					
		self.entries['maxlines']=Tkinter.Spinbox(self.gen_lframe, width=8, from_=25, to=1000, increment=25, state='readonly', readonlybackground='white')
		self.entries['maxlines'].grid(row=1,column=1, sticky='wns', padx=2, pady=2)		
		self.entries['serial_port']=Combobox(self.serial_lframe, state='readonly')
		self.entries['serial_port'].grid(row=0,column=1, sticky='wens', padx=2, pady=2, columnspan=2)			
		self.entries['serial_baudrate']=Combobox(self.serial_lframe, width=8, state='readonly', values=(1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200))
		self.entries['serial_baudrate'].grid(row=1,column=1, sticky='wns', padx=2, pady=2)
		self.entries['serial_bytesize']=Combobox(self.serial_lframe, width=8, state='readonly', values=(5 , 6, 7, 8))
		self.entries['serial_bytesize'].grid(row=1,column=3, sticky='wns', padx=2, pady=2)
		self.entries['serial_parity']=Combobox(self.serial_lframe, width=8, state='readonly', values=('N', 'E', 'O', 'M', 'S'))
		self.entries['serial_parity'].grid(row=2,column=1, sticky='wns', padx=2, pady=2)
		self.entries['serial_stopbits']=Combobox(self.serial_lframe, width=8, state='readonly', values=(1, 2))
		self.entries['serial_stopbits'].grid(row=2,column=3, sticky='wns', padx=2, pady=2)		
		self.entries['serial_autoconnect']=Tkinter.Checkbutton(self.serial_lframe, text="Autoconnect")
		self.entries['serial_autoconnect'].grid(row=3,column=0, sticky='wns', padx=2, pady=2, columnspan=2)		
		
		for key in self.entries:
			widgettype=self.entries[key].winfo_class()
			if widgettype=='Checkbutton':
				self.variables[key]=Tkinter.IntVar()
				self.variables[key].set(getattr(self.options,key))
				self.entries[key]['variable']=self.variables[key]
			else:
				self.variables[key]=Tkinter.StringVar()
				self.variables[key].set(getattr(self.options,key))
				self.entries[key]['textvariable']=self.variables[key]
			
		self.refresh_ports()
	
	def save(self):
		for key,value in self.variables.iteritems():
			setattr(self.options,key,value.get())
		self.options.save()
		self.win.destroy()
	
	def cancel(self):
		self.win.destroy()
	
	def refresh_ports(self):
		comports = sorted(serial.tools.list_ports.comports(), key=lambda x: x[0])
		values=['None']
		for port,description,address in comports:
			values.append(port)
		self.entries['serial_port']['values']=values
	
	def browse_database(self):
		dbfile=askopenfilename(parent=self.win, title='Select Database',filetypes=[('Database File','*.db'),("All Files", "*.*"),],defaultextension = '.db')
		if dbfile is None:
			return
		if not os.path.isfile(dbfile):
			tkMessageBox.showerror("File Not Found","Database File Not Found", parent=self.win);
			return

		db=sqlite3.connect(dbfile)
		c=db.cursor()				
		
		try:
			c.execute("""SELECT DatabaseVersion FROM config WHERE rowid=1""")
		except sqlite3.OperationalError:
			tkMessageBox.showerror("Invalid Database Version","Database Version not found.", parent=self.win)
			return			
		result=c.fetchone()
		if result is not None:
			version=result[0]
		else:
			tkMessageBox.showerror("Invalid Database Version","Database Version not found.", parent=self.win)
			return
		if version==self.options.dbversion:
			self.variables['dbfile'].set(dbfile)
		else:
			tkMessageBox.showerror("Incorrect Database Version","Database Version does not match application version.", parent=self.win)
			return		
		
###Widget Classes###
	
class StructureTree(Treeview):
	
	def __init__(self,parent,options):
		Treeview.__init__(self,parent,selectmode="browse", show='tree')
		self.column("#0",stretch=True)
		self.options=options
		self.update_structure()
		
		
	def update_structure(self):
		self.delete(*self.get_children())
		self.db = sqlite3.connect(self.options.dbfile)
		c=self.db.cursor()
		c.execute("""SELECT MachineName FROM config WHERE rowid=1""")
		result=c.fetchone()
		if result is not None:
			result=result[0]
		if result is not None:
			MachineName=result
		else:
			MachineName="MACHINE"
		
		self.insert("", 'end', MachineName, text=MachineName, tags="Machine",open=True)
		
		c.execute("""SELECT DISTINCT LocationID,LocationName,SensorID,SensorName from v_structure ORDER BY LocationName,SensorID""")
		for LocationID,LocationName,SensorID,SensorName in c.fetchall():
			LocationLabel="Location_%d"%LocationID
			ReportTypeLabel="Location_%d"%LocationID
			LocationLabel="Location_%d"%LocationID
			if not self.exists("Location_%d"%LocationID):
				self.insert(MachineName, 'end', "Location_%d"%LocationID, text=LocationName, tags="Location")
			if not self.exists("Sensor_%d"%SensorID):
				self.insert("Location_%d"%LocationID, 'end', "Sensor_%d"%SensorID, text=SensorName,tags="Sensor")		
		c.close()
		self.db.close()
		
class ReportTypeTree(Treeview):
	
	def __init__(self,parent,options):
		Treeview.__init__(self,parent,selectmode="browse", show='tree')
		self.options=options
		self.column("#0",stretch=True)
		
	def update_reports(self,event):
		"""Method to be bound to by StructureTree <<Selection>> event.  Populates the ReportTypeTree with available report types."""
		#always change selection so it can trigger downstream Trees
		if self.get_children(""):
			self.selection_set(self.selection())
		self.delete(*self.get_children())
		self.db = sqlite3.connect(self.options.dbfile)
		c=self.db.cursor()
		call_widget=event.widget
		item=call_widget.selection()[0]
		
		if call_widget.tag_has("Sensor",item):
			SensorID=item.split("_")[1]
			LocationID=call_widget.parent(item).split("_")[1]
			c.execute("""SELECT DISTINCT ReportConfigID,ReportTypeName FROM v_structure WHERE LocationID=? and SensorID=? ORDER BY ReportTypeID""",(LocationID,SensorID))
			results=c.fetchall()
			if not results:
				self.generate_button.config(state='disabled')
				c.close()
				self.db.close()
				return
			#for ReportTypeID,ReportTypeName in results:
			for ReportConfigID,ReportTypeName in results:
				self.insert("", 'end', "ReportConfig_%d"%ReportConfigID, text=ReportTypeName)
			self.selection_set(self.get_children("")[0])
		elif call_widget.tag_has("Location",item):
			pass
		elif call_widget.tag_has("Machine",item):
			pass		
		else:
			tkMessageBox.showerror("Error","Invalid item tag",parent=call_widget)
		c.close()
		self.db.close()
class LabelTree(Treeview):

	def __init__(self,parent,options):
		Treeview.__init__(self,parent,selectmode="browse", show='tree')
		self.options=options
		self.column("#0",stretch=True)

	def update_labels(self,event):
		"""Method to be bound to by ReportTypeTree <<Selection>> event.  Populates the LabelTree with available labels."""
		self.delete(*self.get_children())
		self.db = sqlite3.connect(self.options.dbfile)
		c=self.db.cursor()
		call_widget=event.widget
		if call_widget.selection():
			item=call_widget.selection()[0]
		else:
			return
		ReportConfigID=item.split("_")[1]
		c.execute("""SELECT DISTINCT LabelID,LabelName FROM v_structure WHERE ReportConfigID=? ORDER BY LabelID""",(ReportConfigID,))
		results=c.fetchall()
		if not results:
			#self.generate_button.config(state='disabled')
			c.close()
			self.db.close()
			return
		#for ReportTypeID,ReportTypeName in results:
		for LabelID,LabelName in results:
			self.insert("", 'end', "Label_%d"%LabelID, text=LabelName)
		self.selection_set(self.get_children("")[0])
		c.close()
		self.db.close()
		
class Options:
	"""Class to hold all user defined option"""
	
	def __init__(self):
		"""Class Options init function"""
		path=os.path.dirname(os.path.realpath(__file__))
		path = '/'.join(path.split('\\'))		
		self.configfile=path+"/"+"config.xml"
		
		###LOAD IN DEFAULTS FIRST###
		
		##Hard Coded##
		self.dbversion="1.1"
		
		##general##
		self.dbfile=path+"/"+"stk.db"		
		self.maxlines=500
		
		##serial#
		self.serial_port=None
		self.serial_baudrate=9600
		self.serial_bytesize=8
		self.serial_parity='N'
		self.serial_stopbits=1
		self.serial_autoconnect=False
		
		#if there was no config file, save the defaults
		if not self.load():
			self.save()
		
	def load(self):
		"""Function to load options from config.xml"""
		if not os.path.isfile(self.configfile):
			return False
		options=etree.parse(self.configfile).getroot()
		for child in options:
			#try is to deal with string.  eval on a string is an error
			try:
				value=eval(child.text)
			except:
				value=child.text
			if hasattr(self,child.tag):
				setattr(self,child.tag,value)
			#print child.tag,value,getattr(self,child.tag),type(getattr(self,child.tag))
		return True
			
	def save(self,option=None):
		"""Function to save current option(s) to config.xml"""
		if option is None:
			root = etree.Element("options")
			for key, value in sorted(vars(self).iteritems()):
				if key!='configfile' and key!='dbversion': #skip these ones.
					etree.SubElement(root,key).text=str(value)
					
			et=etree.ElementTree(root)
			prettyxml = minidom.parseString(etree.tostring(root)).toprettyxml()
			with open(self.configfile, "w") as f:
				f.write(prettyxml)	
	
		else:
			if not os.path.isfile(self.configfile):
				return			
			tree=etree.parse(self.configfile)
			options=tree.getroot()
			if options.find(option) is not None:
				options.find(option).text=str(getattr(self,option))
				tree.write(self.configfile)			
			else:
				return
			
class Report:
	
	def __init__(self,report):
		self.ReportTypeName=report['name']
		self.LocationName=report['location']
		self.Timestamp=report['timestamp']
		self.GradeCode=report['gradecode']
		self.GradeName=report['gradename']
		self.SensorName=report['data'][0]['sensor']
		self.LabelNames=report['data'][0]['labels']
		self.Values=report['data'][0]['values']
		
			
if __name__ == "__main__":
	main()
