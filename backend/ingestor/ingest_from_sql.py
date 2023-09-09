import sqlite3
# /Users/solivagant_ss/Desktop/data-source/master-reference.db
conn = sqlite3.connect('/Users/solivagant_ss/Desktop/data-source/master-reference.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for table in tables:
    print(table[0])


cursor.execute("SELECT * FROM bond_reference")
records = cursor.fetchall()
for record in records:  
    print(record)
conn.close()


