from app import app
from app import db
from app import socketio
from flask import request, render_template, flash, redirect, url_for, session
from flask_login import current_user, login_user, logout_user, login_required
from flask_socketio import SocketIO
from sqlalchemy import desc
from app.users import User, Group, Link, Pokemon, Post, Comment, Chat
from app.forms import LoginForm, RegisterForm, ReportForm, GroupForm, PostForm

import yagmail #for sending emails
import urllib.request as urllib2

#home page once logged in
@app.route('/')
@app.route('/home')
def home():
	if not current_user.is_authenticated:
		return redirect(url_for('signin'))
	else:
		posts = current_user.get_posts()
		return render_template('home.html', posts=posts)

#takes care of the sign in form on the sign in page
@app.route('/signin', methods=['GET', 'POST'])
def signin():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('signin'))
        else:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('home'))
    return render_template('signin.html', form=form)

#takes care of the register form on the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.set_default_image()
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('signin'))
    return render_template('register.html', title='Register', form=form)

#takes user to their profile
@app.route('/profile')
@login_required
def profile():
    links = Link.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', links=links)#remember to return group here when the time comes

#takes user to avatar selection screen
@app.route('/profile/avatar')
@login_required
def avatar():
    return render_template('avatar.html')

#javascript helper to change the profile image
@app.route('/change_profile', methods=["POST"])
def change_profile():
    user = User.query.filter_by(id=current_user.id)
    link = request.form["check"]
    current_user.image_link = link
    db.session.commit()
    return "OK!"

#takes user to their profile
@app.route('/groups')
@login_required
def groups():
	return render_template('groups.html')

@app.route('/groups/create', methods=['GET', 'POST'])
@login_required
def create():
    form = GroupForm()
    if form.validate_on_submit():
        group = Group(name=form.title.data, leader=current_user.username,
         kind=form.group_type.data, platform=form.method.data, dex=form.dex.data)
        current_user.groups.append(group)
        db.session.add(group)
        db.session.commit()
        link = Link.query.filter_by(user_id=current_user.id, group_id=group.id).first()
        link.status = 0
        link.set_id()
        link.set_pokemon()
        db.session.commit()
        return redirect(url_for('groupname', name=form.title.data))#make this the group page later
    return render_template('create.html', form=form)

@app.route('/groups/join')
@login_required
def join():
    groups = Group.query.order_by(desc(Group.timestamp)).all()
    return render_template('join.html', groups=groups)

@app.route('/groups/join', methods=['POST'])
@login_required
def join_search():
    search = request.form['search']
    groups = Group.query.filter(Group.name.contains(search))
    return render_template('join.html', groups=groups)

@app.route('/groups/<name>', methods=['GET', 'POST'])
@app.route('/groups/<name>/<mode>', methods=['GET', 'POST'])
@login_required
def groupname(name, mode=1):
    form = PostForm()
    submit = False
    group = Group.query.filter_by(name=name).first()
    if form.validate_on_submit():
    	post = Post(title=form.title.data, body=form.body.data + '\n-' + current_user.username, link=form.link.data )
    	group.posts.append(post)
    	db.session.commit()
    	submit = True

    #set all of the group variables for the html
    link = Link.query.filter_by(user_id=current_user.id, group_id=group.id).first()
    members = len(group.users)
    links = Link.query.filter_by(group_id=group.id, status=1).all() #get all the members
    links.append(Link.query.filter_by(group_id=group.id, status=0).first()) #add the owner
    players = []
    for l in links:
        players.append(User.query.filter_by(id=l.user_id).first()) #add all the other members

    mode = int(mode)
    posts = Post.query.filter_by(group_id=group.id).order_by(desc(Post.timestamp)).all()

    if submit:
    	return redirect(url_for('groupname', name=group.name))
    	
    return render_template('groupname.html', group=group, user_link=link, links=links, members=members, players=players, mode=mode, form=form, posts=posts, chats=group.chats)

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
	socketio.emit('my response', json)

#takes user to group avatar selection screen
@app.route('/groups/<name>/avatar', methods=['GET', 'POST'])
@login_required
def avatar_group(name):
    return render_template('avatar_group.html', name=name)

#javascript helper to change the profile image
@app.route('/change_group', methods=["POST"])
def change_group():
    text = request.form["check"]
    text = text.split("|")
    link = text[0]
    name = text[1]
    group = Group.query.filter_by(name=name).first()
    group.image = link
    db.session.commit()
    return "OK!"

#javascript helper to change group to private or public
@app.route('/change_publicity', methods=["POST"])
def change_publicity():
    text = request.form["check"]
    text = text.split("|")
    group_name = text[0]
    password = text[1]
    group = Group.query.filter_by(name=group_name).first()
    group.private = not group.private
    if password != "":
    	group.set_password(password)
    db.session.commit()
    return "OK!"

#javascript helper to let a user become a member of a group
@app.route('/become_member', methods=["POST"])
def become_member():
    text = request.form["check"].split("|")
    group_name = text[0]
    password = text[1]
    group = Group.query.filter_by(name=group_name).first()
    if group.private == True:
    	if group.check_password(password):
    		current_user.groups.append(group)
    		link = Link.query.filter_by(user_id=current_user.id, group_id=group.id).first()
    		link.status = 1
    		link.set_id()
    		link.set_pokemon()
    		db.session.commit()
    	else:
    		return "Error: your password was incorrect"
    elif group.private == False:
    	current_user.groups.append(group)
    	link = Link.query.filter_by(user_id=current_user.id, group_id=group.id).first()
    	link.status = 1
    	link.set_id()
    	link.set_pokemon()
    	db.session.commit()

    return ""

@app.route('/remove_member', methods=['POST'])
def remove_member():
    text = request.form["check"].split("|")
    group_name = text[0]
    username = text[1]
    group = Group.query.filter_by(name=group_name).first()
    user = User.query.filter_by(username=username).first()
    group.users.remove(user)
    db.session.commit()
    return "OK!"

@app.route('/become_spectator', methods=["POST"])
def become_spectator():
    group_name = request.form["check"]
    group = Group.query.filter_by(name=group_name).first()
    current_user.groups.append(group)
    link = Link.query.filter_by(user_id=current_user.id, group_id=group.id).first()
    link.status = 2
    link.set_id()
    db.session.commit()
    return "OK!"

@app.route('/remove_spectate', methods=["POST"])
def remove_spectate():
    group_name = request.form["check"]
    group = Group.query.filter_by(name=group_name).first()
    current_user.groups.remove(group)
    db.session.commit()
    return "OK!"

@app.route('/remove_post', methods=["POST"])
def remove_post():
	post_id = request.form["check"]
	post = Post.query.filter_by(id=post_id).first()
	group = Group.query.filter_by(id=post.group_id).first()
	group.posts.remove(post)
	db.session.delete(post)
	db.session.commit()
	return "OK!"

@app.route('/remove_pokemon', methods=["POST"])
def remove_pokemon():
	text = request.form["check"]
	text = text.split("|")
	group_id = text[0]
	pokemon = text[1]
	link = Link.query.filter_by(user_id=current_user.id, group_id=group_id).first()
	poke = Pokemon.query.filter_by(link_id=link.id, name=pokemon).first()
	db.session.delete(poke)
	db.session.commit()
	return "OK!"

@app.route('/add_pokemon', methods=['POST'])
def add_pokemon():
	text = request.form["check"]
	text = text.split("|")
	group_id = text[0]
	pokemon = text[1]
	url = "http://smogon.com/dex/media/sprites/xy/" + pokemon + ".gif"
	message = ""
	req = urllib2.Request(url)

	try:
		resp = urllib2.urlopen(req)
		link = Link.query.filter_by(user_id=current_user.id, group_id=group_id).first()
		p = Pokemon(link_id=link.id, name=pokemon)
		link.pokemon.append(p)
		db.session.commit()
	except Exception as err:
		message = "Sorry, we couldn't find the pokemon: " + pokemon
	return message

@app.route("/add_comment", methods=['POST'])
def add_comment():
	text = request.form["check"].split("|")
	post_id = text[0]
	body = text[1]
	#query for the post the comment belongs to
	post = Post.query.filter_by(id=post_id).first()
	#make the comment and connect it to user and the post
	comment = Comment(body=body)
	current_user.comments.append(comment)
	post.comments.append(comment)
	db.session.commit()
	return "OK!"

@app.route("/add_chat", methods=['POST'])
def add_chat():
	text = request.form["check"].split("|")
	username = text[0]
	message = text[1]
	groupname = text[2]
	group = Group.query.filter_by(name=groupname).first()
	chat = Chat(username=username, message=message)
	group.chats.append(chat)
	group.check_chat()
	db.session.commit()
	return "OK!"

@app.route("/edit_record", methods=['POST'])
def edit_record():
	text = request.form['check'].split("|")
	#check if the values can be made into an int
	try:
		int(text[0])
		int(text[1])
	except ValueError:
		return "No"

	link = Link.query.filter_by(id=text[2] + "|" + text[3]).first()
	link.record = text[0] + "-" + text[1]
	db.session.commit()
	return "OK!"

#takes user to their profile
@app.route('/info')
@login_required
def info():
	return render_template('info.html')

'''takes user to their profile, sends email 
to pokeleagues account to process requests'''
@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    form = ReportForm()
    if form.validate_on_submit():
        try:
            yag = yagmail.SMTP(user='email goes here', password="password goes here")
            yag.send('pokeleagues.colton@gmail.com', form.title.data, (form.report.data + "\n -" + current_user.username))
            return redirect(url_for('home'))
        except:
            print("The email was not sent")
    return render_template('report.html', form=form)

#logs out the user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))