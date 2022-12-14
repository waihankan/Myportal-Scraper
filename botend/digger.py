#!/usr/bin/python3

""" Implement all the functions for retrieving data from the database. """


import sqlite3
from multipledispatch import dispatch
from datetime import datetime


class Digger:
   """ Definitly not a gold digger LOL"""
   def __init__(self, database_filepath):
      self.database_filepath = database_filepath
      
      # connect to the database
      self.conn = sqlite3.connect(self.database_filepath)
      self.cur = self.conn.cursor()

   def bot_usage(self, name):
      """ 
      This function will add the number of times each command is used

      """
      self.cur.execute('''
         UPDATE bot_usage SET counter = counter + 1 WHERE Command = ?;
         ''', (name,))
      self.conn.commit()
   
   def bot_usage_viewer(self):
      """ 
      This function will return raw bot usage data

      """
      self.cur.execute('''
         SELECT SUM(Counter) FROM bot_usage;
         ''')
      return self.cur.fetchall()

   def get_updated_time(self):
      """ 
      This function will return the time when the database was last updated

      """
      self.cur.execute('''
         SELECT Updated_time FROM submission_time;
         ''')
      return self.cur.fetchall()

   def waitlist_viewer_crse(self, instructor, subj, crse):
      """ 
      This function will return raw waitlist data for a specific instructor, subject, and course

      Parameters:
      instructor (str): instructor name, accept partial name, case insensitive, e.g. "John" will return all instructors with "John" in their name
      subj (str): subject, case insensitive
      crse (str): course number, case insensitive

      """
      LINES = 10
      self.cur.execute('''
         SELECT Terms, Subj, Crse, Act, Rem, Wlrem, Instructor, Location FROM deanza_course_schedule
         WHERE Instructor LIKE ? COLLATE NOCASE AND Subj = ? AND Crse = ?
         ORDER BY Terms DESC
         LIMIT ?;
         ''', 
      (f"%{instructor.split()[0]}%", subj.upper(), crse.upper(), LINES))
      return self.cur.fetchall()

   def waitlist_viewer_prof(self, instructor, subj):
      """ 
      This function will return raw waitlist data for a specific instructor, subject, and course

      Parameters:
      instructor (str): instructor name, accept partial name, case insensitive, e.g. "John" will return all instructors with "John" in their name
      subj (str): subject, case insensitive

      """
      LINES = 10
      self.cur.execute('''
         SELECT Terms, Subj, Crse, Act, Rem, Wlrem, Instructor, Location FROM deanza_course_schedule
         WHERE Instructor LIKE ? COLLATE NOCASE AND Subj = ?
         ORDER BY Terms DESC
         LIMIT ?;
         ''', 
      (f"%{instructor.split()[0]}%", subj.upper(), LINES))
      return self.cur.fetchall()

   def search_by_term_subj(self, term, subj):
      """ 
      This function will return raw schedule data for a specific term and subject

      Parameters:
      term (str): term, e.g. "202322"
      subj (str): subject, case insensitive

      """
      self.cur.execute('''
         SELECT Crn, deanza_course_schedule.Subj, deanza_course_schedule.Crse, Act, Rem, Wlrem,
         Instructor, Days, Time, Location
         FROM deanza_course_schedule
         LEFT JOIN deanza_course_details
         ON deanza_course_schedule.Subj = deanza_course_details.Subj AND deanza_course_schedule.Crse = deanza_course_details.Crse
         WHERE Terms = ? AND deanza_course_schedule.Subj = ?
         ''', 
      (term, subj.upper()))
      return self.cur.fetchall()

   def search_by_term_subj_crse(self, term, subj, crse):
      """ 
      This function will return raw schedule data for a specific term, subject, and course

      Parameters:
      term (str): term, e.g. "202322"
      subj (str): subject, case insensitive
      crse (str): course number, case insensitive

      """
      self.cur.execute('''
         SELECT Crn, deanza_course_schedule.Subj, deanza_course_schedule.Crse, Act, Rem, Wlrem,
         Instructor, Days, Time, Location
         FROM deanza_course_schedule
         LEFT JOIN deanza_course_details
         ON deanza_course_schedule.Subj = deanza_course_details.Subj AND deanza_course_schedule.Crse = deanza_course_details.Crse
         WHERE Terms = ? AND deanza_course_schedule.Subj = ? AND deanza_course_schedule.Crse = ?
         ORDER BY Rem ASC, Wlrem ASC;
         ''', 
         (term, subj.upper(), crse.upper()))
      return self.cur.fetchall()

   def search_by_crn(self, term, crn):
      """ 
      This function will return raw schedule data for a specific term and crn

      Parameters:
      term (str): term, e.g. "202322"
      crn (int): course registration number

      """
      self.cur.execute('''
         SELECT Crn, deanza_course_schedule.Subj, deanza_course_schedule.Crse, Act, Rem, Wlrem,
         Instructor, Days, Time, Location
         FROM deanza_course_schedule
         LEFT JOIN deanza_course_details
         ON deanza_course_schedule.Subj = deanza_course_details.Subj AND deanza_course_schedule.Crse = deanza_course_details.Crse
         WHERE Terms = ? AND Crn = ?
         ORDER BY Act DESC, Rem ASC, Wlrem ASC;
         ''', 
      (term, crn))
      return self.cur.fetchall()

   def term_parser(self, term):
      if(len(term) != 6):
         return "Invalid term"
      else:
         campus = term[5:6]
         if campus == "1":
            campus = "FH"
         elif campus == "2":
            campus = "DA"
         else:
            return "Invalid term"

         year = term[0:4]
         quarter = term[4:5]
         if(quarter == "1"):
            return f"{int(year) - 1} Summer {campus}"
         elif(quarter == "2"):
            return f"{int(year) - 1} Fall {campus}"
         elif(quarter == "3"):
            return f"{year} Winter {campus}"
         elif(quarter == "4"):
            return f"{year} Spring {campus}"
         else:
            return "Invalid term"

   def course_parser(self, crse):
      if(len(crse) > 5):
         return "Invalid course number"

      elif(len(crse) == 5):
         return crse

      elif(len(crse) < 5):
         if(len(crse) == 1):
            return f"D00{crse}."
         elif(len(crse) == 2 and not crse.isdigit()):
            return f"D00{crse}"
         elif(len(crse) == 2 and crse.isdigit()):
            return f"D0{crse}."
         elif(len(crse) == 3 and not crse.isdigit()):
            return f"D0{crse}"
         elif(len(crse) == 3 and crse.isdigit()):
            return f"D{crse}."
         elif(len(crse) == 4):
            return f"D{crse}"

   @dispatch(str)
   def prof_grade_info(self, instructor):
      """
      This function will return raw grade distribution data for a specific instructor
      
      Parameters:
      instructor (str): instructor name, case insensitive
      lines (int): number of lines to return, default is 5
      
      """
      LINES = 10
      self.cur.execute('''
         SELECT Year, Semester, Instructor, Subj, Crse, A, B, C, D, F, W FROM deanza_transfer_camp
         WHERE Instructor LIKE ? COLLATE NOCASE
         ORDER BY Year DESC
         LIMIT ?;
         ''', 
      (f"%{instructor.split()[0]}%", LINES))
      return self.cur.fetchall()

   @dispatch(str, str)
   def prof_grade_info(self, subj, crse):
      LINES = 10
      self.cur.execute('''
         SELECT Year, Semester, Instructor, Subj, Crse, A, B, C, D, F, W FROM deanza_transfer_camp
         WHERE Subj = ? AND Crse = ?
         ORDER BY A DESC, B DESC, C DESC, D DESC, F ASC, W DESC
         LIMIT ?;
         ''',
      (subj.upper(), crse.upper(), LINES))
      return self.cur.fetchall()

   @dispatch(str, str, str)
   def prof_grade_info(self, instructor, subj, crse):
      """
      This function will return raw grade distribution data for a specific instructor
      
      Parameters:
      instructor (str): instructor name, case insensitive
      lines (int): number of lines to return, default is 5
      
      """
      LINES = 10
      self.cur.execute('''
         SELECT Year, Semester, Instructor, Subj, Crse, A, B, C, D, F, W FROM deanza_transfer_camp
         WHERE Instructor LIKE ? COLLATE NOCASE AND Subj = ? AND Crse = ?
         ORDER BY Year DESC
         LIMIT ?;
         ''', 
      (f"%{instructor.split()[0]}%", subj.upper(), crse.upper(), LINES))
      return self.cur.fetchall()

   def who_is(self, instructor):
      """
      This function will return instructor information for a specific instructor
      
      Parameters:
      instructor (str): instructor name, case insensitive
      
      """
      if len(instructor.split()) == 1:
         self.cur.execute('''
            SELECT Instructor_Name, Department, Email, Phone_Number FROM deanza_instructors
            WHERE Instructor_Name LIKE ? COLLATE NOCASE;
            ''', 
         (f"%{instructor.split()[0]}%",))
      elif len(instructor.split()) >= 2:
         self.cur.execute('''
            SELECT Instructor_Name, Department, Email, Phone_Number FROM deanza_instructors
            WHERE Instructor_Name LIKE ? COLLATE NOCASE;
            ''', 
         (f"%{instructor.split()[0]}%{instructor.split()[1]}%",))
      else:
         return []
      return self.cur.fetchall()
