import pandas as pd
from os import listdir
from os.path import isfile, join



HTML_FILEPATH = "./database/transfer_html_archive/"
CSV_FILEPATH = "./database/transfer_csv_archive/"
SQL_COL_LIST = [
                "Year", "Semester", "Instructor", "Subj",
                "Crse", "A", "B", "C", "D","F", "W"
                ] 

html_files = [f for f in listdir(HTML_FILEPATH)
                if isfile(join(HTML_FILEPATH, f))]
html_files.sort()
print(html_files)

for html_file in html_files:
    df = pd.read_html(f"{HTML_FILEPATH}{html_file}")
    df = df[0]
    df = df.drop("COURSE ID", axis=1)
    df = df.dropna()
    df = df.astype({"F": int, "W": int})
    df.columns = SQL_COL_LIST
    df.to_csv(f"{CSV_FILEPATH}{html_file[:-5]}.csv", index=False, encoding='utf-8')
    print(f"Saved {html_file} to csv file")
