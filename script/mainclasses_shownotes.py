#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Organize the Notes and Categories
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

class ShowNotes():	

	#First Method called ba Mainclasses.py
	#Needs the actual window-object to change label "view"
	def start(self, classname, builder, window):

		#Databaseconnection
		dataop = DataOp()
		con = dataop.opendatabase(classname)

		######################################################################################
		#
		#
		#
		#				CATEGORIE AREA START
		#	
		######################################################################################

		#Saving new Upper-Categorie
		def savecatup(self, noteupwindow, catmanagewindow):
			#Getting Data from the Window
			name = builder.get_object("name").get_text().decode("utf-8")
			short = builder.get_object("short").get_text().decode("utf-8")
			weight = builder.get_object("weight").get_text().decode("utf-8")

			if len(name) == 0 or len(short) == 0 or len(weight) == 0:
				messWindow = Tkinter.Tk()
				messWindow.wm_withdraw()
				result = tkMessageBox.showinfo("Falsche Daten", "Bitte Daten korrekt eintragen!")
				messWindow.destroy()
			else:
				cur = con.cursor()
				#Count existing Units in the Datbase
				newid = dataop.getdata(con, "select count(id) from catup", None)
				if newid.fetchone()[0] == 0:
					try:
						cur.execute("insert into catup(id, name, short, weight) values (0, ?, ?, ?);", (name, short, int(weight),))
					except:
						messWindow = Tkinter.Tk()
						messWindow.wm_withdraw()
						result = tkMessageBox.showinfo("Falsche Daten", "Bitte bei Gewicht nur ganze Zahlen eingeben!")
						messWindow.destroy()
				else:
					try:
						cur.execute("insert into catup(id, name, short, weight) values ((SELECT max(id) FROM catup) + 1, ?, ?, ?);", (name, short, int(weight),))
					except:
						messWindow = Tkinter.Tk()
						messWindow.wm_withdraw()
						result = tkMessageBox.showinfo("Falsche Daten", "Bitte bei Gewicht nur ganze Zahlen eingeben!")
						messWindow.destroy()

				con.commit()
				noteupwindow.destroy()				

			#Reload the Managewindow
			printupcats(catmanagewindow)
			printdowncats(catmanagewindow)
				
		#Saving new Down-Categorie
		def savecatdown(self, notedownwindow, catmanagewindow):
			#Getting Data from the Window
			name = builder.get_object("name").get_text().decode("utf-8")
			short = builder.get_object("short").get_text().decode("utf-8")
			weight = builder.get_object("weight").get_text().decode("utf-8")
			uppercatid = builder.get_object("comboupcat").get_active_id()
			
			
			if len(name) == 0 or len(short) == 0 or len(weight) == 0:
				messWindow = Tkinter.Tk()
				messWindow.wm_withdraw()
				result = tkMessageBox.showinfo("Falsche Daten", "Bitte Daten korrekt eintragen!")
				messWindow.destroy()
			else:
				cur = con.cursor()
				#Count existing Units in the Datbase
				newid = dataop.getdata(con, "select count(id) from catdown", None)
				if newid.fetchone()[0] == 0:
					try:
						cur.execute("insert into catdown(id, upcat, name, short, weight) values (0, ?, ?, ?, ?);", (int(uppercatid), name, short, int(weight),))
					except:
						messWindow = Tkinter.Tk()
						messWindow.wm_withdraw()
						result = tkMessageBox.showinfo("Falsche Daten", "Bitte bei Gewicht nur ganze Zahlen eingeben oder Oberkategorie anlegen!")
						messWindow.destroy()
				else:
					try:
						cur.execute("insert into catdown(id, upcat, name, short, weight) values ((SELECT max(id) FROM catdown) + 1, ?, ?, ?, ?);", (int(uppercatid), name, short, int(weight),))
					except:
						messWindow = Tkinter.Tk()
						messWindow.wm_withdraw()
						result = tkMessageBox.showinfo("Falsche Daten", "Bitte bei Gewicht nur ganze Zahlen eingeben oder Oberkategorie anlegen!")
						messWindow.destroy()

				con.commit()
				notedownwindow.destroy()				

			#Reload the Managewindow
			printupcats(catmanagewindow)
			printdowncats(catmanagewindow)


		#Showing NOteUpAdd Window to prepare new Upper-Cat
		def addcat_up(self, managewindow):
			builder.add_from_file("gui/NoteUpPop.glade")
			addnoteup = builder.get_object("addnoteup")
						
			#Get Button-Object
			savedata = builder.get_object("addnoteup_save")
			savedata.connect("clicked", savecatup, addnoteup, managewindow)
			#Show New-Student-Popup
			addnoteup.show_all()

		#Showing NOteDownAdd Window to prepare new Down-Cat
		def addcat_down(self, managewindow):
			builder.add_from_file("gui/NoteDownPop.glade")
			addnotedown = builder.get_object("addnotedown")
				
			#Get Button-Object
			savedata = builder.get_object("savenotedown")
			savedata.connect("clicked", savecatdown, addnotedown, managewindow)

			#Loading all Upper-Cats and ad them to a Combo-Box
			uppeercats = builder.get_object("comboupcat")		

			allupcat = dataop.getdata(con, "select id, name from catup order by weight desc", None)
			
			for upcats in allupcat.fetchall():
				uppeercats.append(str(upcats[0]), upcats[1].encode("utf-8"))				

			uppeercats.set_active(0)	

			#Show New-Student-Popup
			addnotedown.show_all()

		#Close the manage-Window
		def closemanagewindow(self, managewindow):
			managewindow.destroy()

		#Updating Changes Catup and reload Grid
		def savechanges_catup(self, catup_changewindow, managewindow, id):
			name = builder.get_object("name").get_text().decode("utf-8")
			short = builder.get_object("short").get_text().decode("utf-8")
			weight = builder.get_object("weight").get_text().decode("utf-8")

			if len(name) == 0 or len(short) == 0 or len(weight) == 0:
				messWindow = Tkinter.Tk()
				messWindow.wm_withdraw()
				result = tkMessageBox.showinfo("Falsche Daten", "Bitte Daten korrekt eintragen!")
				messWindow.destroy()
			else:
				cur = con.cursor()
				#Count existing Units in the Datbase
				try:
					cur.execute("update catup set name=?, short=?, weight=? where id=?", (name, short, int(weight), id,))
				except:
					messWindow = Tkinter.Tk()
					messWindow.wm_withdraw()
					result = tkMessageBox.showinfo("Falsche Daten", "Bitte bei Gewicht nur ganze Zahlen eingeben!")
					messWindow.destroy()

				con.commit()
				catup_changewindow.destroy()
				printupcats(managewindow)
				printdowncats(managewindow)
				fillDataGrid()

		#Updating Changes Catdown and reload Grid
		def savechanges_catdown(self, catdown_changewindow, managewindow, id):
			name = builder.get_object("name").get_text().decode("utf-8")
			short = builder.get_object("short").get_text().decode("utf-8")
			weight = builder.get_object("weight").get_text().decode("utf-8")
			uppercatid = builder.get_object("comboupcat").get_active_id()

			if len(name) == 0 or len(short) == 0 or len(weight) == 0:
				messWindow = Tkinter.Tk()
				messWindow.wm_withdraw()
				result = tkMessageBox.showinfo("Falsche Daten", "Bitte Daten korrekt eintragen!")
				messWindow.destroy()
			else:
				cur = con.cursor()
				#Count existing Units in the Datbase
				try:
					cur.execute("update catdown set name=?, short=?, weight=?, upcat=? where id=?", (name, short, int(weight), uppercatid, id,))
				except:
					messWindow = Tkinter.Tk()
					messWindow.wm_withdraw()
					result = tkMessageBox.showinfo("Falsche Daten", "Bitte bei Gewicht nur ganze Zahlen eingeben!")
					messWindow.destroy()

				con.commit()
				catdown_changewindow.destroy()
				printupcats(managewindow)
				printdowncats(managewindow)
				fillDataGrid()

		#Starting workflow for changing a Upper-Categorie
		def changeupcat(self, id, managewindow, name, short, weight):
			builder.add_from_file("gui/NoteUpPop.glade")
			addnoteupchange = builder.get_object("addnoteup")
						
			builder.get_object("name").set_text(name)
			builder.get_object("short").set_text(short)
			builder.get_object("weight").set_text(str(weight))

			#Get Button-Object
			savedata = builder.get_object("addnoteup_save")
			savedata.connect("clicked", savechanges_catup, addnoteupchange, managewindow, id)
			#Show New-Student-Popup
			addnoteupchange.show_all()

		#WORKFLOW FOR DOWN CATEGORIES
		def changedowncat(self, id, idup, managewindow, name, short, weight):
			builder.add_from_file("gui/NoteDownPop.glade")
			addnotedownchange = builder.get_object("addnotedown")
						
			builder.get_object("name").set_text(name)
			builder.get_object("short").set_text(short)
			builder.get_object("weight").set_text(str(weight))
			#Loading all Upper-Cats and ad them to a Combo-Box
			uppeercats = builder.get_object("comboupcat")		

			allupcat = dataop.getdata(con, "select id, name from catup order by weight desc", None)
			
			for upcats in allupcat.fetchall():
				uppeercats.append(str(upcats[0]), upcats[1].encode("utf-8"))				

			#Select the active Upper-ID
			uppeercats.set_active_id(str(idup))	
			#Get Button-Object
			savedata = builder.get_object("savenotedown")
			savedata.connect("clicked", savechanges_catdown, addnotedownchange, managewindow, id)
			#Show New-Student-Popup
			addnotedownchange.show_all()

		#Delete a Upper Cateogire and all Data wich is connected to (WARNGIN! Deletes Down-Cats and Notes!!! Check dataop.py)
		def delcatup(self, id, managewindow, name):
			messWindow = Tkinter.Tk()
			messWindow.wm_withdraw()
			result = tkMessageBox.askokcancel("Warnung", "ACHTUNG! Alle Daten der Kategorie  " + name + " werden UNWIDERRUFLICH gelöscht. Auch alle Noten und Unterkategorien! Fortfahren?")
			
			#Check for deleting or not
			if result == True:
				#Delete True - Delete the Uppercat and reload the Grid
				dataop.deleteCatUp(con, id)
				messWindow.destroy()
				#Reload Upper-Categories
				printupcats(managewindow)
				printdowncats(managewindow)
			else:
				messWindow.destroy()

		def delcatdown(self, id, managewindow, name):
			messWindow = Tkinter.Tk()
			messWindow.wm_withdraw()
			result = tkMessageBox.askokcancel("Warnung", "ACHTUNG! Alle Daten der Kategorie  " + name + " werden UNWIDERRUFLICH gelöscht. Auch alle Noten! Fortfahren?")
			
			#Check for deleting or not
			if result == True:
				#Delete True - Delete the Uppercat and reload the Grid
				dataop.deleteCatDown(con, id)
				messWindow.destroy()
				#Reload Upper-Categories
				printupcats(managewindow)
				printdowncats(managewindow)				
			else:
				messWindow.destroy()

		#Print all Upper Categories
		def printupcats(managewindow):
			#Adding all Upper Categories
			upgrid = builder.get_object("catup_grid")

			#Clear the UpCatGrid
			for child in upgrid.get_children():
				upgrid.remove(child)

			#Adding all Uppercategories to the Grid
			datas = dataop.getdata(con, "select id, name, short, weight from catup order by weight desc", None)
			
			counter = 1
			for row in datas.fetchall():
				templabel_counter = Gtk.Label()
				templabel_counter.set_markup("<b>" + "  " + str(counter) + ".</b>")
				templabel_name = Gtk.Label()
				templabel_name.set_markup("   <b>" + str(row[1].encode("utf-8")) + "</b>")
				templabel_catshort = Gtk.Label()
				templabel_catshort.set_markup("  <b>" + str(row[2].encode("utf-8")) + "</b>")
				templabel_catweight = Gtk.Label()
				templabel_catweight.set_markup("  <b>" + str(row[3]) + "</b>    ")

				#Buttons to change/delete the Categories
				#ChangeButton
				changebutton = Gtk.Button()
				image = Gtk.Image()
				image.set_from_file("icons/gear74.png")
				changebutton.set_size_request(10,10)
				changebutton.set_image(image)				
				#Button to Label
				upgrid.attach(changebutton, 5, counter, 1, 1)
				#Add Action to the Button with id from actual student				
				changebutton.connect("clicked", changeupcat, row[0], managewindow, str(row[1].encode("utf-8")), str(row[2].encode("utf-8")), row[3])

				#DeleteButton
				deletebutton = Gtk.Button()
				image = Gtk.Image()
				image.set_from_file("icons/cancel19.png")
				deletebutton.set_size_request(10,10)
				deletebutton.set_image(image)				
				#Button to Label
				upgrid.attach(deletebutton, 6, counter, 1, 1)
				#Add Action to the Button with id from actual student
				deletebutton.connect("clicked", delcatup, row[0], managewindow, str(row[1].encode("utf-8")))

				upgrid.attach(templabel_counter, 1, counter, 1, 1)
				upgrid.attach(templabel_name, 2, counter, 1, 1)
				upgrid.attach(templabel_catshort, 3, counter, 1, 1)
				upgrid.attach(templabel_catweight, 4, counter, 1, 1)
				counter = counter + 1
				managewindow.show_all()

		#Print all Upper Categories
		def printdowncats(managewindow):
			#Adding all Upper Categories
			downgrid = builder.get_object("catdown_grid")

			#Clear the UpCatGrid
			for child in downgrid.get_children():
				downgrid.remove(child)

			#Adding all Uppercategories to the Grid
			datas = dataop.getdata(con, "select id, name, short, weight, upcat from catdown order by weight desc", None)
			
			counter = 1
			for row in datas.fetchall():
				#Getting Name of upper Categorie
				uppercatname = dataop.getdata(con, "select name from catup where id=?", row[4]).fetchone()[0]
				templabel_counter = Gtk.Label()
				templabel_counter.set_markup("<b>" + "  " + str(counter) + ".</b>")
				templabel_name = Gtk.Label()
				templabel_name.set_markup("   <b>" + str(row[1].encode("utf-8")) + "</b>")
				templabel_catshort = Gtk.Label()
				templabel_catshort.set_markup("  <b>" + str(row[2].encode("utf-8")) + "</b>")
				templabel_catweight = Gtk.Label()
				templabel_catweight.set_markup("  <b>" + str(row[3]) + "</b>    ")
				templabel_in = Gtk.Label()
				templabel_in.set_markup(" in ")
				templabel_uppercat = Gtk.Label()
				templabel_uppercat.set_markup("<b>" + uppercatname + "</b>    ")

				#Buttons to change/delete the Categories
				#ChangeButton
				changebutton = Gtk.Button()
				image = Gtk.Image()
				image.set_from_file("icons/gear74.png")
				changebutton.set_size_request(10,10)
				changebutton.set_image(image)				
				#Button to Label
				downgrid.attach(changebutton, 7, counter, 1, 1)
				#Add Action to the Button with id from actual student				
				changebutton.connect("clicked", changedowncat, row[0], row[4], managewindow, str(row[1].encode("utf-8")), str(row[2].encode("utf-8")), row[3])

				#DeleteButton
				deletebutton = Gtk.Button()
				image = Gtk.Image()
				image.set_from_file("icons/cancel19.png")
				deletebutton.set_size_request(10,10)
				deletebutton.set_image(image)				
				#Button to Label
				downgrid.attach(deletebutton, 8, counter, 1, 1)
				#Add Action to the Button with id from actual student
				deletebutton.connect("clicked", delcatdown, row[0], managewindow, str(row[1].encode("utf-8")))

				downgrid.attach(templabel_counter, 1, counter, 1, 1)
				downgrid.attach(templabel_name, 2, counter, 1, 1)
				downgrid.attach(templabel_catshort, 3, counter, 1, 1)
				downgrid.attach(templabel_catweight, 4, counter, 1, 1)
				downgrid.attach(templabel_in, 5, counter, 1, 1)
				downgrid.attach(templabel_uppercat, 6, counter, 1, 1)
				counter = counter + 1
				managewindow.show_all()

		#Manage Categories
		def managecat(*args):
			builder.add_from_file("gui/ManageCat.glade")
			managewindow = builder.get_object("windowmanagecat")
						
			#Close-Button
			closewindow = builder.get_object("close_catmanage")
			closewindow.connect("clicked", closemanagewindow, managewindow)

			#New Upper-Cat
			newupcat = builder.get_object("new_upcat")
			newupcat.connect("clicked", addcat_up, managewindow)

			#New Down-Cat
			newdowncat = builder.get_object("new_downcat")
			newdowncat.connect("clicked", addcat_down, managewindow)

			printupcats(managewindow)
			printdowncats(managewindow)
			#Show Categoriemanagewindow
			managewindow.show_all()

		######################################################################################
		#
		#
		#
		#				CATEGORIE AREA END
		#	
		######################################################################################

		######################################################################################
		#
		#
		#
		#				NOTE AREA START
		#	
		######################################################################################

		#Saving a new Note
		def do_savenewnote(self, notewindow):
			#Getting all the Data
			name = builder.get_object("name").get_text().decode("utf-8")
			weight = builder.get_object("weight").get_text()
	
			if len(name) == 0 or len(weight) == 0:
				messWindow = Tkinter.Tk()
				messWindow.wm_withdraw()
				tkMessageBox.showinfo("Falsche Daten", "Bitte korrekte Daten eintragen")
				messWindow.destroy()
			else:
				upcat = builder.get_object("combo_catup").get_active_id()
				downcat = builder.get_object("combo_catdown").get_active_id()
				#Date
				date = builder.get_object("notedate").get_date()			
				year = str(date[0])
				#Make the Month userfriendly :)
				month = str(date[1]+1)
				day = str(date[2])

				#Save Note
				cur = con.cursor()
				#Count existing Notes in the Datbase
				newid = dataop.getdata(con, "select count(id) from notes", None)
				if newid.fetchone()[0] == 0:
					try:						
						cur.execute("insert into notes(id, name, weight, upcat, downcat, year, month, day) values (0, ?, ?, ?, ?, ?, ?, ?);", (name, int(weight), int(upcat), int(downcat), year, month, day))
					except:
						messWindow = Tkinter.Tk()
						messWindow.wm_withdraw()
						result = tkMessageBox.showinfo("Falsche Daten", "Bitte bei Gewicht nur ganze Zahlen eingeben!")
						messWindow.destroy()
				else:
					try:
						cur.execute("insert into notes(id, name, weight, upcat, downcat, year, month, day) values ((SELECT max(id) FROM notes) + 1, ?, ?, ?, ?, ?, ?, ?);", (name, int(weight), int(upcat), int(downcat), year, month, day))
					except:
						messWindow = Tkinter.Tk()
						messWindow.wm_withdraw()
						result = tkMessageBox.showinfo("Falsche Daten", "Bitte bei Gewicht nur ganze Zahlen eingeben!")
						messWindow.destroy()

				con.commit()				
				notewindow.destroy()
				#Fill the new Grid
				fillDataGrid()

		#Updating a Note
		def do_updatenote(self, id, notewindow):
			#Getting all the Data
			name = builder.get_object("name").get_text().decode("utf-8")
			weight = builder.get_object("weight").get_text()
	
			if len(name) == 0 or len(weight) == 0:
				messWindow = Tkinter.Tk()
				messWindow.wm_withdraw()
				tkMessageBox.showinfo("Falsche Daten", "Bitte korrekte Daten eintragen")
				messWindow.destroy()
			else:
				upcat = builder.get_object("combo_catup").get_active_id()
				downcat = builder.get_object("combo_catdown").get_active_id()
				#Date
				date = builder.get_object("notedate").get_date()			
				year = str(date[0])
				#Make the Month userfriendly :)
				month = str(date[1]+1)
				day = str(date[2])

				#Save Note
				cur = con.cursor()
				#Count existing Notes in the Datbase
				cur.execute("update notes set name=?, weight=?, upcat=?, downcat=?, year=?, month=?, day=? where id=?", (name, int(weight), upcat, downcat, year, month, day, id, )) 
				con.commit()				
				notewindow.destroy()
				#Fill the new Grid
				fillDataGrid()

		#Creating the NewNoteWindow
		def addnewnote(*args):
			builder.add_from_file("gui/NewNotePop.glade")
			notewindow = builder.get_object("addnote")
			
			#Loading all Upper-Cats and ad them to a Combo-Box
			uppercats = builder.get_object("combo_catup")		
			allupcat = dataop.getdata(con, "select id, name from catup order by weight desc", None)			
			for upcats in allupcat.fetchall():
				uppercats.append(str(upcats[0]), upcats[1].encode("utf-8"))	
			uppercats.set_active(0)

			#Loading all Down-Cats and ad them to a Combo-Box
			downcats = builder.get_object("combo_catdown")		
			alldowncat = dataop.getdata(con, "select id, name from catdown order by weight desc", None)			
			for downcat in alldowncat.fetchall():
				downcats.append(str(downcat[0]), downcat[1].encode("utf-8"))	
			downcats.set_active(0)

			#Adding Functionality to the Save-Button
			savebutton = builder.get_object("savenote")
			savebutton.connect("clicked", do_savenewnote, notewindow)
			#Show Categoriemanagewindow
			notewindow.show_all()

		#Update a Note
		def updatenote(self, noteid, studentid, notecombobox):
			#Update a Note
			cur = con.cursor()
			#Checking for a Note
			maybenote = cur.execute("select id from notes_student where notesid=? and studentid=?", (noteid, studentid,)).fetchone()

			#Getting new Note
			note = notecombobox.get_active()
				
			#Save a new note or update
			if maybenote == None:
				newid = dataop.getdata(con, "select count(id) from notes_student", None)
				if newid.fetchone()[0] == 0:
					cur.execute("insert into notes_student(id, notesid, studentid, note) values(0, ?, ?,?)", (noteid, studentid, float(note),))
				else:
					cur.execute("insert into notes_student(id, notesid, studentid, note) values((SELECT max(id) FROM notes_student) + 1, ?, ?,?)", (noteid, studentid, float(note),))
			else:
				cur.execute("update notes_student set note=? where notesid=? and studentid=?", (float(note), noteid, studentid,))
				
			con.commit()
			fillDataGrid()			
		
		#Delete a Note
		def deletenote(self, id, mainwindow, name):
			messWindow = Tkinter.Tk()
			messWindow.wm_withdraw()
			result = tkMessageBox.askokcancel("Warnung", "ACHTUNG! Alle Daten der Noten " + str(name) + " werden UNWIDERRUFLICH gelöscht. Fortfahren?")
			messWindow.destroy()

			#Check for deleting or not
			if result == True:
				#Delete True - Delete the Note and reload the Grid
				dataop.deleteNoteComplete(con, id)
				fillDataGrid()

		def changenote(self, mainwindow, id, name, weight, upcat, downcateg, year, month, day):
			builder.add_from_file("gui/NewNotePop.glade")
			notewindow = builder.get_object("addnote")
			name = builder.get_object("name").set_text(name)
			weight = builder.get_object("weight").set_text(str(weight))
			#Loading all Upper-Cats and ad them to a Combo-Box
			uppercats = builder.get_object("combo_catup")		
			allupcat = dataop.getdata(con, "select id, name from catup order by weight desc", None)	
			counter = 0		
			for upcats in allupcat.fetchall():
				uppercats.append(str(upcats[0]), upcats[1].encode("utf-8"))	
				if upcats[0] == upcat:
					uppercats.set_active(counter)
				counter = counter + 1
			
			#Loading all Down-Cats and ad them to a Combo-Box
			downcats = builder.get_object("combo_catdown")		
			alldowncat = dataop.getdata(con, "select id, name from catdown order by weight desc", None)		
			counter = 0	
			for downcat in alldowncat.fetchall():
				downcats.append(str(downcat[0]), downcat[1].encode("utf-8"))	
				if downcat[0] == downcateg:
					downcats.set_active(counter)
				counter = counter + 1
			
			#Date
			date = builder.get_object("notedate")
			date.select_month(int(month) - 1, int(year))
			date.select_day(int(day))

			#Adding Functionality to the Save-Button
			savebutton = builder.get_object("savenote")
			savebutton.connect("clicked", do_updatenote, id, notewindow)
			#Show Categoriemanagewindow
			notewindow.show_all()

		#Loading all Notes
		def loadNotes(datagrid, mainwindow):
			#datas = dataop.getdata(con, "select id, name, weight, upcat, downcat, year, month, day from notes order by year, month, day asc", None)
			datas = dataop.getdata(con, "select id, name, weight, upcat, downcat, year, month, day from notes order by name asc", None)
			rowcount = 4
			notecounter = 0
			for row in datas.fetchall():
				#Getting Names from Categories
				upcat = dataop.getdata(con, "select short, weight from catup where id=?", row[3]).fetchone()
				downcat =  dataop.getdata(con, "select short, weight from catdown where id=?", row[4]).fetchone()
				notegrid = Gtk.Grid()
				notegrid_snd = Gtk.Grid()				
				templabel = Gtk.Label()
				templabel.set_markup("<b><big>" + row[1] + "</big></b>\n<b>Gewicht: " + str(row[2]) + "\n" + row[7] + "."+ row[6] + "."+ row[5] + "\nObKa: " + str(upcat[0]) + " | " + str(upcat[1]) + "\nUnKa: " + str(downcat[0]) + " | " + str(downcat[1]) + "</b>")
				notegrid.attach(templabel, 0, 0, 1, 1)
				
				#Buttons to change/delete the Categories
				#ChangeButton
				changebutton = Gtk.Button()
				image = Gtk.Image()
				image.set_from_file("icons/gear74.png")
				changebutton.set_size_request(10,10)
				changebutton.set_image(image)				
				#Button to Label
				notegrid_snd.attach(changebutton, 0, 0, 1, 1)
				#Add Action to the Button with id from actual student				
				changebutton.connect("clicked", changenote, mainwindow, row[0], str(row[1].encode("utf-8")), row[2],row[3],row[4],row[5],row[6],row[7],)

				#DeleteButton
				deletebutton = Gtk.Button()
				image = Gtk.Image()
				image.set_from_file("icons/cancel19.png")
				deletebutton.set_size_request(10,10)
				deletebutton.set_image(image)				
				#Button to Label
				notegrid_snd.attach(deletebutton, 1, 0, 1, 1)
				#Add Action to the Button with id from actual student
				deletebutton.connect("clicked", deletenote, row[0], mainwindow, str(row[1].encode("utf-8")))

				notegrid.attach(notegrid_snd, 0, 1, 1, 1)
				datagrid.attach(notegrid, rowcount, 0, 1, 1)
				#notes_student (id INT PRIMARY KEY NOT NULL, notesid INT NOT NULL, studentid INT NOT NULL, note DOUBLE NOT NULL)
				data_students = dataop.getdata(con, "select id from students order by name asc", None)				
				studentcounter = 1
				average_note = 0
				#Needed in case that a student as no note 
				corrector = 0
				for student in data_students.fetchall():
					stugrid = Gtk.Grid()
					cur = con.cursor()			
					stunote = cur.execute("select note from notes_student where notesid=? and studentid=?", (int(row[0]), int(student[0]),)).fetchone()
					spacer = Gtk.Label("   ")
					if stunote == None:		
						notecombobox = giv15to0ComboBox()
						stugrid.attach(notecombobox, rowcount, studentcounter, 1, 1)
						stugrid.attach(spacer, rowcount + 1, studentcounter, 1, 1)
						notecombobox.connect("changed", updatenote, int(row[0]), int(student[0]), notecombobox)
					else:

						notecombobox = giv15to0ComboBox()
						notecombobox.set_active(stunote[0])
						#Calculate Average-Note and prevent for adding "na" (16)
						if stunote[0] != 16.0:
							average_note = average_note + stunote[0]
						else:
							corrector = corrector + 1

						stugrid.attach(notecombobox, rowcount, studentcounter, 1, 1)
						stugrid.attach(spacer, rowcount + 1, studentcounter, 1, 1)
						notecombobox.connect("changed", updatenote, int(row[0]), int(student[0]), notecombobox)

					if studentcounter % 2 != 0:
						stugrid.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.8, 0.8, 0.8, 1))				

					datagrid.attach(stugrid, rowcount, studentcounter, 1, 1)	
					studentcounter = studentcounter + 1

				#Adding Average-Note under the Table
				diff = studentcounter - corrector - 1
				average_note = round(average_note / diff, 2)
				average = Gtk.Label("Durchschnitt: " + str(average_note))
				datagrid.attach(average, rowcount, studentcounter + 1, 1, 1)	

				rowcount = rowcount + 2	
				notecounter = notecounter + 1
				#If four Notes reached print all Names of the Students again
				if notecounter % 4 == 0:
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
						datagrid.attach(templabel_postname, rowcount  + 1, startfield_rows, 1, 1)
						datagrid.attach(templabel_prename, rowcount + 2, startfield_rows, 1, 1)
						datagrid.attach(templabel_numbers, rowcount, startfield_rows, 1, 1)
						startfield_rows = startfield_rows + 1		
					rowcount = rowcount + 3
			#Reload the Mainwindow
			mainwindow.show_all()

		#Gives a 0 to 15 Combobox
		def giv15to0ComboBox():			
			notes = Gtk.ListStore(int, str)			
			for note in range(16):
				notes.append([note, str(note)])
			notes.append([17, "na"])
			combobox = Gtk.ComboBox.new_with_model_and_entry(notes)			
			combobox.set_entry_text_column(1)
			return combobox
			
		######################################################################################
		#
		#
		#
		#				NOTE AREA ENDE
		#	
		######################################################################################

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
			
			#Adding New Note-Button
			addnote = Gtk.Button.new_with_label("Neue Note")
			addnote.connect("clicked", addnewnote)
			datagrid_buttons.attach(addnote, 0, 1, 1, 1)
	
			#Button for manage Categories			
			kat_down = Gtk.Button("Kategorien verwalten")
			kat_down.connect("clicked", managecat)
			datagrid_buttons.attach(kat_down, 1, 1, 1, 1)

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
				newviewgrid.attach(templabel_prename, 2, startfield_rows, 1, 1)
				newviewgrid.attach(templabel_numbers, 0, startfield_rows, 1, 1)
				startfield_rows = startfield_rows + 1

			#Show the window		
			window.show_all()
			loadNotes(newviewgrid, window)			

		#Fill the Grid for the first time and call this method to reload
		fillDataGrid()
		





