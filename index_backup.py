from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

#create a flask instance
app = Flask(__name__)

#add database
#Old Sqlite DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#Another Sqlite DB as Backup
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///backup_database.db'



#New Sqlite
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@Ebire199806@localhost/database_users'

#secret key!
app.config['SECRET_KEY'] = "my super secret key"

#initializing the database
db = SQLAlchemy(app)
migrate = Migrate(app,db)


#Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

#create login form
class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Submit")


#create login page
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user:
			
			#cHECK THE HASH
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				flash("Login Successful!")
				return redirect(url_for('dashboard'))
			else:
				flash("Wrong Password Please... Try Again!")
		else:
			flash(" That User Doesn't Exist... Try Again!")

	return render_template('login.html', form=form)


#Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("You Have Successfully Logged Out! ")
	return redirect(url_for('login'))

#create dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	return render_template('dashboard.html')






#Create A Blog Post
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text)
	author = db.Column(db.String(255))
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))

#Create A Post Form
class  PostForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	content = StringField("Content", validators=[DataRequired()], widget=TextArea())
	author = StringField("Author", validators=[DataRequired()])
	slug = StringField("Summary", validators=[DataRequired()])
	submit = SubmitField("Submit")


@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
	post_to_delete = Posts.query.get_or_404(id)

	try:
		db.session.delete(post_to_delete)
		db.session.commit()

		#return message
		flash ("Blog Post Was Deleted Successfully!")
		

		#Grab all the post from the DataBase
		posts = Posts.query.order_by(Posts.date_posted)
		return render_template("posts.html", posts=posts)

	except:
		#return error message
		flash ("Whoops!!! There was a Problem Deleting Post Try Again...")

		#Grab all the post from the DataBase
		posts = Posts.query.order_by(Posts.date_posted)
		return render_template("posts.html", posts=posts)




@app.route('/posts')
def posts():
	#Grab all the post from the DataBase
	posts = Posts.query.order_by(Posts.date_posted)
	return render_template("posts.html", posts=posts)


@app.route('/posts/<int:id>')
def post(id):
	post = Posts.query.get_or_404(id)
	return render_template("post.html", post=post)


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
	post = Posts.query.get_or_404(id)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.author = form.author.data
		post.slug = form.slug.data
		post.content = form.content.data

		#Update to DataBase
		db.session.add(post)
		db.session.commit()

		flash("Post Successfully Updated")
		return redirect(url_for('post', id=post.id))

	form.title.data = post.title
	form.author.data = post.author
	form.slug.data = post.slug
	form.content.data = post.content

	return render_template('edit_post.html', form=form)



#Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
	form = PostForm()

	if form.validate_on_submit():
		post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
		#clear the form
		form.title.data = ''
		form.content.data = ''
		form.author.data = ''
		form.slug.data = ''

		#add post data to database
		db.session.add(post)
		db.session.commit()

		#return a message
		flash("Blog Post Submitted Successfully !")


	#redirect to the webpage
	return render_template("add_post.html", form=form)





#Json Thing
@app.route('/date')
def get_current_date():
	return {"Date": date.today()}


#create a model
class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(200), nullable=False, unique=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)
	
	#Do Some Password Stuff
	password_hash = db.Column(db.String(128))

	@property
	def password(self):
		raise AttributeError(' Password Not A Readable Attribute !!! ')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	
	#create string
	def __repr__(self):
		return '<Name %r>' % self.name

#Delete DataBase
@app .route('/delete/<int:id>')
def delete(id):
	user_to_delete = Users.query.get_or_404(id)
	name = None
	form = UserForm()

	try:
		db.session.delete(user_to_delete)
		db.session.commit()
		flash("User Deleted Successfully!!")

		our_users = Users.query.order_by(Users.date_added)
		return render_template("add_user.html",
			form=form,
			name=name,
			our_users=our_users)

	except:
		flash("Whoops! There was a problem deleting user, Try Again... ")
		return render_template("add_user.html",
			form=form,
			name=name,
			our_users=our_users)


#create a userform class
class UserForm(FlaskForm):
	name = StringField("Name :", validators=[DataRequired()])
	username = StringField("Username :", validators=[DataRequired()])
	email = StringField("Email Address :", validators=[DataRequired()])
	
	password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
	password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
	submit = SubmitField("Submit")


#Create New DataBase Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.username = request.form['username']

		try:
			db.session.commit()
			flash("User Updated Successfully !")
			return render_template("update.html",
				form=form,
				name_to_update = name_to_update)
		except:
			flash("Error! Looks Like There Was a Problem... Try Again!")
			return render_template("update.html",
				form=form,
				name_to_update = name_to_update)

	else:
		return render_template("update.html",
				form=form,
				name_to_update = name_to_update, 
				id = id )



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



@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			#Hash Password
			hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
			user = Users(name=form.name.data, username=form.username.data, email=form.email.data, password_hash=hashed_pw)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data = ''
		form.username.data = ''
		form.email.data = ''
		form.password_hash = ''

		flash("User Added Successfully")

	our_users = Users.query.order_by(Users.date_added)

	return render_template("add_user.html",
		form=form,
		name=name,
		our_users=our_users)



#create a route decorator
@app.route("/")

#def index():
	#return "<h1>Hello World!</h1>"


def index():
	first_name = "John"
	stuff = "This is <strong>Bold</strong> Text"

	favourite_pizza = ["Pepperoni", "Cheese", "Mushroom", 41]
	return render_template("index.html", 
		first_name=first_name,
		stuff=stuff,
		favourite_pizza=favourite_pizza)


#localhost:5000/user/john
@app.route("/user")
@login_required
def user():
	return render_template("user.html")

#create custom error page

#invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500

#create name page
@app.route('/name', methods=['GET', 'POST'])
def name():
	name = None
	form = NamerForm()

	#validate form
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
		flash("Form Submitted Successful")

	return render_template("name.html",
		name = name,
		form = form)


#create password Testing page
@app.route('/test_pw', methods=['GET', 'POST'])
@login_required
def test_pw():
	email = None
	password = None
	pw_to_check = None
	passed = None
	form = PasswordForm()

	#validate form
	if form.validate_on_submit():
		email = form.email.data
		password = form.password_hash.data
		form.email.data = ''
		form.password_hash.data = ""

		#Look up User by Email Address
		pw_to_check = Users.query.filter_by(email=email).first()

		#check hash password
		passed = check_password_hash(pw_to_check.password_hash, password)

		#flash("Form Submitted Successful")

	return render_template("test_pw.html",
		email = email,
		password = password,
		pw_to_check = pw_to_check,
		passed = passed,
		form = form)
