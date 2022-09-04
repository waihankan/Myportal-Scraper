from os import listdir
from os.path import isfile, join
import pandas as pd
import sqlite3 as sql


DATABASE_FILEPATH = "./database/test2.db"
CSV_FILEPATH = "./database/transfer_csv_archive/"

conn = sql.connect(DATABASE_FILEPATH)
cur = conn.cursor()

def edit_crse(crse):
   if len(crse) == 4:
      return f"{crse}."
   else:
      return crse

def insert_transfer_camp(year, semester, instructor, subj, crse, a, b, c, d, f, w):
   cur.execute("INSERT OR IGNORE INTO deanza_transfer_camp VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (year, semester, instructor, subj, crse, a, b, c, d, f, w))
   conn.commit()


csv_files = [f for f in listdir(CSV_FILEPATH) if isfile(join(CSV_FILEPATH, f))]
csv_files.sort()


for csv_file in csv_files:
   df = pd.read_csv(f"{CSV_FILEPATH}{csv_file}")
   for row in df.itertuples():
      insert_transfer_camp(getattr(row, "Year"), getattr(row, "Semester"), getattr(row, "Instructor"), getattr(row, "Subj"), edit_crse(getattr(row, "Crse")), getattr(row, "A"), getattr(row, "B"), getattr(row, "C"), getattr(row, "D"), getattr(row, "F"), getattr(row, "W"))
   print(f"Inserted {csv_file} into database")

conn.close()
