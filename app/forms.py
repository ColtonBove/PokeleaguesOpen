from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Required, DataRequired, ValidationError, Email, EqualTo, Length
from app.users import User

class LoginForm(FlaskForm):
    username = StringField(render_kw={"placeholder": "Username"}, validators=[DataRequired()])
    password = PasswordField(render_kw={"placeholder": "Password"}, validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField(render_kw={"placeholder": "Username"}, validators=[DataRequired()])
    email = StringField(render_kw={"placeholder": "Email"}, validators=[DataRequired(), Email()])
    password = PasswordField(render_kw={"placeholder": "Password"}, validators=[DataRequired()])
    password2 = PasswordField(render_kw={"placeholder": "Repeat Password"}, validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
    	user = User.query.filter_by(email=email.data).first()
    	if user is not None:
    		raise ValidationError('Sorry this email is already in use.')

class ReportForm(FlaskForm):
    title = StringField(render_kw={"placeholder": "I'm inquiring about..."}, validators=[DataRequired()])
    report = TextAreaField(render_kw={"placeholder": "My message is..."}, validators=[DataRequired()])
    submit = SubmitField('Send Report')

class GroupForm(FlaskForm):
    title = StringField('Group Name:', render_kw={"placeholder": "My Group"}, validators=[DataRequired()])
    '''abbreviation = StringField('Abbreviation:', render_kw={"placeholder": "MG"}, validators=
        [Length(min=1, max=4, message=('Abbreviation must be between 1 and 4 characters'))])'''
    group_type = StringField('Group Type:', render_kw={"placeholder": "Ex) Tournament"}, validators=[DataRequired()])
    dex = StringField('Pokedex:', render_kw={"placeholder": "Ex) Galar-National"}, validators=[DataRequired()])
    method = SelectField('Method:', choices=[('Wifi Battles','Wifi Battles'), ('Pokemon Showdown', 'Pokemon Showdown'), ('Other', 'Other')], validators=[DataRequired()])
    submit = SubmitField('Create Group')

class PostForm(FlaskForm):
    title = StringField(render_kw={"placeholder": "Title"}, validators=[DataRequired()])
    body = TextAreaField(render_kw={"placeholder": "Description of post, battle replay links, etc... (250 max)"}, validators=
        [Length(min=1, max=250, message=('Sorry, your post must be between 1-250 characters'))])
    link = StringField(render_kw={"placeholder": "Optional Battle Link"})
    submit = SubmitField('Create Post')
