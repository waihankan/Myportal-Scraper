"""
   normalized multiple tables version
   this file is used to insert data into the database SQLite3
   draw a SQLite3 database Relational Diagram
"""


from os import listdir
from os.path import isfile, join
import pandas as pd
import sqlite3 as sql
import regex as re

# Change filepaths to here
DATABASE_FILEPATH = "./database/test2.db"
CSV_FILEPATH = "./database/csv_archive/"

conn = sql.connect(DATABASE_FILEPATH)
cur = conn.cursor()

def insert_course(subj, crse, title, cred):
   cur.execute("INSERT OR IGNORE INTO deanza_course_details VALUES (?, ?, ?, ?)", (subj, crse, title, cred))
   conn.commit()

""" 
Insert into deanza_course_schedule table if not exists
Also implemented to update the Live Data if the course is already in the database
"""

def insert_schedule(term, crn, status, subj, crse, sec, _cmp, coreq, act, rem, wlrem, instructor, date, days, time, location):
   cur.execute("""
   INSERT INTO deanza_course_schedule (Terms, Crn, Status, Subj, Crse, Sec, Cmp, Coreq, Act, Rem, Wlrem, Instructor, Date, Days, Time, Location)
   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
   ON CONFLICT (Terms, Crn) DO
   UPDATE SET Status=excluded.status, Subj=excluded.subj, Crse=excluded.crse, Sec=excluded.sec, Cmp=excluded.cmp, Coreq=excluded.coreq, Act=excluded.act, Rem=excluded.rem, Wlrem=excluded.wlrem, Instructor=excluded.instructor, Date=excluded.date, Days=excluded.days, Time=excluded.time, Location=excluded.location;
   """, (term, crn, status, subj, crse, sec, _cmp, coreq, act, rem, wlrem, instructor, date, days, time, location)
   )
   conn.commit()


def instructor_email_generator(full_name_with_middle_initial):
      full_name = re.sub(r"\s\w*.\s", " ", full_name_with_middle_initial)
      first_name = full_name.split()[0]
      last_name = full_name.split()[1]
      first_email_name = re.sub(r"-", "", first_name).lower()
      last_email_name = re.sub(r"-", "", last_name).lower()
      return f"{last_email_name}{first_email_name}@deanza.edu"

def get_legal_name(full_name_with_middle_initial):
   full_name = re.sub(r"\s\w*.\s", " ", full_name_with_middle_initial)
   first_name = full_name.split()[0]
   last_name = full_name.split()[1]
   return f"{last_name}, {first_name}"


# Insert into deanza_instructors table if not exists
def insert_instructor(instructor, dept):
   if (instructor != "TBA"):
      email = instructor_email_generator(instructor)
      name = get_legal_name(instructor)
      cur.execute("INSERT OR IGNORE INTO deanza_instructors (Instructor_Name, Department, Email, Name) VALUES (?, ?, ?, ?)", (instructor, dept, email, name))
      conn.commit()


# get a list of all csv files in the csv_archive folder
csv_files = [f for f in listdir(CSV_FILEPATH)
               if isfile(join(CSV_FILEPATH, f))]
csv_files.sort()

# loop through all csv files and insert data into the database (3 tables)
for csv_file in csv_files:
   df = pd.read_csv(f"{CSV_FILEPATH}{csv_file}", converters={'Crn': lambda x: str(x)})
   for row in df.itertuples():
      # insert_course(getattr(row, "Subj"), getattr(row, "Crse"), getattr(row, "Title"), getattr(row, "Cred"))
      # insert_schedule(getattr(row, "Terms"), getattr(row, "Crn"), getattr(row, "Status"), getattr(row, "Subj"), getattr(row, "Crse"), getattr(row, "Sec"), getattr(row, "Cmp"), getattr(row, "Coreq"), getattr(row, "Act"), getattr(row, "Rem"), getattr(row, "Wlrem"), getattr(row, "Instructor"), getattr(row, "Date"), getattr(row, "Days"), getattr(row, "Time"), getattr(row, "Location"))
      insert_instructor(getattr(row, "Instructor"), getattr(row, "Subj"))
   print(f"Inserted {csv_file} into database")
conn.close()
