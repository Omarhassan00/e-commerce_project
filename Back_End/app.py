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


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', 'z::xvs9N`[j):ld.bRx83N)[potFg&yANj.((Nb>bL<CC<SH)/_}2Fi+gV":28i')

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'


# app.register_blueprint()
app.register_blueprint(routes.main.bp2)
app.register_blueprint(routes.auth.bp)
app.register_blueprint(routes.admin.bp)


@login_manager.user_loader
def load_user(user_id):
    cr.execute('select * from `users` where id = %s', (user_id,))
    data = cr.fetchone()
    if data:
        return user.User(data[0], data[4], data[1], data[11])
    return None

# Run server code (development mode)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
