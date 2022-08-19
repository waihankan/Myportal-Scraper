import pandas as pd
import sqlite3 as sql

conn = sql.connect("./database/classes.db")
cur = conn.cursor()

df = pd.read_csv("./dev_test/test.csv")

df.to_sql("schedule", conn, if_exists='replace', index=False) # writes to file
conn.close()