from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

#Advert Column
#Advert Column Image One
class AdvertoneForm(FlaskForm):
	title = StringField("Title :", validators=[DataRequired()])
	file = FileField("Upload Image : ", validators=[DataRequired()])
	percentage = StringField("Percentage Off :", validators=[DataRequired()])
	deal = StringField("Deal For the Day :", validators=[DataRequired()])
	alt = StringField("Alt Text :")
	slug = StringField("Summary :", validators=[DataRequired()])
	link = StringField("Link :", validators=[DataRequired()])
	content = CKEditorField('Content :', validators=[DataRequired()])
	current_user = StringField("Specify User :", validators=[DataRequired()])
	submit = SubmitField("Submit")

#Advert Column Image Two
class AdverttwoForm(FlaskForm):
	title = StringField("Title :", validators=[DataRequired()])
	file = FileField("Upload Image : ", validators=[DataRequired()])
	percentage = StringField("Percentage Off :", validators=[DataRequired()])
	alt = StringField("Alt Text :")
	slug = StringField("Summary :", validators=[DataRequired()])
	link = StringField("Link :", validators=[DataRequired()])
	content = CKEditorField('Content :', validators=[DataRequired()])
	submit = SubmitField("Submit")

#Advert Column Image Three
class AdvertthreeForm(FlaskForm):
	title = StringField("Title :", validators=[DataRequired()])
	file = FileField("Upload Image : ", validators=[DataRequired()])
	percentage = StringField("Percentage Off :", validators=[DataRequired()])
	alt = StringField("Alt Text :")
	slug = StringField("Summary :", validators=[DataRequired()])
	link = StringField("Link :", validators=[DataRequired()])
	content = CKEditorField('Content :', validators=[DataRequired()])
	submit = SubmitField("Submit")

#Advert Column Image Four
class AdvertfourForm(FlaskForm):
	title = StringField("Title :", validators=[DataRequired()])
	file = FileField("Upload Image : ", validators=[DataRequired()])
	percentage = StringField("Percentage Off :", validators=[DataRequired()])
	alt = StringField("Alt Text :")
	slug = StringField("Summary :", validators=[DataRequired()])
	link = StringField("Link :", validators=[DataRequired()])
	content = CKEditorField('Content :', validators=[DataRequired()])
	submit = SubmitField("Submit")








#Create A Post Form
class  OrganiseForm(FlaskForm):
	title = StringField("Title :", validators=[DataRequired()])
	file = FileField("Upload Image : ", validators=[DataRequired()])
	alt = StringField("Alt Text :")
	slug = StringField("Summary :", validators=[DataRequired()])
	content = CKEditorField('Content :', validators=[DataRequired()])
	submit = SubmitField("Submit")

#Community Form
class CommunityForm(FlaskForm):
	title = StringField("Topic :", validators=[DataRequired()])
	slug = StringField("Add a Tag :", validators=[DataRequired()])
	content = CKEditorField('Community :', validators=[DataRequired()])
	submit = SubmitField("Submit")

#Create a Search Form
class SearchForm(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])
	submit = SubmitField("Submit")

#create login form
class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Log In")

#Create A Health Form
class  IdeaForm(FlaskForm):
	title = StringField("Title :", validators=[DataRequired()])
	file = FileField("Upload Image : ", validators=[DataRequired()])
	alt = StringField("Alt Text :")
	slug = StringField("Summary :", validators=[DataRequired()])
	content = CKEditorField('Content :', validators=[DataRequired()])
	submit = SubmitField("Submit")

#Create A Health Form
class  HealthForm(FlaskForm):
	title = StringField("Title :", validators=[DataRequired()])
	file = FileField("Upload Image : ", validators=[DataRequired()])
	alt = StringField("Alt Text :")
	slug = StringField("Summary :", validators=[DataRequired()])
	content = CKEditorField('Content :', validators=[DataRequired()])
	submit = SubmitField("Submit")

#Create A Green Form
class  GreenForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	file = FileField("Upload Image : ", validators=[DataRequired()])
	content = CKEditorField('Content', validators=[DataRequired()])
	author = StringField("Author")
	slug = StringField("Summary", validators=[DataRequired()])
	submit = SubmitField("Submit")

#Create A Finance Form
class  FinanceForm(FlaskForm):
	title = StringField("Title :", validators=[DataRequired()])
	file = FileField("Upload Image : ", validators=[DataRequired()])
	alt = StringField("Alt Text :")
	slug = StringField("Summary :", validators=[DataRequired()])
	content = CKEditorField('Content :', validators=[DataRequired()])
	submit = SubmitField("Submit")

#Create A Essay Form
class  EssayForm(FlaskForm):
	title = StringField("Title :", validators=[DataRequired()])
	file = FileField("Upload Image : ", validators=[DataRequired()])
	alt = StringField("Alt Text :")
	slug = StringField("Summary :", validators=[DataRequired()])
	content = CKEditorField('Content :', validators=[DataRequired()])
	submit = SubmitField("Submit")

#Create A Design Form
class  DesignForm(FlaskForm):
	title = StringField("Title :", validators=[DataRequired()])
	file = FileField("Upload Image : ", validators=[DataRequired()])
	alt = StringField("Alt Text :")
	slug = StringField("Summary :", validators=[DataRequired()])
	content = CKEditorField('Content :', validators=[DataRequired()])
	submit = SubmitField("Submit")

#Create A Business Form
class  BusinessForm(FlaskForm):
	title = StringField("Title :", validators=[DataRequired()])
	file = FileField("Upload Image : ", validators=[DataRequired()])
	alt = StringField("Alt Text :")
	slug = StringField("Summary :", validators=[DataRequired()])
	content = CKEditorField('Content :', validators=[DataRequired()])
	submit = SubmitField("Submit")

#Create A Post Form
class  PostForm(FlaskForm):
	title = StringField("Title :", validators=[DataRequired()])
	file = FileField("Upload Image : ", validators=[DataRequired()])
	alt = StringField("Alt Text :")
	slug = StringField("Summary :", validators=[DataRequired()])
	content = CKEditorField('Content :', validators=[DataRequired()])
	submit = SubmitField("Submit")

#create a userform class
class UserForm(FlaskForm):
	name = StringField("Name :", validators=[DataRequired()])
	username = StringField("Username : ('Be Advice Use Your Email As Your Username')", validators=[DataRequired()])
	email = StringField("Email Address :", validators=[DataRequired()])
	about_author = TextAreaField("About Author : ")
	password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
	password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
	profile_pic = FileField("Profile Pic : ")
	submit = SubmitField("Submit")

#create a Password class
class PasswordForm(FlaskForm):
	email = StringField("what's your Email", validators=[DataRequired()])
	password_hash = PasswordField("what's your Password", validators=[DataRequired()])
	submit = SubmitField("Submit")


#create a form class
class NamerForm(FlaskForm):
	name = StringField("what's your name", validators=[DataRequired()])
	submit = SubmitField("Submit")

#FILTERS
#safe: This removes html tags from the screen display and prevents it from being displayed on the screen

#capitalize
#upper
#lower
#title: This will capitalize every letter in every word

#trim: this will remove spaces at the end

#striptags: This removes the html tags ad text totally

