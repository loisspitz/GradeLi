#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Opens a new Class and check if it is already open
#
#Import Glade3
from gi.repository import Gtk

#Import Messagebox and Tkinter
import tkMessageBox
import Tkinter

#Import SQLIte
import sqlite3 as lite

#import sql-class
from dataop import DataOp
from mainclasses_showdata import ShowData
from mainclasses_showunits import ShowUnits
from mainclasses_shownotes import ShowNotes
from mainclasses_showindi import ShowIndi
from mainclasses_showoverview import ShowOverview

classname = None

class MainClasses():	

	#First Method called by newclass.py
	def start(self, classname):
		
		#Overload classname
		classname = classname

		#Defining import Objects for Window and Builder
		builder = Gtk.Builder()
		builder.add_from_file("gui/Classes.glade")
		newclasswindow = builder.get_object("window_mc")

		#Giving a Messagebox 
		def msgbox(messtitle, message):
			messWindow = Tkinter.Tk()
			messWindow.wm_withdraw()
			tkMessageBox.showinfo(messtitle, message)
			messWindow.destroy()	
			newclasswindow.destroy()

		#Close Window and delete Classname from Control-Database
		#Gets classname
		def close_window_classes(*args):
			dataop = DataOp()			
			con = dataop.opencontroldata(classname)
			dataop.executequery(con, "DELETE FROM gradelicontrol WHERE openclass = ?", classname)
			newclasswindow.destroy()

		#																		#
		#																		#		
		############################### FUNCTION SECTION START ##################
		#																		#	
		#																		#

		#Data 
		#Creates a new Objects to make this class smaller :)
		#Give the Window-Object to make changes on GUI (Grid "datagrid") possible
		def do_data(*args):
			showdata = ShowData()
			showdata.start(classname, builder, newclasswindow)

		#Unit-View
		def do_units(*args):				
			showunits = ShowUnits()
			showunits.start(classname, builder, newclasswindow)

		#Notes
		def do_notes(*args):
			shownotes = ShowNotes()
			shownotes.start(classname, builder, newclasswindow)

		#Individual View
		def do_indi(*args):
			showindi = ShowIndi()
			showindi.start(classname, builder, newclasswindow)

		#Overview
		def do_overview(*args):
			showoverview = ShowOverview()
			showoverview.start(classname, builder, newclasswindow)

		#																	  #
		#																	  #		
		############################### FUNCTION SECTION END ##################
		#																	  #	
		#																	  #		


		#Check for already opened
		dataop = DataOp()			
		con = dataop.opencontroldata()
		classesopen = dataop.getdata(con, "select * from gradelicontrol", None)
		
		#If Class open do not open it againg and throw a message-window
		# If Class not open open the class and save the name in the database
		checked_open_class = False

		for row in classesopen.fetchall():
			if row[1] == classname:
				msgbox("Klasse geöffnet", "Die ausgewählte Klasse ist bereits geöffnet.")
				checked_open_class = True			
		
		if checked_open_class == False:
			dataop = DataOp()
			dataop.executequery(con, "INSERT INTO gradelicontrol(ID, openclass) VALUES((SELECT max(id) FROM gradelicontrol) + 1, ?)", classname)
			classlabel = builder.get_object("label_classname")
			classlabel.set_text(classname)			
			newclasswindow.connect("delete-event", close_window_classes)

			#Save view-label
			viewlabel = builder.get_object("view")

			#Adding Actions to the Buttons
			#Data
			show_data = builder.get_object("show_data")
			show_data.connect("clicked", do_data)

			#Units
			show_units = builder.get_object("show_units")
			show_units.connect("clicked", do_units)

			#Notes
			show_notes = builder.get_object("show_notes")
			show_notes.connect("clicked", do_notes)

			#Individual View
			show_indi = builder.get_object("show_indi")
			show_indi.connect("clicked", do_indi)

			#Overview
			show_overview = builder.get_object("show_overview")
			show_overview.connect("clicked", do_overview)

			#GUI Loading
			newclasswindow.show_all()

			#Call do_data to prevent placeholderviewing
			do_data()
			

