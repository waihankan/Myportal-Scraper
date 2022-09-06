#!/usr/bin/python3
from fetch_data import FetchDataRequests
import pandas as pd
import sqlite3 as sql



CURRENT_TERM = "202322"  # <---- edit the term here 

HTML_FILEPATH = "./database/html_archive/"
CSV_FILEPATH = "./database/csv_archive/"
DATABASE_FILEPATH = "./database/test2.db"
SQL_COL_LIST = ["Status", "Crn", "Coreq", "Subj", "Crse",
               "Sec", "Cmp", "Cred", "Title", "Days", "Time",
               "Act", "Rem", "Wlrem", "Instructor", "Date", 
               "Location"] 
N = 17  # number of useful columns in the html file


# FetchDataRequests().archive_one_term(CURRENT_TERM) 

conn = sql.connect(DATABASE_FILEPATH)
cur = conn.cursor()

def insert_schedule(term, crn, status, subj, crse, sec, _cmp, coreq, act, rem, wlrem, instructor, date, days, time, location):
   cur.execute("""
   INSERT INTO deanza_course_schedule (Terms, Crn, Status, Subj, Crse, Sec, Cmp, Coreq, Act, Rem, Wlrem, Instructor, Date, Days, Time, Location)
   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
   ON CONFLICT (Terms, Crn) DO
   UPDATE SET Status=excluded.status, Subj=excluded.subj, Crse=excluded.crse, Sec=excluded.sec, Cmp=excluded.cmp, Coreq=excluded.coreq, Act=excluded.act, Rem=excluded.rem, Wlrem=excluded.wlrem, Instructor=excluded.instructor, Date=excluded.date, Days=excluded.days, Time=excluded.time, Location=excluded.location;
   """, (term, crn, status, subj, crse, sec, _cmp, coreq, act, rem, wlrem, instructor, date, days, time, location)
   )
   conn.commit()

def update_csv(term):
   df = pd.read_html(f"{HTML_FILEPATH}{term}.html")
   df = df[5].iloc[: , :N]
   df.columns = SQL_COL_LIST   # overwrite the headers for sql columns
   df["Instructor"] = df["Instructor"].str.replace(r' \(P\)', '', regex=True)  # clean up instructor names and remove the (P) from the end
   df = df[df['Date'].str.contains('/\d\d-', regex=True)]  # filter out the rows that are not schedules of classes
   df.insert(0, 'Terms', term)
   # save the dataframe to a csv file
   df.to_csv(f"{CSV_FILEPATH}{term}.csv", index=False, encoding='utf-8')
   print(f"Saved {term} to csv file")

        
def update_database(term):
   df = pd.read_csv(f"{CSV_FILEPATH}{term}.csv", converters={'Crn': lambda x: str(x)})
   for row in df.itertuples():
      insert_schedule(getattr(row, "Terms"), getattr(row, "Crn"), getattr(row, "Status"), getattr(row, "Subj"), getattr(row, "Crse"), getattr(row, "Sec"), getattr(row, "Cmp"), getattr(row, "Coreq"), getattr(row, "Act"), getattr(row, "Rem"), getattr(row, "Wlrem"), getattr(row, "Instructor"), getattr(row, "Date"), getattr(row, "Days"), getattr(row, "Time"), getattr(row, "Location"))
   print(f"Saved {term} to database")


def main():
   print("started")
   fetcher = FetchDataRequests()
   while True:
      conn = sql.connect(DATABASE_FILEPATH)
      cur = conn.cursor()
      index = 1
      fetcher.archive_one_term(CURRENT_TERM)
      update_csv(CURRENT_TERM)
      update_database(CURRENT_TERM)
      index += 1
      print(index)

if __name__ == "__main__":
   main()
