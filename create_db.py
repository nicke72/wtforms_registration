import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE macs (mac_address TEXT, date_expired TEXT, email TEXT, user_id TEXT)')
print ("Table created successfully")
conn.close()