import sqlite3
import mysql.connector

conn = sqlite3.connect('readings.sqlite')

db_conn = mysql.connector.connect(host="taylor-lab6.eastus.cloudapp.azure.com", user="user", password="password", database="events")

db_cursor = db_conn.cursor()
c = conn.cursor()
db_cursor.execute('''
          CREATE TABLE views
          (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
           user_id VARCHAR(250) NOT NULL,
           views INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

db_cursor.execute('''
          CREATE TABLE likes
          (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
           user_id VARCHAR(250) NOT NULL,
           likes INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

db_conn.commit()
db_conn.close()
