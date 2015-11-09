#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Show main data and give following options:
# Create a new Student
# Delete a Student
# Import mass-Students with csv 
#
#Import Glade3
from gi.repository import Gtk
from gi.repository import Gdk

#Import Messagebox and Tkinter
import tkMessageBox
import Tkinter

#Import File-Read-Packages
from sys import argv

#Import SQLIte
import sqlite3 as lite

#import sql-class
from dataop import DataOp

#import csv
import csv

class ShowData():	

	#First Method called ba Mainclasses.py
	#Needs the actual window-object to change label "view"
	def start(self, classname, builder, window):

		#Databaseconnection
		dataop = DataOp()
		con = dataop.opendatabase(classname)

		#Functions for adding, importing and editing students
		def do_addstudent(*args):

			#Function to save a new Student
			def save_new_student(*args):
				name = builder.get_object("student_postname").get_text().decode("utf-8")
				prename = builder.get_object("student_prename").get_text().decode("utf-8")
				mail = builder.get_object("student_mail").get_text().decode("utf-8")
				
				#Checking the data
				if len(name) == 0 or len(prename) == 0:
					messWindow = Tkinter.Tk()
					messWindow.wm_withdraw()
					tkMessageBox.showinfo("Falsche Eingabe", "Bitte mindestens Vorname und Nachname eingeben.")
					messWindow.destroy()	

				#Check of so save new student to database
				else:
					#Insert all Datas
					cur = con.cursor()
					#Count existing Students in the Datbase
					
					newid = dataop.getdata(con, "select count(id) from students", None)
					if newid.fetchone()[0] == 0:
						cur.execute("insert into students(id, name, prename, mail) values (0, ?, ?, ?);", (name, prename, mail,))
					else:
						cur.execute("insert into students(id, name, prename, mail) values ((SELECT max(id) FROM students) + 1, ?, ?, ?);", (name, prename, mail,))		
					con.commit()
					#Destroy Input-Window
					addstudentwindow.destroy()
					#Reload the DataGrid					
					fillDataGrid()

			#Show New-Student-Popup
			builder.add_from_file("gui/NewStudentPop.glade")
			addstudentwindow = builder.get_object("addstudentwindow")
			addstudentwindow.show_all()

			savebutton = builder.get_object("addstudent_save")
			savebutton.connect("clicked", save_new_student)

		#Function to save a new Student
		def save_new_student_csv(postname, prename, mail):
			#Insert all Datas
			cur = con.cursor()
			#Count existing Students in the Datbase
			newid = dataop.getdata(con, "select count(id) from students", None)
			if newid.fetchone()[0] == 0:
				cur.execute("insert into students(id, name, prename, mail) values (0, ?, ?, ?);", (postname, prename, mail,))
			else:
				cur.execute("insert into students(id, name, prename, mail) values ((SELECT max(id) FROM students) + 1, ?, ?, ?);", (postname, prename, mail,))		
			
			con.commit()
			#Reload the DataGrid					
			fillDataGrid()
			
		#Destroy checkwindow
		def quit_checkwindow(self, another, checkwindow):
			checkwindow.destroy()

		#Destroy the CSV-Window
		def abort_savecsv(self, importcsvwin):
			importcsvwin.destroy()

		#Save all new Students
		def savecsv(self, importcsvwin, counter):
			#Getting the Students-Data from the Grid
			grid = builder.get_object("newstudents")
			for newstu in range(counter):
				if newstu > 0:					
					prename = grid.get_child_at(3, newstu).get_text().decode("utf-8")
					postname = grid.get_child_at(5, newstu).get_text().decode("utf-8")
					mail = grid.get_child_at(7, newstu).get_text().decode("utf-8")
					save_new_student_csv(postname, prename, mail)	
			
			#Reload the Grid
			fillDataGrid()
			importcsvwin.destroy()

		#Import a lot of students from a csv-File
		def do_importstudents(*args):
			dialog = Gtk.FileChooserDialog("Klassendatei wählen", None, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
			response = dialog.run()

			if response == -6:
				dialog.destroy()
			elif response == -5:
				#Read CSV-File				
				filename = argv
				filename = str(dialog.get_filename())				
				cr = csv.reader(open(filename,"rb"))

				#Load GUI
				builder.add_from_file("gui/ImportCSV.glade")
				importcsvwin = builder.get_object("importcsv")
				csvgrid = builder.get_object("newstudents")
				
				#Read all Data and prepare Check-Window
				counter = 1
				for row in cr:
					templabel_numb = Gtk.Label(str(counter) + "." )
					templabel_postname = Gtk.Label(str(row[0]))
					templabel_prename = Gtk.Label(str(row[1]))
					templabel_mail = Gtk.Label(str(row[2]))
					
					space1 = Gtk.Label("   ")
					space2 = Gtk.Label("   ")
					space3 = Gtk.Label("   ")

					#If 2nd row --> make it grey :)
					if counter % 2 != 0:
						templabel_numb.modify_bg(0, Gdk.Color(52000, 52000, 52000))
						templabel_postname.modify_bg(0, Gdk.Color(52000, 52000, 52000))
						templabel_prename.modify_bg(0, Gdk.Color(52000, 52000, 52000))
						templabel_mail.modify_bg(0, Gdk.Color(52000, 52000, 52000))
						space1.modify_bg(0, Gdk.Color(52000, 52000, 52000))
						space2.modify_bg(0, Gdk.Color(52000, 52000, 52000))
						space3.modify_bg(0, Gdk.Color(52000, 52000, 52000))
					
					#Attach all Labels to the Grid
					csvgrid.attach(templabel_numb, 1, counter, 1, 1)
					csvgrid.attach(space1, 2, counter, 1, 1)
					csvgrid.attach(templabel_postname, 3, counter, 1, 1)
					csvgrid.attach(space2, 4, counter, 1, 1)
					csvgrid.attach(templabel_prename, 5, counter, 1, 1)
					csvgrid.attach(space3, 6, counter, 1, 1)
					csvgrid.attach(templabel_mail, 7, counter, 1, 1)
					counter = counter + 1
				
				#Adding Button-Functionality
				abort = builder.get_object("abort")
				abort.connect("clicked", abort_savecsv, importcsvwin)

				savecsvbutton = builder.get_object("savecsv")
				savecsvbutton.connect("clicked", savecsv, importcsvwin, counter)

				#Show New-Student-Popup
				importcsvwin.show_all()
		    	dialog.destroy()


		#Save Update Data from Student
		def saveupdatedata(self, id, windowtodestroy):
			name = builder.get_object("student_postname").get_text().decode("utf-8")
			prename = builder.get_object("student_prename").get_text().decode("utf-8")
			mail = builder.get_object("student_mail").get_text().decode("utf-8")
			
			#Checking the data
			if len(name) == 0 or len(prename) == 0:
				messWindow = Tkinter.Tk()
				messWindow.wm_withdraw()
				tkMessageBox.showinfo("Falsche Eingabe", "Bitte mindestens Vorname und Nachname eingeben.")
				messWindow.destroy()	

			#Check of so save new student to database
			else:
				#Update all Datas
				cur = con.cursor()
				cur.execute("UPDATE students SET name=?, prename=?, mail=? WHERE id=?", (name, prename, mail, id)) 
				con.commit()
				#Destroy Input-Window
				windowtodestroy.destroy()
				#Reload the DataGrid					
				fillDataGrid()

		def deletestudent(self, id, prename, postname):
			messWindow = Tkinter.Tk()
			messWindow.wm_withdraw()
			result = tkMessageBox.askokcancel("Warnung", "ACHTUNG! Alle Daten von " + prename.encode("utf-8") + " " + postname.encode("utf-8") + " werden UNWIDERRUFLICH gelöscht. Fortfahren?")
			messWindow.destroy()

			#Check for deleting or not
			if result == True:
				#Delete True - Call main Student-Delete-Funktion and give ID
				dataop.deleteStudentComplete(con, id)
				fillDataGrid()

		#Changes Data from a Student, needs Button and id from a student
		def changedata(self, id, data_post, data_pre, data_mail):
			builder.add_from_file("gui/NewStudentPop.glade")
			addstudentwindow = builder.get_object("addstudentwindow")
			
			#Adding Data into Textfields
			prename = builder.get_object("student_prename")
			postname = builder.get_object("student_postname")
			mail = builder.get_object("student_mail")
			
			prename.set_text(data_pre.encode("utf-8"))		
			postname.set_text(data_post.encode("utf-8"))
			mail.set_text(data_mail.encode("utf-8"))

			#Get Button-Object
			savedata = builder.get_object("addstudent_save")
			savedata.connect("clicked", saveupdatedata, id, addstudentwindow)

			#Show New-Student-Popup
			addstudentwindow.show_all()

		#Fill the Grid with all Data from the actual database resp. Class		
		def fillDataGrid(*args):
			
			#Get all the Grids :)
			datagrid_buttons = builder.get_object("datagrid_buttons")				
			newviewgrid = builder.get_object("datagrid")

			#Clear the grid
			for child in newviewgrid.get_children():
				newviewgrid.remove(child)

			#Clear the button-grid
			for child in datagrid_buttons.get_children():
				datagrid_buttons.remove(child)			
			
			#Adding Buttons in Top-Area to add Students or import a csv-List (LATER!!)
			addstudents = Gtk.Button.new_with_label("Neuer Schüler")
			addstudents.connect("clicked", do_addstudent)
			datagrid_buttons.attach(addstudents, 0, 1, 1, 1)
			
			importstudents = Gtk.Button("Import CSV")
			datagrid_buttons.attach(importstudents, 1, 1, 1, 1)
			importstudents.connect("clicked", do_importstudents)

			#Adding Studentsnames - Postname, Prenames, Numbers and Buttons
			datas = dataop.getdata(con, "select id, name, prename, mail from students order by 2 asc", None)
			#Startfield of Rows
			startfield_rows = 1
			for row in datas.fetchall():
				templabel_numbers = Gtk.Label()
				templabel_postname = Gtk.Label()
				templabel_prename = Gtk.Label()

				templabel_numbers.set_text("     " + str(startfield_rows) + ". ")
				templabel_postname.set_text(row[1].encode("utf-8") + " ")
				templabel_prename.set_text(row[2].encode("utf-8") + " ")
				
				#COLOR 0-65535 Gdk.Color(RED, GREEN, BLUE)
				if startfield_rows % 2 != 0:
					templabel_postname.modify_bg(0, Gdk.Color(52000, 52000, 52000))
					templabel_prename.modify_bg(0, Gdk.Color(52000, 52000, 52000))
					templabel_numbers.modify_bg(0, Gdk.Color(52000, 52000, 52000))

				newviewgrid.attach(templabel_postname, 1, startfield_rows, 1, 1)
				newviewgrid.attach(templabel_prename, 3, startfield_rows, 1, 1)
				newviewgrid.attach(templabel_numbers, 0, startfield_rows, 1, 1)

				#Button to change
				changebutton = Gtk.Button()
				changebutton.set_name("button_" + str(row[0]))
				image = Gtk.Image()
				image.set_from_file("icons/gear74.png")
				changebutton.set_size_request(10,10)
				changebutton.set_image(image)				
				#Button to Label
				newviewgrid.attach(changebutton, 4, startfield_rows, 1, 1)
				#Add Action to the Button with id from actual student
				changebutton.connect("clicked", changedata, row[0], row[1], row[2], row[3])
				
				#Button to delete all Students Data
				deletebutton = Gtk.Button()
				deletebutton.set_name("delete_" + str(row[0]))
				image = Gtk.Image()
				image.set_from_file("icons/cancel19.png")
				deletebutton.set_size_request(10,10)
				deletebutton.set_image(image)				
				#Button to Label
				newviewgrid.attach(deletebutton, 5, startfield_rows, 1, 1)
				#Add Action to the Button with id from actual student
				deletebutton.connect("clicked", deletestudent, row[0], row[1], row[2])

				startfield_rows = startfield_rows + 1

			#Show the window		
			window.show_all()

		#Fill the Grid for the first time and call this method to reload
		fillDataGrid()
		





