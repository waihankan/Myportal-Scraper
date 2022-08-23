'''
   > multiple entities version
''' 

import pandas as pd
import sqlite3 as sql
from os import listdir
from os.path import isfile, join


conn = sql.connect("./database/test2.db")
cur = conn.cursor()

def insert_course(subj, crse, title, cred):
   cur.execute("INSERT OR IGNORE INTO deanza_course_details VALUES (?, ?, ?, ?)", (subj, crse, title, cred))
   conn.commit()

def insert_schedule(term, crn, status, subj, crse, sec, _cmp, coreq, act, rem, wlrem, instructor, date, days, time, location):
   cur.execute("""
   INSERT INTO deanza_course_schedule (Terms, Crn, Status, Subj, Crse, Sec, Cmp, Coreq, Act, Rem, Wlrem, Instructor, Date, Days, Time, Location)
   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
   ON CONFLICT (Terms, Crn) DO
   UPDATE SET Status=excluded.status, Subj=excluded.subj, Crse=excluded.crse, Sec=excluded.sec, Cmp=excluded.cmp, Coreq=excluded.coreq, Act=excluded.act, Rem=excluded.rem, Wlrem=excluded.wlrem, Instructor=excluded.instructor, Date=excluded.date, Days=excluded.days, Time=excluded.time, Location=excluded.location;
   """, (term, crn, status, subj, crse, sec, _cmp, coreq, act, rem, wlrem, instructor, date, days, time, location)
   )
   conn.commit()

def insert_instructor(instructor):
   cur.execute("INSERT OR IGNORE INTO deanza_instructors (Instructor_Name) VALUES (?)", (instructor,))
   conn.commit()


# get a list of all csv files in the csv_archive folder
csv_files = [f for f in listdir("./database/csv_archive")
               if isfile(join("./database/csv_archive", f))]
csv_files.sort()

for csv_file in csv_files:
   # read the csv file into a pandas dataframe
   df = pd.read_csv(f"./database/csv_archive/{csv_file}", converters={'Crn': lambda x: str(x)})
   for row in df.itertuples():
      insert_course(getattr(row, "Subj"), getattr(row, "Crse"), getattr(row, "Title"), getattr(row, "Cred"))
      insert_schedule(getattr(row, "Terms"), getattr(row, "Crn"), getattr(row, "Status"), getattr(row, "Subj"), getattr(row, "Crse"), getattr(row, "Sec"), getattr(row, "Cmp"), getattr(row, "Coreq"), getattr(row, "Act"), getattr(row, "Rem"), getattr(row, "Wlrem"), getattr(row, "Instructor"), getattr(row, "Date"), getattr(row, "Days"), getattr(row, "Time"), getattr(row, "Location"))
      insert_instructor(getattr(row, "Instructor"))
   print(f"Inserted {csv_file} into database")
conn.close()
