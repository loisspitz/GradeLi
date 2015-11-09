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

class ShowOverview():	

	#First Method called ba Mainclasses.py
	#Needs the actual window-object to change label "view"
	def start(self, classname, builder, window):

		#Databaseconnection
		dataop = DataOp()
		con = dataop.opendatabase(classname)

		#Returns all UpperCat-Notes and the Final-Note as an array
		#Last Entry will be the Finalnote (if there is one :) )		
		def calculateOkFinal(id):
			dataarray = []
			cur = con.cursor()
			#Calculating all Downcategories and save them to downcat with the Categorie-ID
			
			#Step One - Getting all Upper Cats
			data_upcats = cur.execute("select id, weight, name from catup order by weight desc")
			rowcounter = 1
			columncounter = 0
			finalnote = []
			for upcats in data_upcats.fetchall():
				#Step Two: Get all Down-Cats with this Upcat-ID
				data_downcats = cur.execute("select id, weight, name from catdown where upcat=?", (int(upcats[0]), ))
				downcats_notes = []
				for downcats in data_downcats.fetchall():					
					#Step Three: Get all Notes from this DownCat and Upcat from actual Student
					data_notes = cur.execute("select id,weight ,name from notes where upcat=? and downcat=?", (upcats[0], downcats[0]),)
					weight_note = 0
					note_calc = 0
					for notes in data_notes.fetchall():
						#Step Four: Getting the final note
						try:
							data_stunote = cur.execute("select id, note from notes_student where studentid=? and notesid=? and note!=16.0", (id, notes[0],)).fetchone()[1]						
							#
							#	SPECIAL: All Notes with 16.0 will not be calculatet!!!! Here beware by other Gradesystems!!!
							#
							#
							weight_note = weight_note + notes[1]
							note_calc = note_calc + data_stunote * notes[1]
						except:
							rowcounter = rowcounter + 1
							break
					
					#Saving all Downcategorie-Notes ID WEIGHT NOTE
					if weight_note > 0:
						downcats_notes.append([downcats[0], downcats[1], round(note_calc / weight_note, 2)])

				#Calculating final Note for Uppercat
				note = 0
				weight = 0
				for finalupcat in downcats_notes:
					note = note + finalupcat[2] * finalupcat[1]
					weight = weight + finalupcat[1]

				#If a Note was calced than save it as Uppercat-Note
				if weight > 0:
					finalnote.append([upcats[1], round(note / weight, 2)])		
					dataarray.append(round(note / weight, 2))			
				
			#Last Notecalc: Final Note of the Student
			finalnotecalc = 0
			weightfinal = 0
			for finalnoteupcat in finalnote:
				finalnotecalc = finalnotecalc + finalnoteupcat[1] * finalnoteupcat[0]
				weightfinal = weightfinal + finalnoteupcat[0]

			#If all Notes are done: Save the final Note of the Student
			if weight > 0:
				dataarray.append(round(finalnotecalc / weightfinal, 2))		
				
			return dataarray

		#Returns an Array of all counted data
		def gettingCounts(studentid):
			dataarray = []
			unknown = dataarray.append(dataop.getdata(con, "select count(status) from status_stu_unit where studentid=? and status=0", studentid).fetchone()[0])
			leaveok = dataarray.append(dataop.getdata(con, "select count(status) from status_stu_unit where studentid=? and status=1", studentid).fetchone()[0])
			school = dataarray.append(dataop.getdata(con, "select count(status) from status_stu_unit where studentid=? and status=2", studentid).fetchone()[0])
			minusminus = dataarray.append(dataop.getdata(con, "select count(status) from status_stu_unit where studentid=? and status=3", studentid).fetchone()[0])
			minus = dataarray.append(dataop.getdata(con, "select count(status) from status_stu_unit where studentid=? and status=4", studentid).fetchone()[0])
			mid = dataarray.append(dataop.getdata(con, "select count(status) from status_stu_unit where studentid=? and status=5", studentid).fetchone()[0])
			plus = dataarray.append(dataop.getdata(con, "select count(status) from status_stu_unit where studentid=? and status=6", studentid).fetchone()[0])
			plusplus = dataarray.append(dataop.getdata(con, "select count(status) from status_stu_unit where studentid=? and status=7", studentid).fetchone()[0])
			
			return dataarray

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

			#Adding Column-Infos
			#Images			
			ue_r = Gtk.Image()
			ue_r.set_from_file("icons/quest_red.png")	
			newviewgrid.attach(ue_r, 4, 0, 1, 1)

			#OK leaved
			e_g = Gtk.Image()
			e_g.set_from_file("icons/ok_green.png")
			newviewgrid.attach(e_g, 6, 0, 1, 1)

			#School-Event
			school_g = Gtk.Image()
			school_g.set_from_file("icons/school_green.png")			
			newviewgrid.attach(school_g, 8, 0, 1, 1)

			#PLusPlus Work
			minusminus_g = Gtk.Image()
			minusminus_g.set_from_file("icons/minusminus_green.png")
			newviewgrid.attach(minusminus_g, 10, 0, 1, 1)

			#One Minus Work
			minus_g = Gtk.Image()
			minus_g.set_from_file("icons/minus_green.png")
			newviewgrid.attach(minus_g, 12, 0, 1, 1)

			#MIddle good work
			middle_g = Gtk.Image()
			middle_g.set_from_file("icons/middle_green.png")
			newviewgrid.attach(middle_g, 14, 0, 1, 1)

			#One Plus Work
			plus_g = Gtk.Image()
			plus_g.set_from_file("icons/plus_green.png")			
			newviewgrid.attach(plus_g, 16, 0, 1, 1)

			#PLusPlus Work
			plusplus_g = Gtk.Image()		
			plusplus_g.set_from_file("icons/plusplus_green.png")
			newviewgrid.attach(plusplus_g, 18, 0, 1, 1)

			
  			#Getting UpCats
  			cur = con.cursor()
  			data_upcats = cur.execute("select short from catup order by weight desc")
  			counter = 0
  			for upcats in data_upcats.fetchall():
  				label_ok = Gtk.Label()
  				label_ok.set_markup("<b>" + upcats[0].encode("utf-8") + "</b>")
  				newviewgrid.attach(label_ok, counter + 20, 0, 1, 1)
  				counter = counter + 2

  			#Label Finalnote
			label_note = Gtk.Label()
			label_note.set_markup("<b>Abschlussnote</b>")
  			newviewgrid.attach(label_note, counter + 22, 0, 1, 1)

			#Adding Spacer
			for i in xrange(3,23 + counter,2):
  				templabel = Gtk.Label("     ")
  				newviewgrid.attach(templabel, i, 0, 1, 1)
			
			#Adding Studentsnames - Postname, Prenames, Numbers and Buttons
			datas = dataop.getdata(con, "select id, name, prename, mail from students order by 2 asc", None)
			#Startfield of Rows
			startfield_rows = 1
			for row in datas.fetchall():
				templabel_numbers = Gtk.Label()
				templabel_postname = Gtk.Label()
				templabel_prename = Gtk.Label()

				templabel_numbers.set_markup("     <b><big>" + str(startfield_rows) + ".</big></b>  ")
				templabel_postname.set_markup("<b><big>" + row[1].encode("utf-8") + "</big></b> ")
				templabel_prename.set_markup("<b><big>" + row[2].encode("utf-8") + "</big></b> ")
				
				#COLOR 0-65535 Gdk.Color(RED, GREEN, BLUE)
				if startfield_rows % 2 != 0:
					templabel_postname.modify_bg(0, Gdk.Color(52000, 52000, 52000))
					templabel_prename.modify_bg(0, Gdk.Color(52000, 52000, 52000))
					templabel_numbers.modify_bg(0, Gdk.Color(52000, 52000, 52000))

				#Getting the Students Notes notes[LAST] = final notes, all before UpperCats
				notes = calculateOkFinal(row[0])
				upcatcount = 0
				cattogo = len(notes) - 1
				for notes_to_label in range(cattogo):
					upcattemp = Gtk.Label(notes[notes_to_label])
					if startfield_rows % 2 != 0:
						upcattemp.modify_bg(0, Gdk.Color(52000, 52000, 52000))
					
					newviewgrid.attach(upcattemp, 20 + upcatcount, startfield_rows, 1, 1)
					upcatcount = upcatcount + 2

				#Adding Final Note
				if cattogo > 0:
					finalnote = Gtk.Label()
					finalnote.set_markup("<b>" + str(notes[cattogo]) + "</b>")
					if startfield_rows % 2 != 0:
						finalnote.modify_bg(0, Gdk.Color(52000, 52000, 52000))

					newviewgrid.attach(finalnote, 22 + upcatcount, startfield_rows, 1, 1)

				#Make the lines grey if 2nd
				if startfield_rows % 2 != 0:
					templabel_postname.modify_bg(0, Gdk.Color(52000, 52000, 52000))
					templabel_prename.modify_bg(0, Gdk.Color(52000, 52000, 52000))
					templabel_numbers.modify_bg(0, Gdk.Color(52000, 52000, 52000))

				#Adding Grey or White Spacers
				for i in xrange(3,23 + counter,2):
	  				templabel = Gtk.Label("     ")
	  				if startfield_rows % 2 != 0:
	  					templabel.modify_bg(0, Gdk.Color(52000, 52000, 52000))	
	  				
	  				newviewgrid.attach(templabel, i, startfield_rows, 1, 1)

	  			#Adding Countet Data
	  			counts = gettingCounts(row[0])
	  			rowspacer = 4
	  			for countet in counts:
	  				templabel = Gtk.Label(str(countet))
	  				if startfield_rows % 2 != 0:
	  					templabel.modify_bg(0, Gdk.Color(52000, 52000, 52000))	
	  				
	  				newviewgrid.attach(templabel, rowspacer, startfield_rows, 1, 1)
	  				rowspacer = rowspacer + 2

				newviewgrid.attach(templabel_postname, 1, startfield_rows, 1, 1)
				newviewgrid.attach(templabel_prename, 2, startfield_rows, 1, 1)
				newviewgrid.attach(templabel_numbers, 0, startfield_rows, 1, 1)
				startfield_rows = startfield_rows + 1

			#Show the window		
			window.show_all()

		#Fill the Grid for the first time and call this method to reload
		fillDataGrid()
		





