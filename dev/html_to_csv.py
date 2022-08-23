'''
   To parse the data from html file into csv using pandas library.
'''

import pandas as pd
from os import listdir
from os.path import isfile, join


# get a list of all the html files in the html_archive folder
html_files = [f for f in listdir("./database/html_archive") 
               if isfile(join("./database/html_archive", f))]
html_files.sort()

for html_file in html_files:
   # read the html file into a pandas dataframe
   df = pd.read_html(f"./database/html_archive/{html_file}")
   # get the first 17 columns of the dataframe (useful data)
   N = 17
   df  = df[5].iloc[: , :N]
   # overwrite the headers for sql columns
   df.columns = ["Status", "Crn", "Coreq", "Subj", "Crse",
               "Sec", "Cmp", "Cred", "Title", "Days", "Time",
               "Act", "Rem", "Wlrem", "Instructor", "Date", 
               "Location"] 
   # clean up instructor names and remove the (P) from the end
   df["Instructor"] = df["Instructor"].str.replace(r' \(P\)', '', regex=True)
   # filter out the rows that are not schedules of classes
   df = df[df['Date'].str.contains('/\d\d-', regex=True)]
   df.insert(0, 'Terms', html_file[:-5])
   # save the dataframe to a csv file
   df.to_csv(f"./database/csv_archive/{html_file[:-5]}.csv", index=False, encoding='utf-8')
   print(f"Saved {html_file} to csv file")
   