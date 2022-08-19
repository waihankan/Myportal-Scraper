import sqlite3
connection = sqlite3.connect('./database/classes.db')
# cursor = connection.execute('SELECT * FROM schedule')
# names = list(map(lambda x: x[0], cursor.description))
# print(names)
cur = connection.cursor()
cur.execute("""
SELECT * FROM schedule
WHERE Subj = 'ACCT' AND Crse = 'D001A'
ORDER BY Rem ASC
""")
output_list = cur.fetchall()
for output in output_list: 
   print(output)






connection.close()