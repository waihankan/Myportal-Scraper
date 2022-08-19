import sqlite3

connection = sqlite3.connect('./database/classes.db')
cursor = connection.execute('''
SELECT * from schedule
WHERE Subj = 'ACCT' AND Crse = 'D001A'
''')
outputs = cursor.fetchall()

# output is a list of tuples with one element each (e.g. [('CS',), ('MATH',)]) so we need to convert it to a list of strings (e.g. ['CS', 'MATH']) using list comprehension
# outputs = [i[0] for i in output]
 
for output in outputs:
   print(output)