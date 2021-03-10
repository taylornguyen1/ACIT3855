import mysql.connector
db_conn = mysql.connector.connect(host="taylor-lab6.eastus.cloudapp.azure.com", user="user", password="password", database="events")
db_cursor = db_conn.cursor()
db_cursor.execute('''
 DROP TABLE views, likes
''')
db_conn.commit()
db_conn.close()