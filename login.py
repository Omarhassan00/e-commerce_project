import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    database='lavander_project',
    user='root',
    passwd='',
)

cr = db.cursor()

username = input('username : ').strip().lower()
password = input('password : ').strip()
cr.execute(
    f'select * from users where username = "{username}" and password = "{password}"')
data = cr.fetchone()

if data != None:
    print(f'welcome {username}')

else:
    print(f'sorry, {username} you don\'t have access\n')