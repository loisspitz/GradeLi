#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Database-Operations
#
#Import SQLIte
import sqlite3 as lite

#GLOBAL VARIABLES
#Control-Database - DO NOT CHANGE
database = 'GradeLiControl.db'

############### THE DEFAULT-PATH COULD BE CHANGE LATER IN A FILE #########
#
#
#
default_path = "../GradeLi Classes/"
#
#
#
#########################################################################

class DataOp():	


	#Create a new Database for Classes with Classname
	def newdatabase(self, classname):
		#Create new Database-File in "database" if not exists		
		con = lite.connect(default_path + classname + '.db')
		#Creating all Tables needed in a Class-Database
		#Set the Database-Cursor
		cur = con.cursor()
		#Students
		cur.execute("create table students (id INT PRIMARY KEY NOT NULL, name TEXT, prename TEXT, mail TEXT);")
		#Units
		cur.execute("create table units (id INT PRIMARY KEY NOT NULL, year INT, month INT, day INT, title TEXT, desc TEXT);")
		#CATEGORIES
		#up
		cur.execute("create table catup (id INT PRIMARY KEY NOT NULL, name TEXT, short TEXT, weight INT);")
		#Down
		cur.execute("create table catdown (id INT PRIMARY KEY NOT NULL, upcat INT NOT NULL, name TEXT, short TEXT, weight INT);")
		#Notes
		cur.execute("create table notes (id INT PRIMARY KEY NOT NULL, name TEXT, weight INT NOT NULL, upcat INT NOT NULL, downcat INT NOT NULL, year TEXT, month TEXT, day TEXT);")
		#Notes of the Student
		cur.execute("create table notes_student (id INT PRIMARY KEY NOT NULL, notesid INT NOT NULL, studentid INT NOT NULL, note FLOAT NOT NULL);")
		#
		#
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
		#		
		cur.execute("create table status_stu_unit (id INT PRIMARY KEY NOT NULL, studentid INT NOT NULL, unitid INT NOT NULL, status INT NOT NULL);")		
		#Do Querys
		con.commit()
		return con

	#Open Class-Database
	def opendatabase(self, databasename):		
		con = lite.connect(default_path + databasename + '.db')
		return con

	#Open the ControlDatabase (different becaus of a different directory)
	def opencontroldata(*args):
		con = lite.connect(database)
		return con

	#Close Database
	def closedatabase(self, con):
		con.close()

	#Execute a Query
	def executequery(self, con, query, stuff):
		cur = con.cursor()
		if stuff == None:
			cur.execute(query)
		else:
			cur.execute(query, (stuff,))		
		con.commit()
		
	#Return some Data
	def getdata(self, con, query, stuff):
		cur = con.cursor()
		if stuff == None:
			cur.execute(query)
		else:
			cur.execute(query, (stuff,))		
		return cur

	#Delete a Student
	#############################
	#
	#  MISSING: All other tables (later addet) needs to delete same student!!!
	#
	############################
	def deleteStudentComplete(self, con, id):
		cur = con.cursor()
		#Delete from Table students
		cur.execute("delete from students where id=?", (id,))	
		cur.execute("delete from status_stu_unit where studentid=?", (id,))
		con.commit()

	#Delete a Unit from Table units
	def deleteUnitComplete(self, con, id):
		cur = con.cursor()
		#Delete from Table students
		cur.execute("delete from units where id=?", (id,))
		#Delete alle UnitStatus-Entry for this Unit	
		cur.execute("delete from status_stu_unit where unitid=?", (id,))
		con.commit()


	#NOTES

	#Delete a Upper-Cateogire
	#
	#
	# MISSING: HERE WE NEED TO DELETE ALL DOWN-Categories and Notes with these Uppercategorie!
	def deleteCatUp(self, con, id):
		cur = con.cursor()
		data_cur = cur.execute("select id from notes where upcat=?", (id,))
		for data in data_cur.fetchall():
			cur.execute("delete from notes where id=?", (data[0],))
			cur.execute("delete from notes_student where notesid=?", (data[0],))

		cur.execute("delete from catdown where upcat=?", (id,))
		#Delete from Table catup
		cur.execute("delete from catup where id=?", (id,))
		
		con.commit()

	#Delete a Down-Categorie
	def deleteCatDown(self, con, id):
		cur = con.cursor()
		#Delete all Notes and Notes_Students with these CatDown-Id
		data_cur = cur.execute("select id from notes where downcat=?", (id,))
		for data in data_cur.fetchall():
			cur.execute("delete from notes_student where notesid=?", (data[0],))
			cur.execute("delete from notes where id=?", (data[0],))
			
		#Delete from Table catup
		cur.execute("delete from catdown where id=?", (id,))
		con.commit()

	#Delete a Note
	def deleteNoteComplete(self, con, id):
		cur = con.cursor()
		#Delete from Table catup
		cur.execute("delete from notes_student where notesid=?", (id,))
		cur.execute("delete from notes where id=?", (id,))		
		con.commit()