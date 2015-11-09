#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This Class creates a new Database-File which represents a new Class.
# The User can input an Class-Name and after the OK the script creates
# a Database-File with this Name in "database". After that the new Class
# is added to the comboboxand the active Item is always the first.
#
# @param
# window-Object and Builder-Object (Gtk)
#

#Import OS
import glob

#Import Glade3
from gi.repository import Gtk

#Import Messagebox and Tkinter
import tkMessageBox
import Tkinter

#Import Databaseoperations
from dataop import DataOp

#Import os-Operations
import os.path

#Import SQLIte
import sqlite3 as lite
from mainclasses import MainClasses

class NewClass():			

	#Method which starts the NewClass-Logic
	def start(self, window, builder):
		
		
		#This Method close the little pop-up-window
		def close_window_newclass(*args):
			#Close the Window
			newclasswindow.destroy()

		#Create a new Database with Name given from the textfield
		#Add the Name to the Combobx in the MainWindow and Activate the first Item
		def create_new_class(*args):
			#Getting the Textfield
			newclassname = builder.get_object("class_name_text")
			#saving the Name			
			classname = newclassname.get_text()

			#If Classname ist Empty than Error-Message
			if len(classname) == 0:
				messWindow = Tkinter.Tk()
				messWindow.wm_withdraw()
				tkMessageBox.showinfo("Ungültiger Name", "Bitte gültigen Namen eingeben (Keine Sonderzeichen! Bsp. 11_GkInf1)!")
				messWindow.destroy()	
			else:
				#Create new Database-File in "database" if not exists		
				############### THE DEFAULT-PATH COULD BE CHANGE LATER IN A FILE #########
				#
				#
				#
				default_path = "../GradeLi Classes/"
				#
				#
				#
				#########################################################################
				if os.path.isfile(default_path + classname + ".db") == True:		
					messWindow = Tkinter.Tk()
					messWindow.wm_withdraw()
					tkMessageBox.showinfo("Name vergeben", "Name der Klasse ist bereits vergeben. Bitte anderen Namen nutzen oder alte Klasse verschieben.")
					messWindow.destroy()	
					newclasswindow.destroy()
				else:
					#Close Popup-Window
					close_window_newclass()

					#Creating the new Class-Database
					dataop = DataOp()			
					con = dataop.newdatabase(classname)
					dataop.closedatabase(con)

					#Adding Class to Combobox - Sorting after restart
					classesbox = builder.get_object("classes")
					classesbox.append_text(classname)

					#Saving new Classname
					new_class_name = classname

					#Make Loadingbutton Clickable
					loadclass = builder.get_object("loadclass")
					loadclass.set_sensitive(True)

					#Activate always the first Item in the List
					classesbox.set_active(0)

					#Open new Window with new Class-Database
					newmainclass = MainClasses()
					newmainclass.start(new_class_name)
					
		#
		#	Standard-Logic to create the Window, Connect Actions and
		#	add Buttons		
		#		
		#Builderobject from GradLi
		builder.add_from_file("gui/NewClass.glade")
		
		#Window-Object
		newclasswindow = builder.get_object("window_newclass")
		
		#Prepare for Exit-Click
		newclasswindow.connect("delete-event", close_window_newclass)

		#Function for Abort-Button
		abortbutton = builder.get_object("abort")
		abortbutton.connect("clicked", close_window_newclass)

		#Function for NewClass-Button
		newclassbutton = builder.get_object("createnewclass")
		newclassbutton.connect("clicked", create_new_class)

		#GUI Loading
		newclasswindow.show_all()

