import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE views
          (id INTEGER PRIMARY KEY ASC, 
           user_id VARCHAR(250) NOT NULL,
           views INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE likes
          (id INTEGER PRIMARY KEY ASC, 
           user_id VARCHAR(250) NOT NULL,
           likes INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
