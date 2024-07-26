# pip install flask flask_bcrypt mysql.connector os flask_login
import routes
from database import cr 
from models import user
from flask import Flask
from flask_bcrypt import Bcrypt
import os
from flask_login import  LoginManager
import routes.auth
import routes.main
import routes.admin

# start flask app
app = Flask(__name__)

# THE SECRET KEY
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', 'z::xvs9N`[j):ld.bRx83N)[potFg&yANj.((Nb>bL<CC<SH)/_}2Fi+gV":28i')

# app confegration for each library
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'


# app blueprint routs file
app.register_blueprint(routes.main.bp2)
app.register_blueprint(routes.auth.bp)
app.register_blueprint(routes.admin.bp)

# confegration login_manager with user id
@login_manager.user_loader
def load_user(user_id):
    cr.execute('select * from `users` where id = %s', (user_id,))
    data = cr.fetchone()
    if data:
        return user.User(data[0], data[4], data[1], data[11])
    return None

# Run server code
if __name__ == '__main__':
    app.run(debug=False, port=5000)
