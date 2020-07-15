from flask import Flask
from flask_socketio import SocketIO
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import json
import eventlet

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
socketio = SocketIO(app)

from app import routes, users
from app.users import User, Group, Link, Pokemon

#for testing
#db.drop_all()
#db.create_all()

'''user = User(username="user")
new_user = User(username="Colton")
group = Group(name="Pokemon Fans", leader="Colton", kind="Tournament", platform="Wifi Battles", dex="Kanto")
othergroup = Group(name="Just for fun", leader="user", kind="Draft League", platform="Pokemon Showdown", dex="Sinnoh-National")
user.groups.append(group)
user.groups.append(othergroup)
new_user.groups.append(group)
user.set_password("pass")
user.set_default_image()
new_user.set_password("pass")
new_user.set_default_image()
db.session.add(group)
db.session.add(othergroup)
db.session.add(new_user)
db.session.add(user)
db.session.commit()

link = Link.query.filter_by(user_id=user.id, group_id=group.id).first()
link.status = 2
otherlink = Link.query.filter_by(user_id=user.id, group_id=othergroup.id).first()
otherlink.status = 0
mylink = Link.query.filter_by(user_id=new_user.id, group_id=group.id).first()
mylink.status = 0
mylink.set_id()
mylink.set_pokemon()
otherlink.set_id()
otherlink.set_pokemon()
db.session.commit()'''