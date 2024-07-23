import mysql.connector


db_config = {
'host': 'localhost',
'database': 'lavander_website',
'user': 'root',
'passwd': '',
}
db = mysql.connector.connect(**db_config)
cr = db.cursor()

