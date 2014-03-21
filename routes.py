from flask import Flask, render_template, request, flash, session, url_for, redirect, g, abort, send_from_directory
from forms import ContactForm, SignupForm, SigninForm, TapeForm
from flask.ext.mail import Message, Mail
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from database import db_session
import psycopg2
from sqlalchemy import *
import os
from werkzeug import secure_filename
from flask.ext.uploads import UploadSet, IMAGES, configure_uploads
from datetime import datetime
import time

mail = Mail()
app = Flask(__name__)
app.secret_key = "a_random_Transformer_secret_key_$%#!@"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trans:transformer@localhost/mydatabase'
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'Transformingthings@gmail.com'
app.config["MAIL_PASSWORD"] = 'nonmenclature'
app.config['UPLOAD_FOLDER'] = os.path.realpath('.') + '/static/img/productpics/' #UPLOAD_FOLDER
mail.init_app(app)
from models import User

photos = UploadSet('photos', IMAGES)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/signout')
def signout():

  if 'email' not in session:
    return redirect(url_for('signin'))
    
  session.pop('email', None)
  return redirect(url_for('home'))

@app.route('/')
def home():
  return render_template('home.html')
    
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  if 'email' in session:
    return redirect(url_for('welcome', form=form)) 
      
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      signin = User.query.filter_by(email = session['email']).first()
      if signin:
        signin = db_session.query(User.lastname).filter(User.email == session['email']).first()
        signfirst = db_session.query(User.firstname).filter(User.email == session['email']).first()
        signphone = db_session.query(User.phone).filter(User.email == session['email']).first()
        signcountry_id = db_session.query(User.country_id).filter(User.email == session['email']).first()
      return redirect(url_for('storedata', form=form))             
  elif request.method == 'GET':
    return render_template('signin.html', form=form)
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      g.newuser = User(form.firstname.data, form.lastname.data, 
      form.phone.data, form.country_id.data, form.email.data, form.password.data)
      db_session.add(g.newuser)
      db_session.commit()
      session['lastname'] = g.newuser.lastname
      session['firstname'] = g.newuser.firstname
      session['phone'] = g.newuser.phone
      session['country_id'] = g.newuser.country_id
      if g.newuser.country_id == 1:
        session['country_id'] = 'Nigerian'
      else:
        session['country_id'] = 'Foreigner'
      session['email'] = g.newuser.email           
      return redirect(url_for('welcome'))
  elif request.method == 'GET':
    return render_template('signup.html', form=form)


@app.route('/storedata', methods=['GET', 'POST'])
def storedata():
 form = TapeForm()
 if request.method == 'POST':
    if form.validate() == False:
      return render_template('storedata.html', form=form)
    else:
      g.post = db_session.query(User.id).filter(session['email'] == User.email).first()
      g.lastname = db_session.query(User.lastname).filter(session['email'] == User.email).first()
      g.firstname = db_session.query(User.firstname).filter(session['email'] == User.email).first()
      g.fullname = g.lastname + g.firstname  
      g.newuser = Tape(form.tape_number.data, form.project_title.data, form.content.data,
      form.status.data, user_id=g.post, author=g.fullname)
      db_session.add(g.newuser)
      db_session.commit()
      
      session['tape_number'] = g.newuser.tape_number
      session['project_title'] = g.newuser.project_title
      session['content'] = g.newuser.content
      session['status'] = g.newuser.status
      flash('New Entry was Successful')    
                       
      return redirect(url_for('storedata'))
   
 elif request.method == 'GET':
    import psycopg2
    conn = psycopg2.connect("dbname='mydatabase' user='trans' host='localhost' password='transformer'")
    cur = conn.cursor()
    cur.execute("""select tape_number, project_title, content, status, author, timestamp from tapes order by uid desc""")
    rows = cur.fetchall()
    entries = [dict(tape_number=row[0], project_title=row[1], content=row[2], author=row[3], timestamp=row[4]) for row in rows]
    return render_template('storedata.html', form=form, entries=entries)


@app.route('/updatedata', methods=['GET', 'POST'])
def updatedata():
 form = TapeForm()
 if request.method == 'POST':
    if form.validate() == False:
      return render_template('updatedata.html', form=form)
    else:
      g.post = db_session.query(User.id).filter(session['email'] == User.email).first()
      g.lastname = db_session.query(User.lastname).filter(session['email'] == User.email).first()
      g.firstname = db_session.query(User.firstname).filter(session['email'] == User.email).first()
      g.fullname = g.lastname + g.firstname  
      g.newuser = Tape(form.tape_number.data, form.project_title.data, form.content.data,
      form.status.data, user_id=g.post, author=g.fullname)
      db_session.add(g.newuser)
      db_session.commit()
      
      session['tape_number'] = g.newuser.tape_number
      session['project_title'] = g.newuser.project_title
      session['content'] = g.newuser.content
      session['status'] = g.newuser.status
      flash('New Entry was Successful')    
                       
      return redirect(url_for('updatedata'))
   
 elif request.method == 'GET':
    import psycopg2
    conn = psycopg2.connect("dbname='mydatabase' user='trans' host='localhost' password='transformer'")
    cur = conn.cursor()
    cur.execute("""select tape_number, project_title, content, status, author, timestamp from tapes order by uid desc""")
    rows = cur.fetchall()
    entries = [dict(tape_number=row[0], project_title=row[1], content=row[2], author=row[3], timestamp=row[4]) for row in rows]
    return render_template('updatedata.html', form=form, entries=entries)







@app.route('/welcome')
def welcome():
  return render_template('welcome.html')
  
if __name__ == '__main__':
  app.run(debug=True, use_reloader=False)

