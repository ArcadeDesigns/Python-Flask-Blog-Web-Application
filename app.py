from flask import Flask, render_template, flash, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import LoginForm, PostForm, UserForm, PasswordForm, NamerForm, SearchForm, BusinessForm, DesignForm, FinanceForm, EssayForm, GreenForm, HealthForm, IdeaForm, CommunityForm, OrganiseForm, AdvertoneForm, AdverttwoForm, AdvertthreeForm, AdvertfourForm
from flask_ckeditor import CKEditor
from flask_ckeditor import upload_success, upload_fail
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
import urllib.request
import uuid as uuid
import os

#create a flask instance
app = Flask(__name__)

#add Ckeditor
ckeditor = CKEditor(app)

#add database
#Old Sqlite DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#Another Sqlite DB as Backup
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hog_furniture.db'

#add database
#Third Sqlite DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hog.db'



#New Sqlite
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@Ebire199806@localhost/database_users'

#secret key!
app.config['SECRET_KEY'] = "cairocoders-ednalan"

#saving images to the system files
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'jpeg', 'png', 'JPG', 'gif', 'PNG', 'JPEG']
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'

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

app.config['MAX_CONTENT_LENGTH'] = 16 * 900 * 900
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'JPG', 'gif', 'PNG', 'JPEG'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#admin page
@app.route("/admin")
@login_required
def admin():
	form = UserForm()
	our_users = Users.query.order_by(Users.date_added)
	posts = Posts.query.order_by(Posts.date_posted)
	businesses = Businesses.query.order_by(Businesses.date_posted)
	designs = Designs.query.order_by(Designs.date_posted)
	essays = Essays.query.order_by(Essays.date_posted)
	finances = Finances.query.order_by(Finances.date_posted)
	greens = Greens.query.order_by(Greens.date_posted)
	healths = Healths.query.order_by(Healths.date_posted)
	ideas = Ideas.query.order_by(Ideas.date_posted)
	advertones = Advertones.query.order_by(Advertones.date_posted)
	adverttwos = Adverttwos.query.order_by(Adverttwos.date_posted)
	advertthrees = Advertthrees.query.order_by(Advertthrees.date_posted)
	advertfours = Advertfours.query.order_by(Advertfours.date_posted)
	id = current_user.id
	if id == 1:
		return render_template("admin.html", 
			form=form,
			name=name,
			our_users=our_users,
			posts=posts,
			businesses=businesses,
			designs=designs,
			essays=essays,
			finances=finances,
			greens=greens,
			healths=healths,
			ideas=ideas,
			advertones=advertones,
			adverttwos=adverttwos,
			advertthrees=advertthrees,
			advertfours=advertfours)
	else:
		flash("Sorry you have to be an Admin to access this page")
		return redirect(url_for('dashboard'))

@app.route("/all-post")
@login_required
def all_post():
	posts = Posts.query.order_by(Posts.date_posted)
	businesses = Businesses.query.order_by(Businesses.date_posted)
	designs = Designs.query.order_by(Designs.date_posted)
	essays = Essays.query.order_by(Essays.date_posted)
	finances = Finances.query.order_by(Finances.date_posted)
	greens = Greens.query.order_by(Greens.date_posted)
	healths = Healths.query.order_by(Healths.date_posted)
	ideas = Ideas.query.order_by(Ideas.date_posted)
	id = current_user.id
	if id == 1:
		return render_template("all_post.html", 
			posts=posts,
			businesses=businesses,
			designs=designs,
			essays=essays,
			finances=finances,
			greens=greens,
			healths=healths,
			ideas=ideas)
	else:
		flash("Sorry you have to be an Logged in to access this page")
		return redirect(url_for('index'))

#Advertisement Section
@app.route('/add-advertcolumnone', methods=['GET', 'POST'])
@login_required
def add_advertcolumnone():
	form = AdvertoneForm()
			
	if form.validate_on_submit():

		poster = current_user.id
		advertone = Advertones(title=form.title.data, current_user=form.current_user.data, deal=form.deal.data, percentage=form.percentage.data, link=form.link.data, alt=form.alt.data, content=form.content.data, file=form.file.data, poster_id=poster, slug=form.slug.data)
		
		#check for file
		if request.files['file']:
			advertone.file = request.files['file']

			#Grab Image name
			filename = secure_filename(advertone.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			advertone.file = file_name

			try:
				db.session.add(advertone)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash("Hello Admin you have Successfully Published an Advert !")
				return render_template("admin.html",
					form=form,
					advertone=advertone)
			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("add_advertcolumnone.html",
					form=form,
					advertone=advertone)
		else:
			db.session.add(advertone)
			db.session.commit()
			flash("Hello Admin you have Successfully Published an Advert !")
			return render_template("admin.html",
				form=form,
				advertone=advertone)
		
		#clear the form
		form.title.data = ''
		form.content.data = ''
		form.slug.data = ''
		form.file.data = ''
		form.alt.data = ''
		form.percentage.data = ''
		form.deal.data = ''
		form.link.data = ''
		form.current_user.data = ''

		#add post data to database
		db.session.add(advertone)
		db.session.commit()

	return render_template("add_advertcolumnone.html",
			form=form,
			id = id or 1)

@app.route('/advertones/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_advertone(id):
	advertone = Advertones.query.get_or_404(id)
	form = AdvertoneForm()

	if form.validate_on_submit():
		advertone.title = form.title.data
		advertone.slug = form.slug.data
		advertone.content = form.content.data
		advertone.file = form.file.data
		advertone.alt = form.alt.data
		advertone.link = form.link.data
		advertone.percentage = form.percentage.data
		advertone.deal = form.deal.data
		advertone.current_user = form.current_user.data


		#check for file
		if request.files['file']:
			advertone.file = request.files['file']

			#Grab Image name
			filename = secure_filename(advertone.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename

			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			advertone.file = file_name

			try:
				db.session.add(advertone)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash(" You have Successfully Updated Your Post !")
				return render_template("advertones.html",
					form=form,
					advertone=advertone)

			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("edit_advertone.html",
					form=form,
					advertone=advertone)

		else:
			db.session.add(advertone)
			db.session.commit()
			flash(" You have Successfully Updated Your Post !")
			return render_template("advertones.html",
				form=form,
				advertone=advertone)

		#Update to DataBase
		db.session.add(advertone)
		db.session.commit()

		flash("Post Successfully Updated")
		return redirect(url_for('advertone', id=advertone.id))

	if current_user.id == advertone.poster_id or current_user.id == 1 :
		form.title.data = advertone.title
		form.slug.data = advertone.slug
		form.content.data = advertone.content
		form.file.data = advertone.file
		form.alt.data = advertone.alt
		form.percentage.data = advertone.percentage
		form.deal.data = advertone.deal
		form.current_user.data = advertone.current_user
		return render_template('edit_advertone.html', form=form)

	else:
		flash(" You need Authorization to access this Post")
		advertones = Advertones.query.order_by(Advertones.date_posted)
		return render_template("dashboard.html", advertones=advertones)

@app.route('/advertones/delete/<int:id>')
@login_required
def delete_advertone(id):
	advertone_to_delete = Advertones.query.get_or_404(id)
	id = current_user.id
	if id == advertone_to_delete.poster_id or id == 1:
		try:
			db.session.delete(advertone_to_delete)
			db.session.commit()

			#return message
			flash ("Blog Post Was Deleted Successfully!")
			

			#Grab all the post from the DataBase
			advertones = Advertones.query.order_by(Advertones.date_posted)
			return render_template("advertones.html", advertones=advertones)

		except:
			#return error message
			flash ("Whoops!!! There was a Problem Deleting Post Try Again...")

			#Grab all the post from the DataBase
			advertones = Advertones.query.order_by(Advertones.date_posted)
			return render_template("advertones.html", advertones=advertones)
	else:
		#return message
		flash("You are not authorized to Delete this Post!")

		#Grab all the post from the DataBase
		advertones = Advertones.query.order_by(Advertones.date_posted)
		return render_template("advertones.html", advertones=advertones)
	
@app.route('/advertones')
def advertones():
	#Grab all the post from the DataBase
	advertones = Advertones.query.order_by(Advertones.date_posted)
	return render_template("advertones.html", advertones=advertones)

@app.route('/advertones/<int:id>')
def advertone(id):
	advertone = Advertones.query.get_or_404(id)
	return render_template("advertone.html", advertone=advertone)

#Adverttwo Column
@app.route('/add-advertcolumntwo', methods=['GET', 'POST'])
@login_required
def add_advertcolumntwo():
	form = AdverttwoForm()
			
	if form.validate_on_submit():

		poster = current_user.id
		adverttwo = Adverttwos(title=form.title.data, percentage=form.percentage.data, link=form.link.data, alt=form.alt.data, content=form.content.data, file=form.file.data, poster_id=poster, slug=form.slug.data)
		
		#check for file
		if request.files['file']:
			adverttwo.file = request.files['file']

			#Grab Image name
			filename = secure_filename(adverttwo.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			adverttwo.file = file_name

			try:
				db.session.add(adverttwo)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash("Hello Admin you have Successfully Published an Advert !")
				return render_template("admin.html",
					form=form,
					adverttwo=adverttwo)
			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("add_advertcolumntwo.html",
					form=form,
					adverttwo=adverttwo)
		else:
			db.session.add(adverttwo)
			db.session.commit()
			flash("Hello Admin you have Successfully Published an Advert !")
			return render_template("admin.html",
				form=form,
				adverttwo=adverttwo)
		
		#clear the form
		form.title.data = ''
		form.content.data = ''
		form.slug.data = ''
		form.file.data = ''
		form.alt.data = ''
		form.percentage.data = ''
		form.link.data = ''

		#add post data to database
		db.session.add(adverttwo)
		db.session.commit()

	return render_template("add_advertcolumntwo.html",
			form=form,
			id = id or 1)

@app.route('/adverttwos/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_adverttwo(id):
	adverttwo = Adverttwos.query.get_or_404(id)
	form = AdverttwoForm()

	if form.validate_on_submit():
		adverttwo.title = form.title.data
		adverttwo.slug = form.slug.data
		adverttwo.content = form.content.data
		adverttwo.file = form.file.data
		adverttwo.alt = form.alt.data
		adverttwo.link = form.link.data
		adverttwo.percentage = form.percentage.data


		#check for file
		if request.files['file']:
			adverttwo.file = request.files['file']

			#Grab Image name
			filename = secure_filename(adverttwo.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename

			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			adverttwo.file = file_name

			try:
				db.session.add(adverttwo)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash(" You have Successfully Updated Your Post !")
				return render_template("adverttwos.html",
					form=form,
					adverttwo=adverttwo)

			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("edit_adverttwo.html",
					form=form,
					adverttwo=adverttwo)

		else:
			db.session.add(adverttwo)
			db.session.commit()
			flash(" You have Successfully Updated Your Post !")
			return render_template("adverttwos.html",
				form=form,
				adverttwo=adverttwo)

		#Update to DataBase
		db.session.add(adverttwo)
		db.session.commit()

		flash("Post Successfully Updated")
		return redirect(url_for('adverttwo', id=adverttwo.id))

	if current_user.id == adverttwo.poster_id or current_user.id == 1 :
		form.title.data = adverttwo.title
		form.slug.data = adverttwo.slug
		form.content.data = adverttwo.content
		form.file.data = adverttwo.file
		form.alt.data = adverttwo.alt
		form.percentage.data = adverttwo.percentage
		return render_template('edit_adverttwo.html', form=form)

	else:
		flash(" You need Authorization to access this Post")
		adverttwos = Adverttwos.query.order_by(Adverttwos.date_posted)
		return render_template("dashboard.html", adverttwos=adverttwos)

@app.route('/adverttwos/delete/<int:id>')
@login_required
def delete_adverttwo(id):
	adverttwo_to_delete = Adverttwos.query.get_or_404(id)
	id = current_user.id
	if id == adverttwo_to_delete.poster_id or id == 1:
		try:
			db.session.delete(adverttwo_to_delete)
			db.session.commit()

			#return message
			flash ("Blog Post Was Deleted Successfully!")
			

			#Grab all the post from the DataBase
			adverttwos = adverttwos.query.order_by(adverttwos.date_posted)
			return render_template("adverttwos.html", adverttwos=adverttwos)

		except:
			#return error message
			flash ("Whoops!!! There was a Problem Deleting Post Try Again...")

			#Grab all the post from the DataBase
			adverttwos = Adverttwos.query.order_by(Adverttwos.date_posted)
			return render_template("adverttwos.html", adverttwos=adverttwos)
	else:
		#return message
		flash("You are not authorized to Delete this Post!")

		#Grab all the post from the DataBase
		adverttwos = Adverttwos.query.order_by(Adverttwos.date_posted)
		return render_template("adverttwos.html", adverttwos=adverttwos)
	
@app.route('/adverttwos')
def adverttwos():
	#Grab all the post from the DataBase
	adverttwos = Adverttwos.query.order_by(Adverttwos.date_posted)
	return render_template("adverttwos.html", adverttwos=adverttwos)


@app.route('/adverttwos/<int:id>')
def adverttwo(id):
	adverttwo = Adverttwos.query.get_or_404(id)
	return render_template("adverttwo.html", adverttwo=adverttwo)

#Advertisement Advert Three Column  Section
@app.route('/add-advertcolumnthree', methods=['GET', 'POST'])
@login_required
def add_advertcolumnthree():
	form = AdvertthreeForm()
			
	if form.validate_on_submit():

		poster = current_user.id
		advertthree = Advertthrees(title=form.title.data, current_user=form.current_user.data, deal=form.deal.data, percentage=form.percentage.data, link=form.link.data, alt=form.alt.data, content=form.content.data, file=form.file.data, poster_id=poster, slug=form.slug.data)
		
		#check for file
		if request.files['file']:
			advertthree.file = request.files['file']

			#Grab Image name
			filename = secure_filename(advertthree.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			advertthree.file = file_name

			try:
				db.session.add(advertthree)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash("Hello Admin you have Successfully Published an Advert !")
				return render_template("admin.html",
					form=form,
					advertthree=advertthree)
			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("add_advertcolumnthree.html",
					form=form,
					advertthree=advertthree)
		else:
			db.session.add(advertthree)
			db.session.commit()
			flash("Hello Admin you have Successfully Published an Advert !")
			return render_template("admin.html",
				form=form,
				advertthree=advertthree)
		
		#clear the form
		form.title.data = ''
		form.content.data = ''
		form.slug.data = ''
		form.file.data = ''
		form.alt.data = ''
		form.percentage.data = ''
		form.deal.data = ''
		form.link.data = ''
		form.current_user.data = ''

		#add post data to database
		db.session.add(advertthree)
		db.session.commit()

	return render_template("add_advertcolumnthree.html",
			form=form,
			id = id or 1)

@app.route('/advertthrees/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_advertthree(id):
	advertthree = Advertthreesrtthrees.query.get_or_404(id)
	form = AdvertthreeForm()

	if form.validate_on_submit():
		advertthree.title = form.title.data
		advertthree.slug = form.slug.data
		advertthree.content = form.content.data
		advertthree.file = form.file.data
		advertthree.alt = form.alt.data
		advertthree.link = form.link.data
		advertthree.percentage = form.percentage.data
		advertthree.deal = form.deal.data
		advertthree.current_user = form.current_user.data


		#check for file
		if request.files['file']:
			advertthree.file = request.files['file']

			#Grab Image name
			filename = secure_filename(advertthree.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename

			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			advertthree.file = file_name

			try:
				db.session.add(advertthree)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash(" You have Successfully Updated Your Post !")
				return render_template("advertthrees.html",
					form=form,
					advertthree=advertthree)

			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("edit_advertthree.html",
					form=form,
					advertthree=advertthree)

		else:
			db.session.add(advertthree)
			db.session.commit()
			flash(" You have Successfully Updated Your Post !")
			return render_template("advertthrees.html",
				form=form,
				advertthree=advertthree)

		#Update to DataBase
		db.session.add(advertthree)
		db.session.commit()

		flash("Post Successfully Updated")
		return redirect(url_for('advertthree', id=advertthree.id))

	if current_user.id == advertthree.poster_id or current_user.id == 1 :
		form.title.data = advertthree.title
		form.slug.data = advertthree.slug
		form.content.data = advertthree.content
		form.file.data = advertthree.file
		form.alt.data = advertthree.alt
		form.percentage.data = advertthree.percentage
		form.deal.data = advertthree.deal
		form.current_user.data = advertthree.current_user
		return render_template('edit_advertthree.html', form=form)

	else:
		flash(" You need Authorization to access this Post")
		advertthrees = Advertthreess.query.order_by(Advertthrees.date_posted)
		return render_template("dashboard.html", advertthrees=advertthrees)

@app.route('/advertthrees/delete/<int:id>')
@login_required
def delete_advertthree(id):
	advertthree_to_delete = Advertthrees.query.get_or_404(id)
	id = current_user.id
	if id == advertthree_to_delete.poster_id or id == 1:
		try:
			db.session.delete(advertthree_to_delete)
			db.session.commit()

			#return message
			flash ("Blog Post Was Deleted Successfully!")
			

			#Grab all the post from the DataBase
			advertthrees = Advertthree.query.order_by(advertthrees.date_posted)
			return render_template("advertthrees.html", advertthrees=advertthrees)

		except:
			#return error message
			flash ("Whoops!!! There was a Problem Deleting Post Try Again...")

			#Grab all the post from the DataBase
			advertthrees = Advertthrees.query.order_by(Advertthrees.date_posted)
			return render_template("advertthrees.html", advertthrees=advertthrees)
	else:
		#return message
		flash("You are not authorized to Delete this Post!")

		#Grab all the post from the DataBase
		advertthrees = Advertthrees.query.order_by(advertthrees.date_posted)
		return render_template("advertthrees.html", advertthrees=advertthrees)
	

@app.route('/advertthrees')
def advertthrees():
	#Grab all the post from the DataBase
	advertthrees = Advertthrees.query.order_by(Advertthrees.date_posted)
	return render_template("Advertthrees.html", advertthrees=advertthrees)


@app.route('/advertthrees/<int:id>')
def advertthree(id):
	advertthree = Advertthrees.query.get_or_404(id)
	return render_template("advertthrees.html", advertthrees=advertthrees)



#Advertisement Section
@app.route('/add-advertcolumnfour', methods=['GET', 'POST'])
@login_required
def add_advertcolumnfour():
	form = AdvertfourForm()
			
	if form.validate_on_submit():

		poster = current_user.id
		advertfour = Advertfours(title=form.title.data, current_user=form.current_user.data, deal=form.deal.data, percentage=form.percentage.data, link=form.link.data, alt=form.alt.data, content=form.content.data, file=form.file.data, poster_id=poster, slug=form.slug.data)
		
		#check for file
		if request.files['file']:
			advertfour.file = request.files['file']

			#Grab Image name
			filename = secure_filename(advertfour.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			advertfour.file = file_name

			try:
				db.session.add(advertfour)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash("Hello Admin you have Successfully Published an Advert !")
				return render_template("admin.html",
					form=form,
					advertfour=advertfour)
			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("add_advertcolumnone.html",
					form=form,
					advertfour=advertfour)
		else:
			db.session.add(advertfour)
			db.session.commit()
			flash("Hello Admin you have Successfully Published an Advert !")
			return render_template("admin.html",
				form=form,
				advertfour=advertfour)
		
		#clear the form
		form.title.data = ''
		form.content.data = ''
		form.slug.data = ''
		form.file.data = ''
		form.alt.data = ''
		form.percentage.data = ''
		form.deal.data = ''
		form.link.data = ''
		form.current_user.data = ''

		#add post data to database
		db.session.add(advertfour)
		db.session.commit()

	return render_template("add_advertcolumnfour.html",
			form=form,
			id = id or 1)

@app.route('/advertfours/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_advertfour(id):
	advertfour = Advertfours.query.get_or_404(id)
	form = AdvertfourForm()

	if form.validate_on_submit():
		advertfour.title = form.title.data
		advertfour.slug = form.slug.data
		advertfour.content = form.content.data
		advertfour.file = form.file.data
		advertfour.alt = form.alt.data
		advertfour.link = form.link.data
		advertfour.percentage = form.percentage.data
		advertfour.deal = form.deal.data
		advertfour.current_user = form.current_user.data


		#check for file
		if request.files['file']:
			advertfour.file = request.files['file']

			#Grab Image name
			filename = secure_filename(advertfour.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename

			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			advertfour.file = file_name

			try:
				db.session.add(advertfour)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash(" You have Successfully Updated Your Post !")
				return render_template("advertfours.html",
					form=form,
					advertfour=advertfour)

			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("edit_advertfour.html",
					form=form,
					advertfour=advertfour)

		else:
			db.session.add(advertfour)
			db.session.commit()
			flash(" You have Successfully Updated Your Post !")
			return render_template("advertfours.html",
				form=form,
				advertfour=advertfour)

		#Update to DataBase
		db.session.add(advertfour)
		db.session.commit()

		flash("Post Successfully Updated")
		return redirect(url_for('advertfour', id=advertfour.id))

	if current_user.id == advertfour.poster_id or current_user.id == 1 :
		form.title.data = advertfour.title
		form.slug.data = advertfour.slug
		form.content.data = advertfour.content
		form.file.data = advertfour.file
		form.alt.data = advertfour.alt
		form.percentage.data = advertfour.percentage
		form.deal.data = advertfour.deal
		form.current_user.data = advertfour.current_user
		return render_template('edit_advertfour.html', form=form)

	else:
		flash(" You need Authorization to access this Post")
		advertfours = Advertfours.query.order_by(Advertfours.date_posted)
		return render_template("dashboard.html", advertfours=advertfours)

@app.route('/advertfours/delete/<int:id>')
@login_required
def delete_advertfour(id):
	advertfour_to_delete = Advertfours.query.get_or_404(id)
	id = current_user.id
	if id == advertfour_to_delete.poster_id or id == 1:
		try:
			db.session.delete(advertfour_to_delete)
			db.session.commit()

			#return message
			flash ("Blog Post Was Deleted Successfully!")
			

			#Grab all the post from the DataBase
			advertfours = Advertfours.query.order_by(Advertfours.date_posted)
			return render_template("advertfours.html", advertfours=advertfours)

		except:
			#return error message
			flash ("Whoops!!! There was a Problem Deleting Post Try Again...")

			#Grab all the post from the DataBase
			advertfours = Advertfours.query.order_by(Advertfours.date_posted)
			return render_template("advertfours.html", advertfours=advertfours)
	else:
		#return message
		flash("You are not authorized to Delete this Post!")

		#Grab all the post from the DataBase
		advertfours = Advertfours.query.order_by(Advertfours.date_posted)
		return render_template("advertfours.html", advertfours=advertfours)
	
@app.route('/advertfours')
def advertfours():
	#Grab all the post from the DataBase
	advertfours = Advertfours.query.order_by(Advertfours.date_posted)
	return render_template("advertfours.html", advertfours=advertfours)

@app.route('/advertfours/<int:id>')
def advertfour(id):
	advertfours = Advertfours.query.get_or_404(id)
	return render_template("advertfour.html", advertfour=advertfour)































#Necessary Links
@app.route("/cookie")
@login_required
def cookie():
		return render_template("cookie.html")

@app.route("/contribute")
@login_required
def contribute():
		return render_template("contribute.html")

@app.route("/service")
@login_required
def service():
		return render_template("service.html")

@app.route("/about")
@login_required
def about():
		return render_template("about.html")

@app.route("/privacy")
@login_required
def privacy():
		return render_template("privacy.html")

@app.route("/terms-and-conditions")
@login_required
def terms_and_conditions():
		return render_template("terms-and-conditions.html")


@app.route("/disclaimer")
@login_required
def disclaimer():
		return render_template("disclaimer.html")

@app.route("/community", methods=['GET', 'POST'])
@login_required
def community():
	form = CommunityForm()
			
	if form.validate_on_submit():

		poster = current_user.id
		community = Communities(title=form.title.data, content=form.content.data, poster_id=poster, slug=form.slug.data)
				
		#clear the form
		form.title.data = ''
		form.content.data = ''
		form.slug.data = ''

		#add post data to database
		db.session.add(community)
		db.session.commit()

	return render_template("community.html",
			form=form,
			id = id or 1)

#Search Function
@app.route('/search', methods=["POST"])
def search():
	form = SearchForm()
	posts = Posts.query
	if form.validate_on_submit():
		post.searched = form.searched.data
		
		#Query the Database
		posts = Posts.filter_by(Posts.content.like('%' + post.searched + '%'))
		posts = Posts.order_by(Posts.title.desc()).all()

		return render_template("search.html",
			form=form,
			searched=post.searched,
			posts=posts)

#Pass Stuff to NavBar
@app.context_processor
def base():
	form = SearchForm()
	return dict(form=form)


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
	form = UserForm()
	id = current_user.id or 1
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.username = request.form['username']
		name_to_update.about_author = request.form['about_author']
		
		#check for profile pic
		if request.files['profile_pic']:
			name_to_update.profile_pic = request.files['profile_pic']

			#Grab Image name
			pic_filename = secure_filename(name_to_update.profile_pic.filename)

			#set the uuid
			pic_name = str(uuid.uuid1()) + "_" + pic_filename
			
			#save the image
			saver = request.files['profile_pic']

			#change it to a String to save to db
			name_to_update.profile_pic = pic_name

			try:
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
				flash("User Updated Successfully !")
				return render_template("dashboard.html",
					form=form,
					name_to_update = name_to_update)
			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("dashboard.html",
					form=form,
					name_to_update = name_to_update)
		else:
			db.session.commit()
			flash("User Updated Successfully !")
			return render_template("dashboard.html",
				form=form,
				name_to_update = name_to_update)

	else:
		return render_template("dashboard.html",
				form=form,
				name_to_update = name_to_update, 
				id = id or 1)


	return render_template('dashboard.html')

@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
	post_to_delete = Posts.query.get_or_404(id)
	id = current_user.id
	if id == post_to_delete.poster_id or id == 1:
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
	else:
		#return message
		flash("You are not authorized to Delete this Post!")

		#Grab all the post from the DataBase
		posts = Posts.query.order_by(Posts.date_posted)
		return render_template("posts.html", posts=posts)
	
@app.route('/posts')
def posts():
	#Grab all the post from the DataBase
	posts = Posts.query.order_by(Posts.date_posted.desc()).limit(5)
	finances = Finances.query.order_by(Finances.date_posted.desc()).limit(1)
	ideas = Ideas.query.order_by(Ideas.date_posted.desc()).limit(1)
	designs = Designs.query.order_by(Designs.date_posted.desc()).limit(1)
	essays = Essays.query.order_by(Essays.date_posted.desc()).limit(1)
	greens = Greens.query.order_by(Greens.date_posted.desc()).limit(1)
	businesses = Businesses.query.order_by(Businesses.date_posted.desc()).limit(1)
	healths = Healths.query.order_by(Healths.date_posted.desc()).limit(1)
	organises = Organises.query.order_by(Organises.date_posted.desc()).limit(1)
	advertones = Advertones.query.order_by(Advertones.date_posted.desc()).limit(1)
	return render_template("posts.html", 
		posts=posts,
		finances=finances,
		ideas=ideas,
		designs=designs,
		essays=essays,
		greens=greens,
		businesses=businesses,
		healths=healths,
		organises=organises)


@app.route('/posts/<int:id>')
def post(id):
	post = Posts.query.get_or_404(id)
	finances = Finances.query.order_by(Finances.date_posted.desc()).limit(1)
	ideas = Ideas.query.order_by(Ideas.date_posted.desc()).limit(1)
	designs = Designs.query.order_by(Designs.date_posted.desc()).limit(1)
	essays = Essays.query.order_by(Essays.date_posted.desc()).limit(1)
	greens = Greens.query.order_by(Greens.date_posted.desc()).limit(1)
	businesses = Businesses.query.order_by(Businesses.date_posted.desc()).limit(1)
	healths = Healths.query.order_by(Healths.date_posted.desc()).limit(1)
	organises = Organises.query.order_by(Organises.date_posted.desc()).limit(1)
	advertones = Advertones.query.order_by(Advertones.date_posted.desc()).limit(1)
	
	return render_template("post.html", 
		post=post,
		finances=finances,
		ideas=ideas,
		designs=designs,
		essays=essays,
		greens=greens,
		businesses=businesses,
		healths=healths,
		organises=organises)


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required		
def edit_post(id):
	post = Posts.query.get_or_404(id)
	form = PostForm()

	if form.validate_on_submit():
		post.title = form.title.data
		post.slug = form.slug.data
		post.content = form.content.data
		post.file = form.file.data
		post.alt = form.alt.data

		#check for file
		if request.files['file']:
			post.file = request.files['file']

			#Grab Image name
			filename = secure_filename(post.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			post.file = file_name

			try:
				db.session.add(post)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash("Post Successfully Added !")
				return render_template("posts.html",
					form=form,
					post=post)
			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("add_post.html",
					form=form,
					post=post)
		else:
			db.session.add(post)
			db.session.commit()
			flash("Post Successfully Added !")
			return render_template("posts.html",
				form=form,
				post=post)
		
		db.session.add(post)
		db.session.commit()

		flash("Post Successfully Updated")
		return redirect(url_for('post', id=post.id))

	if current_user.id == post.poster_id or current_user.id == 1 :
		form.title.data = post.title
		form.slug.data = post.slug
		form.content.data = post.content
		form.alt.data = post.alt
		form.file.data = post.file
		return render_template('edit_post.html', form=form)

	else:
		flash(" You need Authorization to access this Post")
		posts = Posts.query.order_by(Posts.date_posted)
		return render_template("posts.html", posts=posts)

#Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
	form = PostForm()
			
	if form.validate_on_submit():

		poster = current_user.id
		post = Posts(title=form.title.data, alt=form.alt.data, content=form.content.data, file=form.file.data, poster_id=poster, slug=form.slug.data)

		#check for file
		if request.files['file']:
			post.file = request.files['file']

			#Grab Image name
			filename = secure_filename(post.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			post.file = file_name

			try:
				db.session.add(post)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash("Post Successfully Added !")
				return render_template("posts.html",
					form=form,
					post=post)
			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("add_post.html",
					form=form,
					post=post)
		else:
			db.session.add(post)
			db.session.commit()
			flash("Post Successfully Added !")
			return render_template("posts.html",
				form=form,
				post=post)
		
		#clear the form
		form.title.data = ''
		form.content.data = ''
		form.slug.data = ''
		form.file.data = ''
		form.alt.data = ''

		#add post data to database
		db.session.add(post)
		db.session.commit()

	return render_template("add_post.html",
			form=form,
			id = id or 1)

#Add Business Post Page
@app.route('/add-business', methods=['GET', 'POST'])
def add_business():
	form = BusinessForm()

	if form.validate_on_submit():

		poster = current_user.id
		business = Businesses(title=form.title.data, file=form.file.data, alt=form.alt.data, content=form.content.data, poster_id=poster, slug=form.slug.data)

		#check for file
		if request.files['file']:
			business.file = request.files['file']

			#Grab Image name
			filename = secure_filename(business.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			business.file = file_name

			try:
				db.session.add(business)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash("Post Successfully Added !")
				return render_template("businesses.html",
					form=form,
					business=business)
			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("add_business.html",
					form=form,
					business=business)
		else:
			db.session.add(business)
			db.session.commit()
			flash("Post Successfully Added !")
			return render_template("businesses.html",
				form=form,
				business=business)
		
		#clear the form
		form.title.data = ''
		form.content.data = ''
		form.slug.data = ''
		form.alt.data = ''
		form.file.data = ''

		#add post data to database
		db.session.add(business)
		db.session.commit()

		#return a message
		flash("Blog Post Submitted Successfully !")


	#redirect to the webpage
	return render_template("add_business.html", form=form)


@app.route('/businesses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_business(id):
	business = Businesses.query.get_or_404(id)
	form = BusinessForm()

	if form.validate_on_submit():
		business.title = form.title.data
		business.slug = form.slug.data
		business.content = form.content.data
		business.alt = form.alt.data


		#check for file
		if request.files['file']:
			business.file = request.files['file']

			#Grab Image name
			filename = secure_filename(business.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			business.file = file_name

			try:
				db.session.add(business)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash("Post Successfully Updated !")
				return render_template("businesses.html",
					form=form,
					business=business)
			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("add_business.html",
					form=form,
					business=business)
		else:
			db.session.add(business)
			db.session.commit()
			flash("Post Successfully Updates !")
			return render_template("businesses.html",
				form=form,
				business=business)

		db.session.add(business)
		db.session.commit()

		flash("Post Successfully Updated")
		return redirect(url_for('business', id=business.id))

	if current_user.id == business.poster_id or current_user.id == 1 :
		form.title.data = business.title
		form.slug.data = business.slug
		form.content.data = business.content
		form.alt.data = business.alt
		return render_template('edit_business.html', form=form)

	else:
		flash(" You need Authorization to access this Post")
		businesses = Businesses.query.order_by(Businesses.date_posted)
		return render_template("businesses.html", businesses=businesses)


@app.route('/businesses/delete/<int:id>')
@login_required
def delete_business(id):
	business_to_delete = Businesses.query.get_or_404(id)
	id = current_user.id
	if id == business_to_delete.poster_id or id == 1:
		try:
			db.session.delete(business_to_delete)
			db.session.commit()

			#return message
			flash ("Blog Post Was Deleted Successfully!")
			

			#Grab all the post from the DataBase
			businesses = Businesses.query.order_by(Businesses.date_posted)
			return render_template("businesses.html", businesses=businesses)

		except:
			#return error message
			flash ("Whoops!!! There was a Problem Deleting Post Try Again...")

			#Grab all the post from the DataBase
			businesses = Businesses.query.order_by(Businesses.date_posted)
			return render_template("businesses.html", businesses=businesses)
	else:
		#return message
		flash("You are not authorized to Delete this Post!")

		#Grab all the post from the DataBase
		businesses = Businesses.query.order_by(Businesses.date_posted)
		return render_template("businesses.html", businesses=businesses)

@app.route('/businesses')
def businesses():
	#Grab all the post from the DataBase
	businesses = Businesses.query.order_by(Businesses.date_posted.desc()).limit(5)
	posts = Posts.query.order_by(Posts.date_posted.desc()).limit(1)
	finances = Finances.query.order_by(Finances.date_posted.desc()).limit(1)
	ideas = Ideas.query.order_by(Ideas.date_posted.desc()).limit(1)
	designs = Designs.query.order_by(Designs.date_posted.desc()).limit(1)
	essays = Essays.query.order_by(Essays.date_posted.desc()).limit(1)
	greens = Greens.query.order_by(Greens.date_posted.desc()).limit(1)
	healths = Healths.query.order_by(Healths.date_posted.desc()).limit(1)
	organises = Organises.query.order_by(Organises.date_posted.desc()).limit(1)
	advertones = Advertones.query.order_by(Advertones.date_posted)
	adverttwos = Adverttwos.query.order_by(Adverttwos.date_posted)
	advertthrees = Advertthrees.query.order_by(Advertthrees.date_posted)
	advertfours = Advertfours.query.order_by(Advertfours.date_posted)
	return render_template("businesses.html", 
		posts=posts,
		finances=finances,
		ideas=ideas,
		designs=designs,
		essays=essays,
		greens=greens,
		businesses=businesses,
		healths=healths,
		organises=organises)

@app.route('/businesses/<int:id>')
def business(id):
	business = Businesses.query.get_or_404(id)
	return render_template("business.html", business=business)

#Add Design Post Page
@app.route('/add-design', methods=['GET', 'POST'])
def add_design():
	form = DesignForm()

	if form.validate_on_submit():

		poster = current_user.id
		design = Designs(title=form.title.data, file=form.file.data, alt=form.alt.data, content=form.content.data, poster_id=poster, slug=form.slug.data)

		#check for file
		if request.files['file']:
			design.file = request.files['file']

			#Grab Image name
			filename = secure_filename(design.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			design.file = file_name

			try:
				db.session.add(design)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash("Post Successfully Added !")
				return render_template("designs.html",
					form=form,
					design=design)
			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("add_design.html",
					form=form,
					design=design)
		else:
			db.session.add(design)
			db.session.commit()
			flash("Post Successfully Added !")
			return render_template("designs.html",
				form=form,
				design=design)

		
		#clear the form
		form.title.data = ''
		form.content.data = ''
		form.slug.data = ''
		form.alt.data = ''
		form.file.data = ''

		#add post data to database
		db.session.add(design)
		db.session.commit()

		#return a message
		flash(" Post Submitted Successfully !")


	#redirect to the webpage
	return render_template("add_design.html", form=form)

@app.route('/designs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_design(id):
	design = Designs.query.get_or_404(id)
	form = DesignForm()

	if form.validate_on_submit():
		design.title = form.title.data
		design.slug = form.slug.data
		design.content = form.content.data
		design.alt = form.alt.data
		design.file = form.file.data

		#check for file
		if request.files['file']:
			design.file = request.files['file']

			#Grab Image name
			filename = secure_filename(design.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			design.file = file_name

			try:
				db.session.add(design)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash(" You have Successfully Updated Your Post !")
				return render_template("designs.html",
					form=form,
					design=design)

			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("edit_design.html",
					form=form,
					design=design)
		else:
			db.session.add(design)
			db.session.commit()
			flash(" You have Successfully Updated Your Post !")
			return render_template("designs.html",
				form=form,
				design=design)

		#Update to DataBase
		db.session.add(design)
		db.session.commit()

		flash("Post Successfully Updated")
		return redirect(url_for('design', id=design.id))

	if current_user.id == design.poster_id or current_user.id == 1 :
		form.title.data = design.title
		form.slug.data = design.slug
		form.content.data = design.content
		form.alt.data = design.alt
		form.file.data = design.file
		return render_template('edit_design.html', form=form)

	else:
		flash(" You need Authorization to access this Post")
		designs = Designs.query.order_by(Designs.date_posted)
		return render_template("designs.html", designs=designs)

@app.route('/designs/delete/<int:id>')
@login_required
def delete_design(id):
	design_to_delete = Designs.query.get_or_404(id)
	id = current_user.id
	if id == design_to_delete.poster_id or id == 1:
		try:
			db.session.delete(design_to_delete)
			db.session.commit()

			#return message
			flash ("Blog Post Was Deleted Successfully!")
			
			#Grab all the post from the DataBase
			designs = Designs.query.order_by(Designs.date_posted)
			return render_template("designs.html", designs=designs)

		except:
			#return error message
			flash ("Whoops!!! There was a Problem Deleting Post Try Again...")

			#Grab all the post from the DataBase
			designs = Designs.query.order_by(Designs.date_posted)
			return render_template("designs.html", designs=designs)
	else:
		#return message
		flash("You are not authorized to Delete this Post!")

		#Grab all the post from the DataBase
		designs = Designs.query.order_by(Designs.date_posted)
		return render_template("designs.html", designs=designs)

@app.route('/designs')
def designs():
	#Grab all the post from the DataBase
	designs = Designs.query.order_by(Designs.date_posted.desc()).limit(5)
	posts = Posts.query.order_by(Posts.date_posted.desc()).limit(1)
	finances = Finances.query.order_by(Finances.date_posted.desc()).limit(1)
	ideas = Ideas.query.order_by(Ideas.date_posted.desc()).limit(1)
	essays = Essays.query.order_by(Essays.date_posted.desc()).limit(1)
	greens = Greens.query.order_by(Greens.date_posted.desc()).limit(1)
	businesses = Businesses.query.order_by(Businesses.date_posted.desc()).limit(1)
	healths = Healths.query.order_by(Healths.date_posted.desc()).limit(1)
	organises = Organises.query.order_by(Organises.date_posted.desc()).limit(1)
	return render_template("designs.html", 
		posts=posts,
		finances=finances,
		ideas=ideas,
		designs=designs,
		essays=essays,
		greens=greens,
		businesses=businesses,
		healths=healths,
		organises=organises)

@app.route('/designs/<int:id>')
def design(id):
	design = Designs.query.get_or_404(id)
	return render_template("design.html", design=design)


#Add Essay Post Page
@app.route('/add-essay', methods=['GET', 'POST'])
def add_essay():
	form = EssayForm()

	if form.validate_on_submit():

		poster = current_user.id
		essay = Essays(title=form.title.data, file=form.file.data, alt=form.alt.data, content=form.content.data, poster_id=poster, slug=form.slug.data)

		#check for file
		if request.files['file']:
			essay.file = request.files['file']

			#Grab Image name
			filename = secure_filename(essay.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			essay.file = file_name

			try:
				db.session.add(essay)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash("Post Successfully Added !")
				return render_template("essays.html",
					form=form,
					essay=essay)
			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("add_essay.html",
					form=form,
					essay=essay)
		else:
			db.session.add(essay)
			db.session.commit()
			flash("Post Successfully Added !")
			return render_template("essays.html",
				form=form,
				essay=essay)

		
		#clear the form
		form.title.data = ''
		form.content.data = ''
		form.slug.data = ''
		form.file.data = ''
		form.alt.data = ''

		#add post data to database
		db.session.add(essay)
		db.session.commit()

		#return a message
		flash("Blog Post Submitted Successfully !")


	#redirect to the webpage
	return render_template("add_essay.html", form=form)

@app.route('/essays/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_essay(id):
	essay = Essays.query.get_or_404(id)
	form = EssayForm()

	if form.validate_on_submit():
		essay.title = form.title.data
		essay.slug = form.slug.data
		essay.content = form.content.data
		essay.alt = form.essay.data
		essay.file = form.file.data

		#check for file
		if request.files['file']:
			essay.file = request.files['file']

			#Grab Image name
			filename = secure_filename(essay.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			essay.file = file_name

			try:
				db.session.add(essay)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash(" You have Successfully Updated Your Post !")
				return render_template("essays.html",
					form=form,
					essay=essay)

			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("edit_essay.html",
					form=form,
					essay=essay)
		else:
			db.session.add(post)
			db.session.commit()
			flash(" You have Successfully Updated Your Post !")
			return render_template("essays.html",
				form=form,
				essay=essay)

		#Update to DataBase
		db.session.add(essay)
		db.session.commit()

		flash("Post Successfully Updated")
		return redirect(url_for('essay', id=essay.id))

	if current_user.id == essay.poster_id or current_user.id == 1 :
		form.title.data = essay.title
		form.slug.data = essay.slug
		form.content.data = essay.content
		form.file.data = essay.file
		form.alt.data = essay.alt
		return render_template('edit_essay.html', form=form)

	else:
		flash(" You need Authorization to access this Post")
		essays = Essays.query.order_by(Essays.date_posted)
		return render_template("essays.html", essays=essays)

@app.route('/essays/delete/<int:id>')
@login_required
def delete_essay(id):
	essay_to_delete = Essays.query.get_or_404(id)
	id = current_user.id
	if id == essay_to_delete.poster_id or id == 1:
		try:
			db.session.delete(essay_to_delete)
			db.session.commit()

			#return message
			flash ("Blog Post Was Deleted Successfully!")
			

			#Grab all the post from the DataBase
			essays = Essays.query.order_by(Essays.date_posted)
			return render_template("essays.html", essays=essays)

		except:
			#return error message
			flash ("Whoops!!! There was a Problem Deleting Post Try Again...")

			#Grab all the post from the DataBase
			essays = Essays.query.order_by(Essays.date_posted)
			return render_template("essays.html", essays=essays)
	else:
		#return message
		flash("You are not authorized to Delete this Post!")

		#Grab all the post from the DataBase
		essays = Essays.query.order_by(Essays.date_posted)
		return render_template("essays.html", essays=essays)

@app.route('/essays')
def essays():
	#Grab all the post from the DataBase
	posts = Posts.query.order_by(Posts.date_posted.desc()).limit(1)
	finances = Finances.query.order_by(Finances.date_posted.desc()).limit(1)
	ideas = Ideas.query.order_by(Ideas.date_posted.desc()).limit(1)
	designs = Designs.query.order_by(Designs.date_posted.desc()).limit(1)
	essays = Essays.query.order_by(Essays.date_posted.desc()).limit(5)
	greens = Greens.query.order_by(Greens.date_posted.desc()).limit(1)
	businesses = Businesses.query.order_by(Businesses.date_posted.desc()).limit(1)
	healths = Healths.query.order_by(Healths.date_posted.desc()).limit(1)
	organises = Organises.query.order_by(Organises.date_posted.desc()).limit(1)
	return render_template("essays.html", 
		posts=posts,
		finances=finances,
		ideas=ideas,
		designs=designs,
		essays=essays,
		greens=greens,
		businesses=businesses,
		healths=healths,
		organises=organises)

@app.route('/essays/<int:id>')
def essay(id):
	essay = Essays.query.get_or_404(id)
	return render_template("essay.html", essay=essay)

#Add Finance Post Page
@app.route('/add-finance', methods=['GET', 'POST'])
def add_finance():
	form = FinanceForm()

	if form.validate_on_submit():

		poster = current_user.id
		finance = Finances(title=form.title.data, file=form.file.data, alt=form.alt.data, content=form.content.data, poster_id=poster, slug=form.slug.data)

		#check for file
		if request.files['file']:
			finance.file = request.files['file']

			#Grab Image name
			filename = secure_filename(finance.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			finance.file = file_name

			try:
				db.session.add(finance)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash("Post Successfully Added !")
				return render_template("finances.html",
					form=form,
					finance=finance)
			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("add_finance.html",
					form=form,
					finance=finance)
		else:
			db.session.add(finance)
			db.session.commit()
			flash("Post Successfully Added !")
			return render_template("finances.html",
				form=form,
				finances=finance)

		
		#clear the form
		form.title.data = ''
		form.content.data = ''
		form.slug.data = ''
		form.file.data = ''
		form.alt.data = ''

		#add post data to database
		db.session.add(finance)
		db.session.commit()

		#return a message
		flash("Blog Post Submitted Successfully !")


	#redirect to the webpage
	return render_template("add_finance.html", form=form)

@app.route('/finances/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_finance(id):
	finance = Finances.query.get_or_404(id)
	form = FinanceForm()

	if form.validate_on_submit():
		finance.title = form.title.data
		finance.slug = form.slug.data
		finance.content = form.content.data
		finance.alt = form.alt.data
		finance.file = form.file.data

		#check for file
		if request.files['file']:
			finance.file = request.files['file']

			#Grab Image name
			filename = secure_filename(finance.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			finance.file = file_name

			try:
				db.session.add(finance)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash(" You have Successfully Updated Your Post !")
				return render_template("finances.html",
					form=form,
					finance=finance)

			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("edit_finance.html",
					form=form,
					finance=finance)
		else:
			db.session.add(finance)
			db.session.commit()
			flash(" You have Successfully Updated Your Post !")
			return render_template("posts.html",
				form=form,
				finance=finance)

		#Update to DataBase
		db.session.add(finance)
		db.session.commit()

		flash("Post Successfully Updated")
		return redirect(url_for('finance', id=finance.id))

	if current_user.id == finance.poster_id or current_user.id == 1 :
		form.title.data = finance.title
		form.slug.data = finance.slug
		form.content.data = finance.content
		return render_template('edit_finance.html', form=form)

	else:
		flash(" You need Authorization to access this Post")
		finances = Finances.query.order_by(Finances.date_posted)
		return render_template("finances.html", finances=finances)

@app.route('/finances/delete/<int:id>')
@login_required
def delete_finance(id):
	finance_to_delete = Finances.query.get_or_404(id)
	id = current_user.id
	if id == finance_to_delete.poster_id or id == 1:
		try:
			db.session.delete(finance_to_delete)
			db.session.commit()

			#return message
			flash ("Blog Post Was Deleted Successfully!")
			

			#Grab all the post from the DataBase
			finance = Finances.query.order_by(Finances.date_posted)
			return render_template("finances.html", finances=finances)

		except:
			#return error message
			flash ("Whoops!!! There was a Problem Deleting Post Try Again...")

			#Grab all the post from the DataBase
			finances = Finances.query.order_by(Finances.date_posted)
			return render_template("finances.html", finances=finances)
	else:
		#return message
		flash("You are not authorized to Delete this Post!")

		#Grab all the post from the DataBase
		finances = Finances.query.order_by(Finances.date_posted)
		return render_template("finances.html", finances=finances)

@app.route('/finances')
def finances():
	#Grab all the post from the DataBase
	finances = Finances.query.order_by(Finances.date_posted.desc())
	posts = Posts.query.order_by(Posts.date_posted.desc()).limit(1)
	advertones = Advertones.query.order_by(Advertones.date_posted.desc()).limit(1)
	return render_template("finances.html", 
		finances=finances,
		posts=posts,
		advertones=advertones)


@app.route('/finances/<int:id>')
def finance(id):
	finance = Finances.query.get_or_404(id)
	posts = Posts.query.order_by(Posts.date_posted.desc()).limit(1)
	ideas = Ideas.query.order_by(Ideas.date_posted.desc()).limit(1)
	designs = Designs.query.order_by(Designs.date_posted.desc()).limit(1)
	essays = Essays.query.order_by(Essays.date_posted.desc()).limit(1)
	greens = Greens.query.order_by(Greens.date_posted.desc()).limit(1)
	businesses = Businesses.query.order_by(Businesses.date_posted.desc()).limit(1)
	healths = Healths.query.order_by(Healths.date_posted.desc()).limit(1)
	organises = Organises.query.order_by(Organises.date_posted.desc()).limit(1)
	advertones = Advertones.query.order_by(Advertones.date_posted.desc()).limit(1)
	
	return render_template("finance.html", 
		finance=finance,
		posts=posts,
		ideas=ideas,
		designs=designs,
		essays=essays,
		greens=greens,
		businesses=businesses,
		healths=healths,
		organises=organises)

#Add Green Post Page
@app.route('/add-green', methods=['GET', 'POST'])
def add_green():
	form = GreenForm()

	if form.validate_on_submit():

		poster = current_user.id
		green = Greens(title=form.title.data, alt=form.alt.data, content=form.content.data, file=form.file.data, poster_id=poster, slug=form.slug.data)

		#check for file
		if request.files['file']:
			green.file = request.files['file']

			#Grab Image name
			filename = secure_filename(green.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			green.file = file_name

			try:
				db.session.add(green)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash("User Updated Successfully !")
				return render_template("greens.html",
					form=form,
					green=green)
			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("add_green.html",
					form=form,
					green=green)
		else:
			db.session.add(green)
			db.session.commit()
			flash("User Updated Successfully !")
			return render_template("greens.html",
				form=form,
				green=green)

		
		#clear the form
		form.title.data = ''
		form.content.data = ''
		form.slug.data = ''
		form.file.data = ''
		form.alt.data = ''

		#add post data to database
		db.session.add(green)
		db.session.commit()

		#return a message
		flash("Blog Post Submitted Successfully !")


	#redirect to the webpage
	return render_template("add_green.html", form=form)

@app.route('/greens/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_green(id):
	green = Greens.query.get_or_404(id)
	form = GreenForm()

	if form.validate_on_submit():
		green.title = form.title.data
		green.slug = form.slug.data
		green.content = form.content.data

		#check for file
		if request.files['file']:
			green.file = request.files['file']

			#Grab Image name
			filename = secure_filename(green.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			green.file = file_name

			try:
				db.session.add(green)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash(" You have Successfully Updated Your Post !")
				return render_template("greens.html",
					form=form,
					green=green)

			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("edit_green.html",
					form=form,
					green=green)
		else:
			db.session.add(green)
			db.session.commit()
			flash(" You have Successfully Updated Your Post !")
			return render_template("posts.html",
				form=form,
				green=green)

		#Update to DataBase
		db.session.add(green)
		db.session.commit()

		flash("Post Successfully Updated")
		return redirect(url_for('green', id=green.id))

	if current_user.id == green.poster_id or current_user.id == 1 :
		form.title.data = green.title
		form.slug.data = green.slug
		form.content.data = green.content
		return render_template('edit_green.html', form=form)

	else:
		flash(" You need Authorization to access this Post")
		greens = Greens.query.order_by(Greens.date_posted)
		return render_template("greens.html", greens=greens)

@app.route('/green/delete/<int:id>')
@login_required
def delete_green(id):
	green_to_delete = Greens.query.get_or_404(id)
	id = current_user.id
	if id == green_to_delete.poster_id or id == 1:
		try:
			db.session.delete(green_to_delete)
			db.session.commit()

			#return message
			flash ("Blog Post Was Deleted Successfully!")
			

			#Grab all the post from the DataBase
			greens = Greens.query.order_by(Greens.date_posted)
			return render_template("Greens.html", greens=greens)

		except:
			#return error message
			flash ("Whoops!!! There was a Problem Deleting Post Try Again...")

			#Grab all the post from the DataBase
			greens = Greens.query.order_by(Greens.date_posted)
			return render_template("greens.html", greens=greens)
	else:
		#return message
		flash("You are not authorized to Delete this Post!")

		#Grab all the post from the DataBase
		greens = Greens.query.order_by(Greens.date_posted)
		return render_template("greens.html", greens=greens)

@app.route('/greens')
def greens():
	#Grab all the post from the DataBase
	posts = Posts.query.order_by(Posts.date_posted.desc()).limit(1)
	finances = Finances.query.order_by(Finances.date_posted.desc()).limit(1)
	ideas = Ideas.query.order_by(Ideas.date_posted.desc()).limit(1)
	designs = Designs.query.order_by(Designs.date_posted.desc()).limit(1)
	essays = Essays.query.order_by(Essays.date_posted.desc()).limit(1)
	greens = Greens.query.order_by(Greens.date_posted.desc()).limit(5)
	businesses = Businesses.query.order_by(Businesses.date_posted.desc()).limit(1)
	healths = Healths.query.order_by(Healths.date_posted.desc()).limit(1)
	organises = Organises.query.order_by(Organises.date_posted.desc()).limit(1)
	return render_template("greens.html", 
		posts=posts,
		finances=finances,
		ideas=ideas,
		designs=designs,
		essays=essays,
		greens=greens,
		businesses=businesses,
		healths=healths,
		organises=organises)

@app.route('/greens/<int:id>')
def green(id):
	green = Greens.query.get_or_404(id)
	return render_template("green.html", green=green)

#Add Health Post Page
@app.route('/add-health', methods=['GET', 'POST'])
def add_health():
	form = HealthForm()

	if form.validate_on_submit():

		poster = current_user.id
		health = Healths(title=form.title.data, alt=form.alt.data, content=form.content.data, file=form.file.data, poster_id=poster, slug=form.slug.data)

		#check for file
		if request.files['file']:
			health.file = request.files['file']

			#Grab Image name
			filename = secure_filename(health.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			health.file = file_name

			try:
				db.session.add(health)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash("User Updated Successfully !")
				return render_template("healths.html",
					form=form,
					health=health)
			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("add_health.html",
					form=form,
					health=health)
		else:
			db.session.add(health)
			db.session.commit()
			flash("User Updated Successfully !")
			return render_template("healths.html",
				form=form,
				health=health)
		
		#clear the form
		form.title.data = ''
		form.content.data = ''
		form.slug.data = ''
		form.file.data = ''
		form.alt.data = ''

		#add post data to database
		db.session.add(health)
		db.session.commit()

		#return a message
		flash("Blog Post Submitted Successfully !")


	#redirect to the webpage
	return render_template("add_health.html", form=form)

@app.route('/healths/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_health(id):
	health = Healths.query.get_or_404(id)
	form = GreenForm()

	if form.validate_on_submit():
		health.title = form.title.data
		health.slug = form.slug.data
		health.content = form.content.data
		health.alt = form.alt.data
		health.file = form.file.data

		#check for file
		if request.files['file']:
			health.file = request.files['file']

			#Grab Image name
			filename = secure_filename(health.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			health.file = file_name

			try:
				db.session.add(health)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash(" You have Successfully Updated Your Post !")
				return render_template("healths.html",
					form=form,
					health=health)

			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("edit_health.html",
					form=form,
					health=health)
		else:
			db.session.add(health)
			db.session.commit()
			flash(" You have Successfully Updated Your Post !")
			return render_template("healths.html",
				form=form,
				health=health)

		#Update to DataBase
		db.session.add(health)
		db.session.commit()

		flash("Post Successfully Updated")
		return redirect(url_for('health', id=health.id))

	if current_user.id == health.poster_id or current_user.id == 1 :
		form.title.data = health.title
		form.slug.data = health.slug
		form.content.data = health.content
		form.alt.data = health.alt
		form.file.data = health.file
		return render_template('edit_health.html', form=form)

	else:
		flash(" You need Authorization to access this Post")
		healths = Healths.query.order_by(Healths.date_posted)
		return render_template("greens.html", healths=healths)

@app.route('/health/delete/<int:id>')
@login_required
def delete_health(id):
	health_to_delete = Healths.query.get_or_404(id)
	id = current_user.id
	if id == health_to_delete.poster_id or id == 1:
		try:
			db.session.delete(health_to_delete)
			db.session.commit()

			#return message
			flash ("Blog Post Was Deleted Successfully!")
			

			#Grab all the post from the DataBase
			healths = Healths.query.order_by(Healths.date_posted)
			return render_template("Healths.html", greens=greens)

		except:
			#return error message
			flash ("Whoops!!! There was a Problem Deleting Post Try Again...")

			#Grab all the post from the DataBase
			healths = Healths.query.order_by(Healths.date_posted)
			return render_template("healths.html", healths=healths)
	else:
		#return message
		flash("You are not authorized to Delete this Post!")

		#Grab all the post from the DataBase
		healths = Healths.query.order_by(Healths.date_posted)
		return render_template("healths.html", healths=healths)

@app.route('/healths')
def healths():
	#Grab all the post from the DataBase
	posts = Posts.query.order_by(Posts.date_posted.desc()).limit(1)
	finances = Finances.query.order_by(Finances.date_posted.desc()).limit(1)
	ideas = Ideas.query.order_by(Ideas.date_posted.desc()).limit(1)
	designs = Designs.query.order_by(Designs.date_posted.desc()).limit(1)
	essays = Essays.query.order_by(Essays.date_posted.desc()).limit(1)
	greens = Greens.query.order_by(Greens.date_posted.desc()).limit(1)
	businesses = Businesses.query.order_by(Businesses.date_posted.desc()).limit(1)
	healths = Healths.query.order_by(Healths.date_posted.desc()).limit(5)
	organises = Organises.query.order_by(Organises.date_posted.desc()).limit(1)
	return render_template("healths.html", 
		posts=posts,
		finances=finances,
		ideas=ideas,
		designs=designs,
		essays=essays,
		greens=greens,
		businesses=businesses,
		healths=healths,
		organises=organises)

@app.route('/healths/<int:id>')
def health(id):
	health = Healths.query.get_or_404(id)
	return render_template("health.html", health=health)

#Add Ideas Post Page
@app.route('/add-idea', methods=['GET', 'POST'])
def add_idea():
	form = IdeaForm()

	if form.validate_on_submit():

		poster = current_user.id
		idea = Ideas(title=form.title.data, file=form.file.data, alt=form.alt.data, content=form.content.data, poster_id=poster, slug=form.slug.data)

		#check for file
		if request.files['file']:
			idea.file = request.files['file']

			#Grab Image name
			filename = secure_filename(idea.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			idea.file = file_name

			try:
				db.session.add(idea)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash("Post Successfully Added !")
				return render_template("ideas.html",
					form=form,
					idea=idea)
			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("add_idea.html",
					form=form,
					idea=idea)
		else:
			db.session.add(idea)
			db.session.commit()
			flash("Post Successfully Added !")
			return render_template("ideas.html",
				form=form,
				idea=idea)
		
		#clear the form
		form.title.data = ''
		form.content.data = ''
		form.slug.data = ''
		form.file.data = ''
		form.alt.data = ''

		#add post data to database
		db.session.add(idea)
		db.session.commit()

		#return a message
		flash("Blog Post Submitted Successfully !")


	#redirect to the webpage
	return render_template("add_idea.html", form=form)

@app.route('/ideas/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_idea(id):
	idea = Ideas.query.get_or_404(id)
	form = IdeaForm()

	if form.validate_on_submit():
		idea.title = form.title.data
		idea.slug = form.slug.data
		idea.content = form.content.data
		idea.alt = form.alt.data
		idea.file = form.file.data

		#check for file
		if request.files['file']:
			idea.file = request.files['file']

			#Grab Image name
			filename = secure_filename(idea.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			idea.file = file_name

			try:
				db.session.add(idea)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash(" You have Successfully Updated Your Post !")
				return render_template("ideas.html",
					form=form,
					idea=idea)

			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("edit_idea.html",
					form=form,
					idea=idea)
		else:
			db.session.add(idea)
			db.session.commit()
			flash(" You have Successfully Updated Your Post !")
			return render_template("posts.html",
				form=form,
				idea=idea)

		#Update to DataBase
		db.session.add(idea)
		db.session.commit()

		flash("Post Successfully Updated")
		return redirect(url_for('idea', id=idea.id))

	if current_user.id == idea.poster_id or current_user.id == 1 :
		form.title.data = idea.title
		form.slug.data = idea.slug
		form.content.data = idea.content
		form.alt.data = idea.alt
		form.file.data = idea.file
		return render_template('edit_idea.html', form=form)

	else:
		flash(" You need Authorization to access this Post")
		ideas = Ideas.query.order_by(Ideas.date_posted)
		return render_template("ideas.html", ideas=ideas)

@app.route('/ideas/delete/<int:id>')
@login_required
def delete_idea(id):
	idea_to_delete = Ideas.query.get_or_404(id)
	id = current_user.id
	if id == idea_to_delete.poster_id or id == 1:
		try:
			db.session.delete(idea_to_delete)
			db.session.commit()

			#return message
			flash ("Blog Post Was Deleted Successfully!")
			

			#Grab all the post from the DataBase
			ideas = Ideas.query.order_by(Ideas.date_posted)
			return render_template("ideas.html", ideas=ideas)

		except:
			#return error message
			flash ("Whoops!!! There was a Problem Deleting Post Try Again...")

			#Grab all the post from the DataBase
			ideas = Ideas.query.order_by(Ideasdeas.date_posted)
			return render_template("ideas.html", ideas=ideas)
	else:
		#return message
		flash("You are not authorized to Delete this Post!")

		#Grab all the post from the DataBase
		ideas = Ideas.query.order_by(Ideas.date_posted)
		return render_template("ideas.html", ideas=ideas)

@app.route('/ideas')
def ideas():
	#Grab all the post from the DataBase
	ideas = Ideas.query.order_by(Ideas.date_posted.desc()).limit(5)
	finances = Finances.query.order_by(Finances.date_posted.desc()).limit(1)
	designs = Designs.query.order_by(Designs.date_posted.desc()).limit(1)
	essays = Essays.query.order_by(Essays.date_posted.desc()).limit(1)
	posts = Posts.query.order_by(Posts.date_posted.desc()).limit(1)
	greens = Greens.query.order_by(Greens.date_posted.desc()).limit(1)
	businesses = Businesses.query.order_by(Businesses.date_posted.desc()).limit(1)
	healths = Healths.query.order_by(Healths.date_posted.desc()).limit(1)
	organises = Organises.query.order_by(Organises.date_posted.desc()).limit(1)
	return render_template("ideas.html", 
		ideas=ideas,
		posts=posts,
		finances=finances,
		designs=designs,
		essays=essays,
		greens=greens,
		businesses=businesses,
		healths=healths,
		organises=organises)

@app.route('/ideas/<int:id>')
def idea(id):
	idea = ideas.query.get_or_404(id)
	return render_template("idea.html", idea=idea)


#Add Post Page
@app.route('/add-organise', methods=['GET', 'POST'])
def add_organise():
	form = OrganiseForm()
			
	if form.validate_on_submit():

		poster = current_user.id
		Organises = Organises(title=form.title.data, alt=form.alt.data, content=form.content.data, file=form.file.data, poster_id=poster, slug=form.slug.data)

		#check for file
		if request.files['file']:
			organise.file = request.files['file']

			#Grab Image name
			filename = secure_filename(organise.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			organise.file = file_name

			try:
				db.session.add(organise)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash(" You have Successfully Added Your Backlink to this Site !")
				return render_template("organises.html",
					form=form,
					organise=organise)
			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("add_organise.html",
					form=form,
					organise=organise)
		else:
			db.session.add(organise)
			db.session.commit()
			flash(" You have Successfully Added Your Backlink to this Site !")
			return render_template("organises.html",
				form=form,
				organise=organise)
		
		#clear the form
		form.title.data = ''
		form.content.data = ''
		form.slug.data = ''
		form.file.data = ''
		form.alt.data = ''

		#add post data to database
		db.session.add(organise)
		db.session.commit()

	return render_template("add_organise.html",
			form=form,
			id = id or 1)

@app.route('/organises/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_organise(id):
	organise = Organises.query.get_or_404(id)
	form = OrganiseForm()

	if form.validate_on_submit():
		organise.title = form.title.data
		organise.slug = form.slug.data
		organise.content = form.content.data
		organise.file = form.file.data
		organise.alt = form.alt.data

		#check for file
		if request.files['file']:
			organise.file = request.files['file']

			#Grab Image name
			filename = secure_filename(organise.file.filename)

			#set the uuid
			file_name = str(uuid.uuid1()) + "_" + filename
			
			#save the image
			saver = request.files['file']

			#change it to a String to save to db
			organise.file = file_name

			try:
				db.session.add(organise)
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				flash(" You have Successfully Updated Your Post to the Site !")
				return render_template("posts.html",
					form=form,
					organise=organise)

			except:
				flash("Error! Looks Like There Was a Problem... Try Again!")
				return render_template("add_organise.html",
					form=form,
					organise=organise)
		else:
			db.session.add(organise)
			db.session.commit()
			flash(" You have Successfully Added Your Post to this Site !")
			return render_template("organises.html",
				form=form,
				organise=organise)

		#Update to DataBase
		db.session.add(organise)
		db.session.commit()

		flash("Site Article was Successfully Updated")
		return redirect(url_for('organise', id=organise.id))

	if current_user.id == organise.poster_id or current_user.id == 1 :
		form.title.data = organise.title
		form.slug.data = organise.slug
		form.content.data = organise.content
		form.file.data = organise.file
		form.alt.data = organise.alt
		return render_template('edit_organise.html', form=form)

	else:
		flash(" You need Authorization to access this Site Article")
		organises = Organises.query.order_by(Organises.date_posted)
		return render_template("organises.html", organises=organises)

@app.route('/organises/delete/<int:id>')
@login_required
def delete_organise(id):
	organise_to_delete = Organises.query.get_or_404(id)
	id = current_user.id
	if id == organise_to_delete.poster_id or id == 1:
		try:
			db.session.delete(organise_to_delete)
			db.session.commit()

			#return message
			flash ("Your Article Backlink was Deleted Successfully !")
			

			#Grab all the post from the DataBase
			organises = Organises.query.order_by(Organises.date_posted)
			return render_template("organises.html", organises=organises)

		except:
			#return error message
			flash ("Whoops!!! There was a Problem Deleting Post Try Again...")

			#Grab all the post from the DataBase
			organises = Organises.query.order_by(Organises.date_posted)
			return render_template("organises.html", organises=organises)
	else:
		#return message
		flash("You are not authorized to Delete this Site Backlink Article !")

		#Grab all the post from the DataBase
		organises = Organises.query.order_by(Organises.date_posted)
		return render_template("organises.html", organises=organises)
	

@app.route('/organises')
def organises():
	#Grab all the post from the DataBase
	posts = Posts.query.order_by(Posts.date_posted.desc()).limit(1)
	finances = Finances.query.order_by(Finances.date_posted.desc()).limit(1)
	ideas = Ideas.query.order_by(Ideas.date_posted.desc()).limit(1)
	designs = Designs.query.order_by(Designs.date_posted.desc()).limit(1)
	essays = Essays.query.order_by(Essays.date_posted.desc()).limit(1)
	greens = Greens.query.order_by(Greens.date_posted.desc()).limit(1)
	businesses = Businesses.query.order_by(Businesses.date_posted.desc()).limit(1)
	healths = Healths.query.order_by(Healths.date_posted.desc()).limit(1)
	organises = Organises.query.order_by(Organises.date_posted.desc()).limit(5)
	return render_template("organises.html", 
		posts=posts,
		finances=finances,
		ideas=ideas,
		designs=designs,
		essays=essays,
		greens=greens,
		businesses=businesses,
		healths=healths,
		organises=organises)


@app.route('/organises/<int:id>')
def organise(id):
	organise = Organises.query.get_or_404(id)
	return render_template("organise.html", organise=organise)

#Json Thing
@app.route('/date')
def get_current_date():
	return {"Date": date.today()}

#Delete DataBase
@app .route('/delete/<int:id>')
@login_required
def delete(id):
	if id == current_user.id:
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

	else:
		flash("Sorry, You can delete this User")
		return redirect(url_for('dashboard'))


#Create New DataBase Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.username = request.form['username']
		name_to_update.about_author = request.form['about_author']
		
		#check for profile pic
		if request.files['profile_pic']:
			name_to_update.profile_pic = request.files['profile_pic']

			#Grab Image name
			pic_filename = secure_filename(name_to_update.profile_pic.filename)

			#set the uuid
			pic_name = str(uuid.uuid1()) + "_" + pic_filename
			
			#save the image
			saver = request.files['profile_pic']

			#change it to a String to save to db
			name_to_update.profile_pic = pic_name

			try:
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
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
			db.session.commit()
			flash("User Updated Successfully !")
			return render_template("update.html",
				form=form,
				name_to_update = name_to_update)

	else:
		return render_template("update.html",
				form=form,
				name_to_update = name_to_update, 
				id = id or 1)

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

			flash("User Added Successfully")

		else:
			flash("This User Already Exist")
			return render_template("add_user.html",
				form=form)

		name = form.name.data
		form.name.data = ''
		form.username.data = ''
		form.email.data = ''
		form.password_hash = ''

	our_users = Users.query.order_by(Users.date_added)

	return render_template("add_user.html",
		form=form,
		name=name,
		our_users=our_users)

#create a route decorator
@app.route("/")
def index():
	#Grab all the post from the DataBase
	posts = Posts.query.order_by(Posts.date_posted.desc()).limit(1)
	businesses = Businesses.query.order_by(Businesses.date_posted.desc()).limit(1)
	finances = Finances.query.order_by(Finances.date_posted.desc()).limit(1)
	designs = Designs.query.order_by(Designs.date_posted.desc()).limit(1)
	essays = Essays.query.order_by(Essays.date_posted.desc()).limit(1)
	healths = Healths.query.order_by(Healths.date_posted.desc()).limit(1)
	greens = Greens.query.order_by(Greens.date_posted.desc()).limit(1)
	organises = Organises.query.order_by(Organises.date_posted.desc()).limit(1)
	advertones = Advertones.query.order_by(Advertones.date_posted.desc()).limit(1)
	adverttwos = Adverttwos.query.order_by(Adverttwos.date_posted.desc()).limit(1)
	advertthrees = Advertthrees.query.order_by(Advertthrees.date_posted.desc()).limit(1)
	advertfours = Advertfours.query.order_by(Advertfours.date_posted.desc()).limit(1)
	return render_template("index.html", 
		posts=posts,
		businesses=businesses,
		designs=designs,
		finances=finances,
		essays=essays,
		organises=organises,
		healths=healths,
		advertones=advertones,
		adverttwos=adverttwos)

@app.route('/files/<path:filename>')
def uploaded_files(filename):
	app = current_app._get_current_object()
	path = (app.config['UPLOAD_FOLDER'])
	return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])
def upload():
	app = current_app._get_current_object()
	f = request.files.get('upload')

	# Add more validations here
	extension = f.filename.split('.')[-1].lower()
	if extension not in ['jpg', 'gif', 'png', 'jpeg']:
		return upload_fail(message='Image only!')
	saver.save(os.path.join((app.config['UPLOAD_FOLDER']), f.filename))
	url = url_for('main.uploaded_files', filename=f.filename)
	return upload_success(url, filename=f.filename)


#localhost:5000/user/john
@app.route("/user")
@login_required
def user():
	poster = current_user.id
	posts = Posts.query.order_by(Posts.date_posted)
	businesses = Businesses.query.order_by(Businesses.date_posted)
	designs = Designs.query.order_by(Designs.date_posted)
	essays = Essays.query.order_by(Essays.date_posted)
	finances = Finances.query.order_by(Finances.date_posted)
	greens = Greens.query.order_by(Greens.date_posted)
	healths = Healths.query.order_by(Healths.date_posted)
	ideas = Ideas.query.order_by(Ideas.date_posted)
	return render_template("user.html",
		posts=posts,
		businesses=businesses,
		designs=designs,
		essays=essays,
		finances=finances,
		greens=greens,
		healths=healths,
		ideas=ideas)


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

#Create Advert Post
class Advertfours(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	file = db.Column(db.String(), nullable=True)
	percentage = db.Column(db.String(255), nullable=True)
	deal = db.Column(db.String(255), nullable=True)
	link = db.Column(db.String(255), nullable=False)
	alt = db.Column(db.String(100))
	content = db.Column(db.Text)
	current_user = db.Column(db.String(255), nullable=True)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))

	#Create a foreign Key to link two primary keys
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#Create Advert Post
class Advertthrees(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	file = db.Column(db.String(), nullable=True)
	percentage = db.Column(db.String(255), nullable=True)
	deal = db.Column(db.String(255), nullable=True)
	link = db.Column(db.String(255), nullable=False)
	alt = db.Column(db.String(100))
	content = db.Column(db.Text)
	current_user = db.Column(db.String(255), nullable=True)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))

	#Create a foreign Key to link two primary keys
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#Create Advert Post
class Adverttwos(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	file = db.Column(db.String(), nullable=True)
	percentage = db.Column(db.String(255), nullable=True)
	deal = db.Column(db.String(255), nullable=True)
	link = db.Column(db.String(255), nullable=False)
	alt = db.Column(db.String(100))
	content = db.Column(db.Text)
	current_user = db.Column(db.String(255), nullable=True)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))

	#Create a foreign Key to link two primary keys
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))


#Create Advert Post
class Advertones(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	file = db.Column(db.String(), nullable=True)
	percentage = db.Column(db.String(255), nullable=True)
	deal = db.Column(db.String(255), nullable=True)
	link = db.Column(db.String(255), nullable=False)
	alt = db.Column(db.String(100))
	content = db.Column(db.Text)
	current_user = db.Column(db.String(255), nullable=True)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))

	#Create a foreign Key to link two primary keys
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#Create A Community Post
class Communities(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))

	#Create a foreign Key to link two primary keys
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))








#Create A Organising Post
class Organises(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	file = db.Column(db.String(), nullable=False)
	alt = db.Column(db.String(100))
	content = db.Column(db.Text)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))

	#Create a foreign Key to link two primary keys
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#Create A Health Post
class Ideas(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	file = db.Column(db.String(), nullable=True)
	alt = db.Column(db.String(100))
	content = db.Column(db.Text)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))

	#Create a foreign Key to link two primary keys
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#Create A Health Post
class Healths(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	file = db.Column(db.String(), nullable=True)
	alt = db.Column(db.String(100))
	content = db.Column(db.Text)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))

	#Create a foreign Key to link two primary keys
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#Create A Finance Post
class Greens(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	file = db.Column(db.String(), nullable=True)
	alt = db.Column(db.String(100))
	content = db.Column(db.Text)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))

	#Create a foreign Key to link two primary keys
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#Create A Finance Post
class Finances(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	file = db.Column(db.String(), nullable=True)
	alt = db.Column(db.String(100))
	content = db.Column(db.Text)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))

	#Create a foreign Key to link two primary keys
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#Create A Essay Post
class Essays(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	file = db.Column(db.String(), nullable=True)
	alt = db.Column(db.String(100))
	content = db.Column(db.Text)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))

	#Create a foreign Key to link two primary keys
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#Create A Designs Post
class Designs(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	file = db.Column(db.String(), nullable=True)
	alt = db.Column(db.String(100))
	content = db.Column(db.Text)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))

	#Create a foreign Key to link two primary keys
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))


#Create A Businesses Post
class Businesses(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	file = db.Column(db.String(), nullable=True)
	alt = db.Column(db.String(100))
	content = db.Column(db.Text)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))

	#Create a foreign Key to link two primary keys
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))


#Create A Blog Post
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	file = db.Column(db.String(), nullable=False)
	alt = db.Column(db.String(100))
	content = db.Column(db.Text)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))

	#Create a foreign Key to link two primary keys
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#create a model
class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	name = db.Column(db.String(200), nullable=False)
	about_author = db.Column(db.Text(500), nullable=True)
	email = db.Column(db.String(200), nullable=False, unique=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)
	profile_pic = db.Column(db.String(), nullable=True)
	#Do Some Password Stuff
	password_hash = db.Column(db.String(128))

	#User can Have Many Posts
	posts = db.relationship('Posts', backref='poster')
	businesses = db.relationship('Businesses', backref='poster')
	designs = db.relationship('Designs', backref='poster')
	finances = db.relationship('Finances', backref='poster')
	essays = db.relationship('Essays', backref='poster')
	greens = db.relationship('Greens', backref='poster')
	healths = db.relationship('Healths', backref='poster')
	ideas = db.relationship('Ideas', backref='poster')
	advertones = db.relationship('Advertones', backref='poster')
	adverttwos = db.relationship('Adverttwos', backref='poster')
	advertthrees = db.relationship('Advertthrees', backref='poster')
	advertfours = db.relationship('Advertfours', backref='poster')
	communities = db.relationship('Communities', backref='poster')

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
