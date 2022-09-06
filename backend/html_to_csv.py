#!/usr/bin/python
"""
   Script to parse the data from html file into csv using pandas library.
"""


import pandas as pd
from os import listdir
from os.path import isfile, join


# Change Database filepath here
HTML_FILEPATH = "./database/html_archive/"
CSV_FILEPATH = "./database/csv_archive/"
SQL_COL_LIST = ["Status", "Crn", "Coreq", "Subj", "Crse",
               "Sec", "Cmp", "Cred", "Title", "Days", "Time",
               "Act", "Rem", "Wlrem", "Instructor", "Date", 
               "Location"] 
N = 17  # number of useful columns in the html file

# get a list of all the html files in the html_archive folder
html_files = [f for f in listdir(HTML_FILEPATH) 
               if isfile(join(HTML_FILEPATH, f))]
html_files.sort()

for html_file in html_files:
   df = pd.read_html(f"{HTML_FILEPATH}{html_file}")
   df  = df[5].iloc[: , :N]
   df.columns = SQL_COL_LIST   # overwrite the headers for sql columns
   df["Instructor"] = df["Instructor"].str.replace(r' \(P\)', '', regex=True)  # clean up instructor names and remove the (P) from the end
   df = df[df['Date'].str.contains('/\d\d-', regex=True)]  # filter out the rows that are not schedules of classes
   df.insert(0, 'Terms', html_file[:-5])
   # save the dataframe to a csv file
   df.to_csv(f"{CSV_FILEPATH}{html_file[:-5]}.csv", index=False, encoding='utf-8')
   print(f"Saved {html_file} to csv file")
   