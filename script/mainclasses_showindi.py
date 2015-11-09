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

class ShowIndi():	

	#First Method called ba Mainclasses.py
	#Needs the actual window-object to change label "view"
	def start(self, classname, builder, window):

		#Databaseconnection
		dataop = DataOp()
		con = dataop.opendatabase(classname)

		#Button Prev/Next student
		def do_prevstu(self, combobox, maxstu):
			if combobox.get_active() > 0:
				combobox.set_active(combobox.get_active() - 1)	
			else:
				combobox.set_active(maxstu - 1)					

		def do_nextstu(self, combobox, maxstu):
			if combobox.get_active() + 1 != maxstu:
				combobox.set_active(combobox.get_active() + 1)	
			else:
				combobox.set_active(0)					

		#Show actual Student
		def updateview(self, combobox, grid):
			#Clear the Grid
			for child in grid.get_children():
				grid.remove(child)

			tree_iter = combobox.get_active_iter()
			model = combobox.get_model()
			id, name = model[tree_iter][:2]
			#id = StudentId
			#Add Student Name to Grid
			stuname_label = Gtk.Label()
			stuname_label.set_markup("\n<big><b>" + name + "</b></big>")
			grid.attach(stuname_label, 0, 0, 1, 1)

			#Counting all Status-Infos
			#	Status
			#	0	- Unknown
			#	1	- Leave OK		
			#	2	- Schoolreason
			#	3	- MinusMinus
			#	4	- Minus
			#	5	- Middle
			#	6	- Plus
			#	7	- PlusPlus
			#
			unknown = dataop.getdata(con, "select count(status) from status_stu_unit where studentid=? and status=0", id).fetchone()[0]
			leaveok = dataop.getdata(con, "select count(status) from status_stu_unit where studentid=? and status=1", id).fetchone()[0]
			school = dataop.getdata(con, "select count(status) from status_stu_unit where studentid=? and status=2", id).fetchone()[0]
			minusminus = dataop.getdata(con, "select count(status) from status_stu_unit where studentid=? and status=3", id).fetchone()[0]
			minus = dataop.getdata(con, "select count(status) from status_stu_unit where studentid=? and status=4", id).fetchone()[0]
			mid = dataop.getdata(con, "select count(status) from status_stu_unit where studentid=? and status=5", id).fetchone()[0]
			plus = dataop.getdata(con, "select count(status) from status_stu_unit where studentid=? and status=6", id).fetchone()[0]
			plusplus = dataop.getdata(con, "select count(status) from status_stu_unit where studentid=? and status=7", id).fetchone()[0]
			
			statigrid = Gtk.Grid()
			statigrid_allstati = Gtk.Grid()
			status_label = Gtk.Label()
			status_label.set_markup("\n<b><big>Übersicht         </big></b>\n")
			statigrid.attach(status_label, 0, 0, 1, 1)

			#Images			
			ue_r = Gtk.Image()
			ue_r.set_from_file("icons/quest_red.png")			
			lab_ue_count = Gtk.Label()
			lab_ue_count.set_markup(" <big><b>: " + str(unknown) + "</b></big>")
			statigrid_allstati.attach(ue_r, 0, 0, 1, 1)
			statigrid_allstati.attach(lab_ue_count, 1, 0, 1, 1)

			#OK leaved
			e_g = Gtk.Image()
			e_g.set_from_file("icons/ok_green.png")
			e_g_ue_count = Gtk.Label()
			e_g_ue_count.set_markup(" <big><b>: " + str(leaveok) + "</b></big>")
			statigrid_allstati.attach(e_g, 0, 1, 1, 1)
			statigrid_allstati.attach(e_g_ue_count, 1, 1, 1, 1)

			#School-Event
			school_g = Gtk.Image()
			school_g.set_from_file("icons/school_green.png")
			school_g_ue_count = Gtk.Label()
			school_g_ue_count.set_markup(" <big><b>: " + str(school) + "</b></big>")
			statigrid_allstati.attach(school_g, 0, 2, 1, 1)
			statigrid_allstati.attach(school_g_ue_count, 1, 2, 1, 1)

			#MIddle good work
			middle_g = Gtk.Image()
			middle_g.set_from_file("icons/middle_green.png")
			middle_g_ue_count = Gtk.Label()
			middle_g_ue_count.set_markup(" <big><b>: " + str(mid) + "</b></big>")
			statigrid_allstati.attach(middle_g, 0, 3, 1, 1)
			statigrid_allstati.attach(middle_g_ue_count, 1, 3, 1, 1)

			#One Plus Work
			plus_g = Gtk.Image()
			plus_g.set_from_file("icons/plus_green.png")
			plus_g_ue_count = Gtk.Label()
			plus_g_ue_count.set_markup(" <big><b>: " + str(plus) + "</b></big>")
			statigrid_allstati.attach(plus_g, 0, 4, 1, 1)
			statigrid_allstati.attach(plus_g_ue_count, 1, 4, 1, 1)

			#PLusPlus Work
			plusplus_g = Gtk.Image()		
			plusplus_g.set_from_file("icons/plusplus_green.png")
			plusplus_g_ue_count = Gtk.Label()
			plusplus_g_ue_count.set_markup(" <big><b>: " + str(plusplus) + "</b></big>")
			spacer = Gtk.Label("   ")
			statigrid_allstati.attach(spacer, 2, 4, 1, 1)
			statigrid_allstati.attach(plusplus_g, 3, 4, 1, 1)
			statigrid_allstati.attach(plusplus_g_ue_count, 4, 4, 1, 1)


			#One Minus Work
			minus_g = Gtk.Image()
			minus_g.set_from_file("icons/minus_green.png")
			minus_g_ue_count = Gtk.Label()
			minus_g_ue_count.set_markup(" <big><b>: " + str(minus) + "</b></big>")
			statigrid_allstati.attach(minus_g, 0, 5, 1, 1)
			statigrid_allstati.attach(minus_g_ue_count, 1, 5, 1, 1)

			#PLusPlus Work
			minusminus_g = Gtk.Image()
			minusminus_g.set_from_file("icons/minusminus_green.png")
			minusminus_g_ue_count = Gtk.Label()
			minusminus_g_ue_count.set_markup(" <big><b>: " + str(minusminus) + "</b></big>")
			spacer = Gtk.Label("   ")
			statigrid_allstati.attach(spacer, 2, 5, 1, 1)
			statigrid_allstati.attach(minusminus_g, 3, 5, 1, 1)
			statigrid_allstati.attach(minusminus_g_ue_count, 4, 5, 1, 1)

			statigrid.attach(statigrid_allstati, 0, 1, 1, 1)
						
			#Notes to Grid
			notegrid = Gtk.Grid()
			#notegrid_allnotes = Gtk.Grid()
			notegrid_label = Gtk.Label()
			notegrid_label.set_markup("   \n<b><big>Noten        </big></b>\n")
			notegrid.attach(notegrid_label, 0, 0, 1, 1)
			#Calculate the Notes
			cur = con.cursor()
			#Calculating all Downcategories and save them to downcat with the Categorie-ID
			
			#Step One - Getting all Upper Cats
			data_upcats = cur.execute("select id, weight, name from catup order by weight desc")
			rowcounter = 1
			columncounter = 0
			finalnote = []
			for upcats in data_upcats.fetchall():
				#print "Upcat: " + str(upcats[2].encode("utf-8"))
				#print "Weight: " + str(upcats[1])
				#print "ID: " + str(upcats[0])
				uplabel = Gtk.Label()
				uplabel.set_markup("<b><big>" + upcats[2].encode("utf-8") + " (" + str(upcats[1]) + ")</big></b>      ")
				notegrid.attach(uplabel, columncounter, rowcounter, 1, 1)

				rowcounter = rowcounter + 1
				#Step Two: Get all Down-Cats with this Upcat-ID
				data_downcats = cur.execute("select id, weight, name from catdown where upcat=?", (int(upcats[0]), ))
				downcats_notes = []
				for downcats in data_downcats.fetchall():					
					#print "Downcat: " + str(downcats[2].encode("utf-8"))
					#print "Weight: " + str(downcats[1])
					#print "ID: " + str(downcats[0])
					downlabel = Gtk.Label()
					downlabel.set_markup("<b>" + downcats[2].encode("utf-8") + " (" + str(downcats[1]) + ")</b>     ")
					notegrid.attach(downlabel, columncounter, rowcounter, 1, 1)								
					#Step Three: Get all Notes from this DownCat and Upcat from actual Student
					data_notes = cur.execute("select id,weight ,name from notes where upcat=? and downcat=?", (upcats[0], downcats[0]),)
					weight_note = 0
					note_calc = 0
					for notes in data_notes.fetchall():
						#print "Notes: " + str(notes[2].encode("utf-8"))
						#print "Weight: " + str(notes[1])
						#print "ID: " + str(notes[0])
						notes_info = Gtk.Label()
						notes_info.set_markup("<b>" + notes[2].encode("utf-8") + " (" + str(notes[1]) + "):</b>    ")
						notegrid.attach(notes_info, columncounter + 1, rowcounter, 1, 1)																				
						#Step Four: Getting the final note
						try:
							data_stunote = cur.execute("select id, note from notes_student where studentid=? and notesid=? and note!=16.0", (id, notes[0],)).fetchone()[1]						
							#
							#	SPECIAL: All Notes with 16.0 will not be calculatet!!!! Here beware by other Gradesystems!!!
							#
							#
							note_stu_label = Gtk.Label()
							note_stu_label.set_markup("<b>" + str(data_stunote) + "</b>     ")
							notegrid.attach(note_stu_label, columncounter + 2, rowcounter, 1, 1)
							rowcounter = rowcounter + 1															
							weight_note = weight_note + notes[1]
							note_calc = note_calc + data_stunote * notes[1]
						except:
							rowcounter = rowcounter + 1
							break
					
					#Saving all Downcategorie-Notes ID WEIGHT NOTE
					if weight_note > 0:
						downcats_notes.append([downcats[0], downcats[1], round(note_calc / weight_note, 2)])
						note_down = Gtk.Label()
						note_down.set_markup("<b>Gesamt UnKa: " + str(round(note_calc / weight_note, 2)) + "</b>")
						notegrid.attach(note_down, columncounter + 1, rowcounter, 1, 1)
				
					rowcounter = rowcounter + 1	

				#Calculating final Note for Uppercat
				note = 0
				weight = 0
				for finalupcat in downcats_notes:
					note = note + finalupcat[2] * finalupcat[1]
					weight = weight + finalupcat[1]

				#If a Note was calced than save it as Uppercat-Note
				if weight > 0:
					finalnote.append([upcats[1], round(note / weight, 2)])
					note_up = Gtk.Label()
					note_up.set_markup("\n<b>Gesamt ObKa: " + str(round(note / weight, 2)) + "</b>")
					notegrid.attach(note_up, columncounter, rowcounter, 1, 1)
					
				columncounter = columncounter + 3	
				rowcounter = 1

			#Last Notecalc: Final Note of the Student
			finalnotecalc = 0
			weightfinal = 0
			for finalnoteupcat in finalnote:
				finalnotecalc = finalnotecalc + finalnoteupcat[1] * finalnoteupcat[0]
				weightfinal = weightfinal + finalnoteupcat[0]

			#If all Notes are done: Save the final Note of the Student
			if weight > 0:
				studentfinalnote = round(finalnotecalc / weightfinal, 2)
				finallabelnote = Gtk.Label()
				finallabelnote.set_markup("<b><big>Abschlussnote: " + str(studentfinalnote) + "</big></b>")
				
				notegrid.attach(finallabelnote, columncounter + 1, 0, 1, 1)				

			#All Notes to Note-Grid
			#notegrid.attach(notegrid_allnotes, 0, 2, 1, 1)

			#All Grids to Main-Grid
			grid.attach(notegrid, 1, 1, 1, 1)
			grid.attach(statigrid, 0, 1, 1, 1)

			#Reload the Window
			window.show_all()

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
			
			#StudentCombobox			
			students = Gtk.ListStore(int, str)			
			datas = dataop.getdata(con, "select id, name, prename from students order by 2 asc", None)
			#Startfield of Rows
			stucounter = 0
			for row in datas.fetchall():
				students.append([row[0], str(row[1].encode("utf-8")) + ", " + str(row[2].encode("utf-8"))])
				stucounter = stucounter + 1
			
			combobox = Gtk.ComboBox.new_with_model_and_entry(students)			
			combobox.set_entry_text_column(1)
			combobox.set_active(0)
			combobox.connect("changed", updateview, combobox, newviewgrid)
			datagrid_buttons.attach(combobox, 1, 1, 1, 1)

			#Adding Next-Button
			prevstu = Gtk.Button.new_with_label("Vorheriger")
			nextstu = Gtk.Button("Nächster")			
			
			nextstu.connect("clicked", do_nextstu, combobox, stucounter)
			prevstu.connect("clicked", do_prevstu, combobox, stucounter)
	
			datagrid_buttons.attach(prevstu, 0, 1, 1, 1)
			datagrid_buttons.attach(nextstu, 2, 1, 1, 1)

			#Update View with first Student in List
			updateview(None, combobox, newviewgrid)
			#Show the window		
			window.show_all()

		#Fill the Grid for the first time and call this method to reload
		fillDataGrid()
		





