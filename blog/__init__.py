from flask import Flask
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_breadcrumbs import Breadcrumbs
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f00cd52a167a5cc47802d7b9c216be2f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../budget.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'please login first'
bootstrap = Bootstrap(app)
Breadcrumbs(app=app)

from blog import routes
