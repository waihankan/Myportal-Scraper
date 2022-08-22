import pandas as pd
import sqlite3 as sql
from os import listdir
from os.path import isfile, join


conn = sql.connect("./database/test.db")
cur = conn.cursor()

# get a list of all csv files in the csv_archive folder
csv_files = [f for f in listdir("./database/csv_archive")
               if isfile(join("./database/csv_archive", f))]

for csv_file in csv_files:
   # read the csv file into a pandas dataframe
   df = pd.read_csv(f"./database/csv_archive/{csv_file}")
   table_name = "deanza_schedule"
   df.to_sql(table_name, conn, if_exists='append', index=False)
   print(f"Saved {csv_file} to {table_name} sqlite database")

conn.close()
