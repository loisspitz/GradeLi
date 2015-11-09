#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Show Units and implements add/change/delete - Functions
#

#Import Glade3
from gi.repository import Gtk
from gi.repository import Gdk

#Import Messagebox and Tkinter
import tkMessageBox
import Tkinter

#Import SQLIte
import sqlite3 as lite

#import sql-class
from dataop import DataOp

class ShowUnits():	

	#First Method called ba Mainclasses.py
	#Needs the actual window-object to change label "view"
	def start(self, classname, builder, window):

		#Databaseconnection
		dataop = DataOp()
		con = dataop.opendatabase(classname)

		#Get all the Grids :)
		datagrid_buttons = builder.get_object("datagrid_buttons")				
		newviewgrid = builder.get_object("datagrid")

		#Delete a UNit
		def deleteunit(self, id, year, month, day):
			messWindow = Tkinter.Tk()
			messWindow.wm_withdraw()
			result = tkMessageBox.askokcancel("Warnung", "ACHTUNG! Alle Daten der Stunde vom " + str(day) + "." + str(month) + "." + str(year) + " werden UNWIDERRUFLICH gelöscht. Fortfahren?")
			messWindow.destroy()

			#Check for deleting or not
			if result == True:
				#Delete True - Delete the Unit and reload the Grid
				dataop.deleteUnitComplete(con, id)
				fillDataGrid()

		#Save Updatet Information of a Unit
		def saveupdateunit(self, id, updateunitwindow):
			#Get new Title
			date = builder.get_object("unit_date").get_date()		
			title = builder.get_object("unit_title").get_text().decode("utf-8")
			#Saving changes
			
			cur = con.cursor()
			cur.execute("UPDATE units SET year=?, month=?, day=?, title=? WHERE id=?", (date[0], date[1] + 1, date[2], title, id)) 
			con.commit()		

			updateunitwindow.destroy()
			fillDataGrid()

		#Change a unit
		def changeunit(self, id, year, month, day, title):
			builder.add_from_file("gui/NewUnitPopUpdate.glade")
			updateunitwindow = builder.get_object("updateunitwindow")
			
			#Select actual Date in Calender
			date = builder.get_object("unit_date")			
			date.select_month(month - 1, year)
			date.select_day(day)

			titlewidget = builder.get_object("unit_title")
			titlewidget.set_text(title.encode("utf-8"))
			
			#Get Button-Object
			savedata = builder.get_object("updateunit_save")
			savedata.connect("clicked", saveupdateunit, id, updateunitwindow)

			#Show New-Student-Popup
			updateunitwindow.show_all()
				
		#Save new Unit
		def dosaveunit(self, unitwindow):
			#Getting Date and Title
			#Getting Date: Yeahr date[0] month[1] day[2]
			date = builder.get_object("newunit_date").get_date()
			title = builder.get_object("newunit_title").get_text().decode("utf-8")
			
			#Make the Month userfriendly :)
			month = int(date[1]) + 1
			
			#Saving new Unit into Database
			cur = con.cursor()
			
			#Count existing Units in the Datbase
			newid = dataop.getdata(con, "select count(id) from units", None)
			if newid.fetchone()[0] == 0:
				cur.execute("insert into units(id, year, month, day, title) values (0, ?, ?, ?, ?);", (int(date[0]), int(month), int(date[2]), title,))
			else:
				cur.execute("insert into units(id, year, month, day, title) values ((SELECT max(id) FROM units) + 1, ?, ?, ?, ?);", (date[0], int(month), date[2], title,))			
			
			#New Unit-ID: (SELECT max(id) FROM units)
			#Get all Students
			datas_allstu = dataop.getdata(con, "select id from students order by name asc", None)

			#For all Students add UnitStatus-Entry in Database with actual Unit-ID
			newid_stuunit = dataop.getdata(con, "select count(id) from status_stu_unit", None)
			newid_unitid = dataop.getdata(con, "SELECT max(id) FROM units", None)
			
			#New ID's
			unitid = newid_unitid.fetchone()[0]
			unitcount = newid_stuunit.fetchone()[0]			

			for stuall in datas_allstu.fetchall():
				if unitcount == 0:
					cur.execute("insert into status_stu_unit(id, unitid, studentid, status) values (0, ?, ?, 5);", (unitid, int(stuall[0]),))					
					unitcount = unitcount + 1
				else:
					cur.execute("insert into status_stu_unit(id, unitid, studentid, status) values ((SELECT max(id) FROM status_stu_unit) + 1, ?, ?, 5);", (unitid, int(stuall[0]),))					
					
			#Destroy the Add-Unit-Window
			unitwindow.destroy()
			#Reload the Data-Grid _ Units will be load there to
			fillDataGrid()			

		#Updatefunction for Students Unit-Status
		def updateUnitStu(self, studentid, unitid, newstatus, buttongrid):
			#Updating Data in Database
			cur = con.cursor()
			cur.execute("update status_stu_unit set status=? where unitid=? and studentid=?", (newstatus, unitid, studentid,)) 
			con.commit()	

			#Images
			ue_b = Gtk.Image()
			ue_r = Gtk.Image()
			ue_b.set_from_file("icons/quest_black.png")
			ue_r.set_from_file("icons/quest_red.png")

			#OK leaved
			e_b = Gtk.Image()
			e_g = Gtk.Image()
			e_b.set_from_file("icons/ok_black.png")
			e_g.set_from_file("icons/ok_green.png")

			#MIddle good work
			middle_b = Gtk.Image()
			middle_g = Gtk.Image()
			middle_b.set_from_file("icons/middle_black.png")
			middle_g.set_from_file("icons/middle_green.png")

			#One Plus Work
			plus_b = Gtk.Image()
			plus_g = Gtk.Image()
			plus_b.set_from_file("icons/plus_black.png")
			plus_g.set_from_file("icons/plus_green.png")

			#PLusPlus Work
			plusplus_b = Gtk.Image()
			plusplus_g = Gtk.Image()
			plusplus_b.set_from_file("icons/plusplus_black.png")
			plusplus_g.set_from_file("icons/plusplus_green.png")

			#One Minus Work
			minus_b = Gtk.Image()
			minus_g = Gtk.Image()
			minus_b.set_from_file("icons/minus_black.png")
			minus_g.set_from_file("icons/minus_green.png")

			#MinusMinus Work
			minusminus_b = Gtk.Image()
			minusminus_g = Gtk.Image()
			minusminus_b.set_from_file("icons/minusminus_black.png")
			minusminus_g.set_from_file("icons/minusminus_green.png")

			#School-Event
			school_b = Gtk.Image()
			school_g = Gtk.Image()
			school_b.set_from_file("icons/school_black.png")
			school_g.set_from_file("icons/school_green.png")

			#Changings Button-Images to show right color and button
			for button in buttongrid.get_children():				
				if button.get_name() == "ue":
					if newstatus == 0:
						button.set_image(ue_r)	
					else:
						button.set_image(ue_b)			

				if button.get_name() == "e":
					if newstatus == 1:
						button.set_image(e_g)	
					else:
						button.set_image(e_b)			

				if button.get_name() == "school":
					if newstatus == 2:
						button.set_image(school_g)	
					else:
						button.set_image(school_b)	

				if button.get_name() == "minusminus":
					if newstatus == 3:
						button.set_image(minusminus_g)	
					else:
						button.set_image(minusminus_b)				

				if button.get_name() == "minus":
					if newstatus == 4:
						button.set_image(minus_g)	
					else:
						button.set_image(minus_b)					

				if button.get_name() == "mid":
					if newstatus == 5:
						button.set_image(middle_g)	
					else:
						button.set_image(middle_b)		

				if button.get_name() == "plus":
					if newstatus == 6:
						button.set_image(plus_g)	
					else:
						button.set_image(plus_b)	

				if button.get_name() == "plusplus":
					if newstatus == 7:
						button.set_image(plusplus_g)	
					else:
						button.set_image(plusplus_b)			
				
		#Showing the New-Unit-Popup
		def do_addunit(*args):
			builder.add_from_file("gui/NewUnitPop.glade")
			addunitwindow = builder.get_object("addunitwindow")						

			addunitbutton = builder.get_object("addunit_save")
			addunitbutton.connect("clicked", dosaveunit, addunitwindow)
			#Show NewUnit-Popup
			addunitwindow.show_all()

		#Adding all Students to the Grid
		def addingstudents(self, startpoint):
			#Adding Studentsnames - Postname, Prenames, Numbers and Buttons
			data_stu = dataop.getdata(con, "select id, name, prename, mail from students order by 2 asc", None)
			startfield_rows = 1
			#Startfield of Rows
			if startpoint == None:				
				startpoint = 1

			for stu in data_stu.fetchall():
				templabel_numbers = Gtk.Label()
				templabel_postname = Gtk.Label()
				templabel_prename = Gtk.Label()

				templabel_numbers.set_text("     " + str(startfield_rows) + ". ")
				templabel_postname.set_text(stu[1].encode("utf-8") + " ")
				templabel_prename.set_text(stu[2].encode("utf-8") + " ")
				
				#COLOR 0-65535 Gdk.Color(RED, GREEN, BLUE)
				if startfield_rows % 2 != 0:
					templabel_postname.modify_bg(0, Gdk.Color(52000, 52000, 52000))
					templabel_prename.modify_bg(0, Gdk.Color(52000, 52000, 52000))
					templabel_numbers.modify_bg(0, Gdk.Color(52000, 52000, 52000))

				newviewgrid.attach(templabel_numbers, startpoint , startfield_rows + 1, 1, 1)
				newviewgrid.attach(templabel_postname, startpoint + 1 , startfield_rows + 1, 1, 1)
				newviewgrid.attach(templabel_prename, startpoint + 2, startfield_rows + 1, 1, 1)				
				startfield_rows = startfield_rows + 1

		#Loading all Units from Database with Buttons
		def loadingallunits(*args):
			#Adding Units
			datas = dataop.getdata(con, "select id, year, month, day, title from units order by year, month, day asc", None)
			#Startfield of Rows
			startfield_rows = 4
			numb = 1
			for row in datas.fetchall():
				#Adding the Date-Label
				unitbuttonsgrid = Gtk.Grid()
				unitbuttonsgrid_snd = Gtk.Grid()

				#Label
				templabel_date = Gtk.Label()

				#Create a Nice String with max 16 Signs and three points if longer
				title_unit = str(row[4].encode("utf-8"))
				if len(title_unit) > 16:
					title_unit = title_unit[:16] + "..."

				templabel_date.set_markup("<b><big>" + str(row[3]) + "." + str(row[2]) + "." + str(row[1]) + "</big>\n" + title_unit + "</b>")
				templabel_date.set_justify(Gtk.Justification.LEFT)
				unitbuttonsgrid.attach(templabel_date, 2, 1, 1, 1)

				#Buttons
				#ChangeButton
				changebutton = Gtk.Button()
				changebutton.set_name("button_" + str(row[0]))
				image = Gtk.Image()
				image.set_from_file("icons/gear74.png")
				changebutton.set_size_request(10,10)
				changebutton.set_image(image)				
				#Button to Label
				unitbuttonsgrid_snd.attach(changebutton, 2, 1, 1, 1)
				#Add Action to the Button with id from actual student				
				changebutton.connect("clicked", changeunit, row[0], row[1], row[2], row[3], row[4])

				#DeleteButton
				deletebutton = Gtk.Button()
				deletebutton.set_name("delbutton_" + str(row[0]))
				image = Gtk.Image()
				image.set_from_file("icons/cancel19.png")
				deletebutton.set_size_request(10,10)
				deletebutton.set_image(image)				
				#Button to Label
				unitbuttonsgrid_snd.attach(deletebutton, 3, 1, 1, 1)
				#Add Action to the Button with id from actual student
				deletebutton.connect("clicked", deleteunit, row[0], row[1], row[2], row[3])

				#Spacer
				space = Gtk.Label()
				space.set_text("")
				unitbuttonsgrid.attach(space, 1, 1, 1, 1)
				
				unitbuttonsgrid.attach(unitbuttonsgrid_snd, 2, 2, 1, 1)
				
				#Adding all to the Main-Grid
				newviewgrid.attach(unitbuttonsgrid, startfield_rows, 1, 1, 1)
				
				#Adding all Buttons to all Students
				buttoncounter = 2
				data_students = dataop.getdata(con, "select id from students order by name asc", None)				
				for student in data_students.fetchall():
					#Getting Status of the Student
					cur = con.cursor()			
					unitstat_data = cur.execute("select status from status_stu_unit where unitid=? and studentid=?", (int(row[0]), int(student[0]),))
					
					for counter in unitstat_data.fetchall():
						unitstat = counter[0]
						#Images
						ue_b = Gtk.Image()
						ue_r = Gtk.Image()
						ue_b.set_from_file("icons/quest_black.png")
						ue_r.set_from_file("icons/quest_red.png")

						#OK leaved
						e_b = Gtk.Image()
						e_g = Gtk.Image()
						e_b.set_from_file("icons/ok_black.png")
						e_g.set_from_file("icons/ok_green.png")

						#MIddle good work
						middle_b = Gtk.Image()
						middle_g = Gtk.Image()
						middle_b.set_from_file("icons/middle_black.png")
						middle_g.set_from_file("icons/middle_green.png")

						#One Plus Work
						plus_b = Gtk.Image()
						plus_g = Gtk.Image()
						plus_b.set_from_file("icons/plus_black.png")
						plus_g.set_from_file("icons/plus_green.png")

						#PLusPlus Work
						plusplus_b = Gtk.Image()
						plusplus_g = Gtk.Image()
						plusplus_b.set_from_file("icons/plusplus_black.png")
						plusplus_g.set_from_file("icons/plusplus_green.png")

						#One Minus Work
						minus_b = Gtk.Image()
						minus_g = Gtk.Image()
						minus_b.set_from_file("icons/minus_black.png")
						minus_g.set_from_file("icons/minus_green.png")

						#MinusMinus Work
						minusminus_b = Gtk.Image()
						minusminus_g = Gtk.Image()
						minusminus_b.set_from_file("icons/minusminus_black.png")
						minusminus_g.set_from_file("icons/minusminus_green.png")

						#School-Event
						school_b = Gtk.Image()
						school_g = Gtk.Image()
						school_b.set_from_file("icons/school_black.png")
						school_g.set_from_file("icons/school_green.png")
						
						#Creating all Buttons and actions
						#UE-Button
						button_ue = Gtk.Button()	
						button_ue.set_name("ue")			
						button_ue.set_size_request(5,5)
						button_ue.set_image(ue_b) 	
						

						#E-Button
						button_e = Gtk.Button()		
						button_e.set_name("e")		
						button_e.set_size_request(5,5)
						button_e.set_image(e_b)						


						#Middle-Button
						button_middle = Gtk.Button()		
						button_middle.set_name("mid")	
						button_middle.set_size_request(5,5)
						button_middle.set_image(middle_b)						


						#Plus-Button
						button_plus = Gtk.Button()		
						button_plus.set_name("plus")		
						button_plus.set_size_request(5,5)
						button_plus.set_image(plus_b)	

						#PlusPlus-Button
						button_plusplus = Gtk.Button()		
						button_plusplus.set_name("plusplus")		
						button_plusplus.set_size_request(5,5)
						button_plusplus.set_image(plusplus_b)						


						#Minus-Button
						button_minus = Gtk.Button()		
						button_minus.set_name("minus")		
						button_minus.set_size_request(5,5)
						button_minus.set_image(minus_b)	

						#MinusMinus-Button
						button_minusminus = Gtk.Button()		
						button_minusminus.set_name("minusminus")		
						button_minusminus.set_size_request(5,5)
						button_minusminus.set_image(minusminus_b)					


						#School-Button
						button_school = Gtk.Button()	
						button_school.set_name("school")			
						button_school.set_size_request(5,5)
						button_school.set_image(school_b)		


						#Adding Black or Green/Red Images to the Buttons (depends on the Status of the Student for that Unit)
						#	Status
						#	0	- Unknown
						#	1	- Leave OK		
						#	2	- Schoolreason
						#	3	- MinusMinus
						#	4	- Minus
						#	5	- Middle
						#	6	- Plus
						#	7	- PlusPlus
						if unitstat == 0:
							button_ue.set_image(ue_r)			
						elif unitstat == 1:
							button_e.set_image(e_g)	
						elif unitstat == 2:
							button_school.set_image(school_g)	
						elif unitstat == 3:
							button_minusminus.set_image(minusminus_g)					
						elif unitstat == 4:
							button_minus.set_image(minus_g)
						elif unitstat == 5:
							button_middle.set_image(middle_g)
						elif unitstat == 6:
							button_plus.set_image(plus_g)
						elif unitstat == 7:
							button_plusplus.set_image(plusplus_g)	

						#Adding all Buttons
						#Creating the Grid
						buttonsgrid = Gtk.Grid()
						space1 = Gtk.Label()
						space1.set_text("     ")
						buttonsgrid.attach(space1, 5,1,1,1)
						space2 = Gtk.Label()
						space2.set_text(" ")
						buttonsgrid.attach(space2, 1,3,1,1)
						
						buttonsgrid.attach(button_ue, 1,1,1,1)
						buttonsgrid.attach(button_e, 2,1,1,1)						
						buttonsgrid.attach(button_school, 3,1,1,1)

						buttonsgrid.attach(button_minus, 1,2,1,1)
						buttonsgrid.attach(button_middle, 2,2,1,1)
						buttonsgrid.attach(button_plus, 3,2,1,1)

						buttonsgrid.attach(button_minusminus, 4,1,1,1)
						buttonsgrid.attach(button_plusplus, 4,2,1,1)
				
						#Adding all Actions
						button_ue.connect("clicked", updateUnitStu, int(student[0]), int(row[0]), 0, buttonsgrid)
						button_e.connect("clicked", updateUnitStu, int(student[0]), int(row[0]), 1, buttonsgrid)
						button_middle.connect("clicked", updateUnitStu, int(student[0]), int(row[0]), 5, buttonsgrid)
						button_plus.connect("clicked", updateUnitStu, int(student[0]), int(row[0]), 6, buttonsgrid)	
						button_plusplus.connect("clicked", updateUnitStu, int(student[0]), int(row[0]), 7, buttonsgrid)	
						button_minus.connect("clicked", updateUnitStu, int(student[0]), int(row[0]), 4, buttonsgrid)
						button_minusminus.connect("clicked", updateUnitStu, int(student[0]), int(row[0]), 3, buttonsgrid)						
						button_school.connect("clicked", updateUnitStu, int(student[0]), int(row[0]), 2, buttonsgrid)

						con.commit()

						#Check for Grey-Background
						if buttoncounter % 2 == 0:
							buttonsgrid.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.8, 0.8, 0.8))					

						#Adding Students Buttons
						newviewgrid.attach(buttonsgrid, startfield_rows, buttoncounter, 1, 1)

					#Increase Counter to print and save everything
					buttoncounter = buttoncounter + 1

					#Give all Students-Names every Unit wich is mod 4
				if numb % 4 == 0:
					addingstudents(self, startfield_rows + 1)
					startfield_rows = startfield_rows + 5
					numb = numb + 1
				else:
					startfield_rows = startfield_rows + 1					
					numb = numb + 1	



		#Fill the Grid with all Data from the actual database resp. Class		
		def fillDataGrid(*args):
			#Clear the grid
			for child in newviewgrid.get_children():
				newviewgrid.remove(child)

			#Clear the button-grid
			for child in datagrid_buttons.get_children():
				datagrid_buttons.remove(child)

			#Adding Buttons in Top-Area to add Students or import a csv-List (LATER!!)
			addunit = Gtk.Button.new_with_label("Neue Einheit")
			addunit.connect("clicked", do_addunit)
			datagrid_buttons.attach(addunit, 0, 1, 1, 1)
			
			#Loading the Students
			addingstudents(self, None)
			
			#Loading all Units
			loadingallunits()

			#Show the window		
			window.show_all()

		#Fill the Grid for the first time and call this method to reload
		fillDataGrid()