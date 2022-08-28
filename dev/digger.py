#!/usr/bin/python3

""" Implement all the functions for retrieving data from the database. """


import sqlite3
from multipledispatch import dispatch


class Digger:
   """ Definitly not a gold digger LOL"""
   def __init__(self, database_filepath):
      self.database_filepath = database_filepath
      
      # connect to the database
      self.conn = sqlite3.connect(self.database_filepath)
      self.cur = self.conn.cursor()


   def waitlist_viewer(self, instructor, subj, crse, lines=5):
      """ 
      This function will return raw waitlist data for a specific instructor, subject, and course

      Parameters:
      instructor (str): instructor name, accept partial name, case insensitive, e.g. "John" will return all instructors with "John" in their name
      subj (str): subject, case insensitive
      crse (str): course number, case insensitive
      lines (int): number of lines to return, default is 5

      """
      self.cur.execute('''
         SELECT Terms, Subj, Crse, Act, Rem, Wlrem, Instructor, Location FROM deanza_course_schedule
         WHERE Instructor LIKE ? COLLATE NOCASE AND Subj = ? AND Crse = ?
         ORDER BY Terms DESC
         LIMIT ?;
         ''', 
      (f"%{instructor.split()[0]}%", subj.upper(), crse.upper(), lines))
      return self.cur.fetchall()

   @dispatch(str, str)
   def schedule_finder(self, term, subj):
      """ 
      This function will return raw schedule data for a specific term and subject

      Parameters:
      term (str): term, e.g. "202322"
      subj (str): subject, case insensitive

      """
      self.cur.execute('''
         SELECT Terms, Crn, Coreq, deanza_course_schedule.Subj, deanza_course_schedule.Crse, deanza_course_details.Title, Sec, Cmp, Act, Rem, Wlrem,
         Instructor, Date, Days, Time, Location
         FROM deanza_course_schedule
         LEFT JOIN deanza_course_details
         ON deanza_course_schedule.Subj = deanza_course_details.Subj AND deanza_course_schedule.Crse = deanza_course_details.Crse
         WHERE Terms = ? AND deanza_course_schedule.Subj = ?
         ORDER BY deanza_course_details.Crse DESC, Act DESC, Rem ASC, Wlrem ASC;
         ''', 
      (term, subj.upper()))
      return self.cur.fetchall()


   @dispatch(str, str, str)
   def schedule_finder(self, term, subj, crse):
      """ 
      This function will return raw schedule data for a specific term, subject, and course

      Parameters:
      term (str): term, e.g. "202322"
      subj (str): subject, case insensitive
      crse (str): course number, case insensitive

      """
      self.cur.execute('''
         SELECT Terms, Crn, Coreq, deanza_course_schedule.Subj, deanza_course_schedule.Crse, deanza_course_details.Title, Sec, Cmp, Act, Rem, Wlrem,
         Instructor, Date, Days, Time,
         Location FROM deanza_course_schedule
         LEFT JOIN deanza_course_details
         ON deanza_course_schedule.Subj = deanza_course_details.Subj AND deanza_course_schedule.Crse = deanza_course_details.Crse
         WHERE Terms = ? AND deanza_course_schedule.Subj = ? AND deanza_course_schedule.Crse = ?
         ORDER BY Act DESC, Rem ASC, Wlrem ASC;
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
         SELECT Terms, Crn, Coreq, deanza_course_schedule.Subj, deanza_course_schedule.Crse, deanza_course_details.Title, Sec, Cmp, Act, Rem, Wlrem,
         Instructor, Date, Days, Time,
         Location FROM deanza_course_schedule
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
            

   @dispatch(str, lines=int)
   def prof_grade_info(self, instructor, lines=5):
      """
      This function will return raw grade distribution data for a specific instructor
      
      Parameters:
      instructor (str): instructor name, case insensitive
      lines (int): number of lines to return, default is 5
      
      """
      self.cur.execute('''
         SELECT Year, Semester, Instructor, Subj, Crse, A, B, C, D, F, W FROM deanza_transfer_camp
         WHERE Instructor LIKE ? COLLATE NOCASE
         ORDER BY Year DESC
         LIMIT ?;
         ''', 
      (f"%{instructor.split()[0]}%", lines))
      return self.cur.fetchall()


   @dispatch(str, str, lines=int)
   def prof_grade_info(self, instructor, subj, lines=5):
      """
      This function will return raw grade distribution data for a specific instructor
      
      Parameters:
      instructor (str): instructor name, case insensitive
      subj (str): subject, case insensitive
      lines (int): number of lines to return, default is 5
      
      """
      self.cur.execute('''
         SELECT Year, Semester, Instructor, Subj, Crse, A, B, C, D, F, W FROM deanza_transfer_camp
         WHERE Instructor LIKE ? COLLATE NOCASE AND Subj = ?
         ORDER BY Year DESC
         LIMIT ?;
         ''', 
      (f"%{instructor.split()[0]}%", subj.upper(), lines))
      return self.cur.fetchall()

   @dispatch(str, str, str, lines=int)
   def prof_grade_info(self, instructor, subj, crse, lines=5):
      """
      This function will return raw grade distribution data for a specific instructor and course
      
      Parameters:
      instructor (str): instructor name, case insensitive
      subj (str): subject, case insensitive
      crse (str): course number, case insensitive
      lines (int): number of lines to return, default is 5
      
      """
      self.cur.execute('''
         SELECT Year, Semester, Instructor, Subj, Crse, A, B, C, D, F, W FROM deanza_transfer_camp
         WHERE Instructor LIKE ? COLLATE NOCASE AND Subj = ? AND Crse = ?
         ORDER BY Year DESC
         LIMIT ?;
         ''', 
      (f"%{instructor.split()[0]}%", subj.upper(), crse.upper(), lines))
      return self.cur.fetchall()


   def who_is(self, instructor):
      """
      This function will return instructor information for a specific instructor
      
      Parameters:
      instructor (str): instructor name, case insensitive
      
      """
      self.cur.execute('''
         SELECT Instructor_Name, Department, Email FROM deanza_instructors
         WHERE Name LIKE ? COLLATE NOCASE
         LIMIT 1;
         ''', 
      (f"%{instructor.split()[0]}%",))
      return self.cur.fetchall()
      