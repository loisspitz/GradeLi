#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This Class starts the Main-Window where
# the User choose a Class or create a new 
# Class. If the user wants to create a new
# class this file opens next files to do that.
#
#Import Glade3
from gi.repository import Gtk

#Import glob to read all Databases
import glob

#Messagebox and Tkinter
import tkMessageBox
import Tkinter

#Import SQLIte
import sqlite3 as lite

#Import os-Operations
import os

#Import own Scripts
from script.newclass import NewClass
from script.mainclasses import MainClasses
from script.dataop import DataOp

class gradeli():
	#Inital program-start
	def __init__(self):

		#Prepare to create a new Class
		def createnewclass(button):		
			#Creata a new Instance of NewClass			
			newclassobject = NewClass()
			#Start Logic of NewClass and give window and Builder
			#to get Access to the Combobox for adding new Class after Process
			newclassobject.start(window, builder)				
			
		#Loading all Classes in dir "databases"
		def loadingClasses(builder, window):
			#Reading all Databases in Dir "database"
			############### THE DEFAULT-PATH COULD BE CHANGE LATER IN A FILE #########
			#
			#
			#
			default_path = "../GradeLi Classes/"
			#
			#
			#
			#########################################################################
			classes = glob.glob(default_path + "*.db")
			
			
			#If there is more than one Database fill the Drop-Down-List:
			if len(classes) > 0 :
				classes_clear = [0 for i in range(len(classes))]
				#For every Databse split, remove .db and show in gui
				classesbox = builder.get_object("classes")		
				
				#Read all Databases and prepare adding combobox
				for index in range(len(classes)):
					#Split the Database-Names
					classes_split = classes[index].split("/")
					#Remove .db
					classes_clear[index] = classes_split[2].split(".")
					#Get name of Database after here: classes_clear[index][0]			
					
				
				#Sort all Classnames and add them to the combobox
				classes_clear.sort()
				for index in range(len(classes)):
					classesbox.append_text(classes_clear[index][0])

				#First Database in the Combobox is set to active
				classesbox.set_active(0)

				#Making the LoadClass-BUtton clickable
				loadclass = builder.get_object("loadclass")
				loadclass.set_sensitive(True)
			else:
				#Show Messagewindow with Information about zero Classes
				messWindow = Tkinter.Tk()
				messWindow.wm_withdraw()
				#Create default Dir if not exist
				if not os.path.exists(default_path):
					os.makedirs(default_path)				

				tkMessageBox.showinfo("Keine Klassen gefunden", "Keine Klassen angelegt. Bitte neue Klassen anlegen! Ordner \"GradeLis Classes\" erstellt.")
				
				#LoadLcasss-Button not clickable
				loadclass = builder.get_object("loadclass")
				loadclass.set_sensitive(False)
				messWindow.destroy()	
		
		#Loading an existing Class
		def loadclass(button):
			#Open new Window with new Class-Database			
			classname = None			
			#Getting Classname from Combobox
			classescombo = builder.get_object("classes")		
			model = classescombo.get_model()
			classname = model[classescombo.get_active()][0]			
			#Starting new Window with active classname			           	
			newmainclass = MainClasses()			
			#Starting the Class-Window
			newmainclass.start(classname)
		
		#Object to Build the Windows
		builder = Gtk.Builder()
		#Loading Glade-File
		builder.add_from_file("gui/MainWindow.glade")
		
		window = builder.get_object("window_main")
		
		#Prepare for Window-Logic
		loadingClasses(builder, window)
		#Connect to Buttons and add Action
		#NewClassButton
		newclassbutton = builder.get_object("newclass")
		newclassbutton.connect("clicked", createnewclass)

		#Load existing ClassButton
		loadclassbutton = builder.get_object("loadclass")
		loadclassbutton.connect("clicked", loadclass)

		
		#Prepare for Exit-Click
		window.connect("delete-event", Gtk.main_quit)
		#Loading Classes or throw a message
		
		#Controldatabase anlegen
		#Check if Database "GradeLiControl.db" exists (if no create it and insert first item)
		#
		# GradeLiControl saves open Classes to prevent for multiple-Opening		
		dataop = DataOp()			
		if os.path.isfile("GradeLiControl.db") == False:			
			con = dataop.opencontroldata()
			dataop.executequery(con, "create table gradelicontrol (ID INT PRIMARY KEY NOT NULL, openclass TEXT);", None)
			dataop.executequery(con, "INSERT INTO gradelicontrol(ID, openclass) VALUES(1, 'GradeLiControl First')", None)
			dataop.closedatabase(con)
		else:			
			con = dataop.opencontroldata()	
			dataop.executequery(con, "drop table gradelicontrol", None)	
			dataop.executequery(con, "create table gradelicontrol (ID INT PRIMARY KEY NOT NULL, openclass TEXT);", None)
			dataop.executequery(con, "INSERT INTO gradelicontrol(ID, openclass) VALUES(1, 'DO_NOT_DROP_THIS_ITEM')", None)
			dataop.closedatabase(con)		
		
		#GUI Loading
		window.show_all()
		#Start Program
		Gtk.main()	

#Create Object and Start the Program
startGradeLi = gradeli()