import sqlite3
connection = sqlite3.connect('./database/classes.db')
cur = connection.cursor()

# cur.execute("""
# CREATE TABLE IF NOT EXISTS ACCT (
#    Status TEXT,
#    CRN INTEGER,
#    Coreq INTEGER,
#    Subj TEXT,
#    Crse TEXT,
#    SEC TEXT,
#    Cmp TEXT,
#    Cred REAL,
#    Title TEXT,
#    Days TEXT,
#    Time TEXT,
#    Act INTEGER,
#    Rem INTEGER,
#    WLRem INTEGER,
#    Instructor TEXT,
#    Date TEXT,
#    Location TEXT)
# """)


# cur.execute("""
# INSERT INTO ACCT
# SELECT * FROM schedule
# WHERE Subj = 'ACCT'
# """)

cur.execute("""
   SELECT * FROM ACCT
   ORDER BY Rem ASC
""")
results = cur.fetchall()
for output in results:
   print(output)


connection.commit()
connection.close()