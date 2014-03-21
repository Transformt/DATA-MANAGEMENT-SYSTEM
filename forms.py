from wtforms import Form, TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField, SelectField, FileField 
from flask_wtf import Form
from models import *

class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), 
  validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")
  
class SignupForm(Form):
  firstname = TextField("First name",  [validators.Required("Please enter your first name."),
  validators.length(min=5, max=15)])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name."), validators.length(min=3, max=15)])
  phone = TextField('Phone Number', [validators.Required('Please enter your mobile number'),  validators.length(min=11, max=15)])
  country_id = TextField('Country', [validators.Required('Please enter your country')])
  email = TextField("Email",  [validators.Required("Please enter your email address."), 
  validators.Email("Please enter your email address.")])
  password = PasswordField('Password', 
  [validators.Required("Please enter a password.")])
  confirm = PasswordField('Repeat Password', 
  [validators.Required("Please re-enter your password to confirm"), 
  validators.EqualTo('password', message='Passwords must match')])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("This email is already taken")
      return False
    else:
      return True
      
class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), 
  validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    userpass = User.query.filter_by(pwdhash = self.password.data.lower()).first()
        
    if user and userpass:
      user = User.query.filter_by(email = self.email.data.lower()).one()
      userpass = User.query.filter_by(pwdhash = self.password.data.lower()).one()
      
      if user == userpass:
        return True
      else:
        self.email.errors.append("Invalid e-mail or password")
        return False
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False
      

class TapeForm(Form):
  tape_number = TextField("Tape Number",  [validators.Required("Please enter tape number.")])
  project_title = TextField('Project Title', 
  [validators.Required("Please enter project title."), validators.length(min=5, max=20)])
  content = TextAreaField('Data Content', [validators.Required("Please Data Content cannot be empty.")])
  status = SelectField(u'status', choices=[('Used Tape', 'Used Tape'), (('Unused Tape', 'Unused Tape'))])
  submit = SubmitField("Save data")
  
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = Tape.query.filter_by(tape_number = self.tape_number.data.lower()).first()
    userpass = Tape.query.filter_by(project_title = self.project_title.data.lower()).first()
        
    if user:
      self.tape_number.errors.append("Data with this tape_number already exists in database")
      return False
    else:
      return True
    if userpass:
      self.project_title.errors.append("Data with this project_title already exists in database")
      return False
    else:
      return True

