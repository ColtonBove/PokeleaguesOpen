from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    image_link = db.Column(db.String(64), index=True)
    groups = relationship('Group', secondary ='link', back_populates="users")
    comments = db.relationship('Comment', back_populates='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_default_image(self):
    	self.image_link = "pokeball.png"

    def get_posts(self):
        return Post.query.join(Link, (Link.group_id == Post.group_id)).filter(Link.user_id == self.id).order_by(Post.timestamp.desc()).all()

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    private = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64), index=True, unique=True)
    leader = db.Column(db.String(64), db.ForeignKey('user.username'))
    image = db.Column(db.String(64), index=True, default="squad.jpg")
    kind = db.Column(db.String(64), index=True) #draft league, tournament
    platform = db.Column(db.String(32), index=True) #showdown or wifi or other
    dex = db.Column(db.String(64), index=True) #galar, kanto, etc
    users = relationship('User', secondary ='link', back_populates="groups")
    posts = db.relationship('Post', back_populates='group', lazy=True)
    chats = db.relationship('Chat', back_populates='group', lazy=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_chat(self):
        if len(self.chats) > 30:
            self.chats.pop(0)

#this class links the users and groups to form the many to many relationship
class Link(db.Model):
    id = db.Column(db.String(32), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    status = db.Column(db.Integer, default=2) #owner 0, member = 1, spectator = 2
    record = db.Column(db.String(4), default="0-0")

    group = db.relationship(Group, backref="link")
    user = db.relationship(User, backref="link")

    pokemon = db.relationship('Pokemon', backref='link', lazy=True)

    def set_id(self):
        self.id = (str(self.user_id) + '|' + str(self.group_id))

    def set_pokemon(self):
        for i in range(6):
            pikachu = Pokemon(link_id=self.id, name="pikachu")
            self.pokemon.append(pikachu) 

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.String(32), db.ForeignKey('link.id'))
    name = db.Column(db.String(32), index=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = relationship("Group", back_populates="posts")
    title = db.Column(db.String(32), index=True)
    body = db.Column(db.String(180), index=True)
    link = db.Column(db.String(64), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='comment', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User", back_populates="comments")
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    body = db.Column(db.String(64), index=True)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = relationship("Group", back_populates="chats")
    username = db.Column(db.String(32), index=True)
    message = db.Column(db.String(64), index=True)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))