# pip install mysql.connector
import mysql.connector

# pip install flask
from flask import Flask, request, redirect

# Flask Start
app = Flask(__name__)

# Link DataBase
db = mysql.connector.connect(
    host='localhost',
    database='lvander_website',
    user='root',
    passwd='',
)
cr = db.cursor()

# Home Page
# http://127.0.0.1:5000/
@app.route('/')
def index():
    return "Hello from home page!"


# Log-in Page
# http://127.0.0.1:5000/login?username=omar&password=123
@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    cr.execute(
        f'select * from `users` where username = "{username}" and password = "{password}"')
    data = cr.fetchone()

    if data != None:
        return redirect('/')

    else:
        return (f'sorry, {username} you don\'t have access\n')


# Registration Page
#  http://127.0.0.1:5000/registration?username=omar&password=123&email=omarhassan&first_name=oar&last_name=hassan&country=egypt&city=suez&adress_line1=sgdf&adress_line2=sgdffdd&gender=male&date_birth=18-5-1997&phone=01090220650
@app.route('/registration')
def registration():

    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    country = request.args.get('country')
    city = request.args.get('city')
    adress_line1 = request.args.get('adress_line1')
    adress_line2 = request.args.get('adress_line2')
    gender = request.args.get('gender')
    date_birth = request.args.get('date_birth')
    phone = request.args.get('phone')

    cr.execute(f'INSERT INTO `users` (username,password,email,first_name,last_name,country,city,adress_line1,adress_line2,gender,date_birth,phone) VALUES ("{username}","{password}","{email}","{first_name}","{last_name}","{country}","{city}","{adress_line1}","{adress_line2}","{gender}","{date_birth}",{phone})')
    db.commit()
    return f'user {username} added'

# Run server code (development mode)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
