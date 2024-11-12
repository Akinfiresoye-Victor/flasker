#render_template is imported so that we can to refer to other files
#flash is imported so as to display alert messages
from flask import Flask, render_template,flash,request
#were importing this so that we would be able to create forms 
from flask_wtf import FlaskForm
#stringfield is imported so as to make input boxes, submitfield adds a submit button to your form
from wtforms import StringField, SubmitField
#Data required is a validator thats validate if the input box has an input
from wtforms.validators import DataRequired
#Importing a library that uses flask to make database 
from flask_sqlalchemy import SQLAlchemy
#Importing datetime so as to be able to use time which they registered or entered
from datetime import datetime


#adding nav bar doesn't affect our code its just the html code we have to deal with

app=Flask(__name__)

#adding database to website
#URI-uniform resource indicator
#the value after the equal indicates the database engine(sqlite) the Separator(///), and the name of existing or new file(user.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#creating a secret key helps to protect users session, prevent hackers, and keep cookies
app.config['SECRET_KEY']="zenoid"
#initializing the database 
#SQLAlchemy is used to like connect flask applications and database together
db=SQLAlchemy(app)



#creating model it is basically used for creating the tables 
class Users(db.Model):
    #note the Column,String, DateTime is case sensitive
    #id indicates the the number of the data inputed then db.integer indicates that the id number will be an integer
    id = db.Column(db.Integer, primary_key=True)
    #this indicates the field setting it to a string format with the maximum length to be 200words nullable=false means that the field cant to be empty 
    name=db.Column(db.String(200), nullable=False)
    #unique=True because we dont want 2 or more different email
    email=db.Column(db.String(120), nullable=False,unique=True)
    #db.datetime is used for inputting date and time if you want it to be inputed automatically we use default=......
    date_added=db.Column(db.DateTime, default=datetime.utcnow)


#repr short for representation it is used for converting the objects to string
def __repr__(self):
    return f"<name'{self.name}'>"
#creating an application context for the flask app like creating the database
with app.app_context():
    #initializes all the tables created in the code so it basically creates all
    db.create_all()

#creating the database form to fill out remember FlaskForm is used for creating form like pages
class UserForm(FlaskForm):
#were assigning an input box with a label into the variable name and creating a validator to validate the input box    
    name = StringField(("Name"), validators=[DataRequired()])
    email = StringField(("Email"), validators=[DataRequired()])
#assigning a submit buttton to the variable submit
    submit = SubmitField("Submit")

#creating series of code to be able to update our database, <int:id>is passed into the url so as to look for where the record is
@app.route('/update/<int:id>', methods=['GET','POST'])
#the argument id will get the id in the url and bring it into the function
def update(id):
    #assigning the class to a variable form
    form=UserForm()
    #searches for an id from the table(user) thats searches and filters whats in the database(query) if none is found error occurs(404.error)
    name_to_update=Users.query.get_or_404(id)
#creating a loop that checks if somebody went to the page
#this request==post sends the thing you searched for to the url to search for     
    if request.method  == "POST":
#name represents the user name while name_to.. represent the variable holding it,request.form helps to retrieve the name submitted 
        name_to_update.name=request.form['name']
#same as email               
        name_to_update.email=request.form['email']
#creating a try except short program to show what will happen if an error occurred while updating the database        
        try:
#since the database is saved db.commit actually saves the new changes added to the database always use it if changes are made            
            db.session.commit()
            flash("User updated successfully")
            return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update)
        except:
            flash("Error looks like theres a problem..... try again!!")
            return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update)
#if a request isn't posted it wouldn't leave the page            
    else:
        return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update)
                    
#namerform is a class that inherits the attribute of flask form the class handles data, validates, protect, and integrates flask route and templates
class NamerForm(FlaskForm):
#were assigning an input box with a label into the variable name and creating a validator to validate the input box    
    name = StringField(("What's your name?"), validators=[DataRequired()])
#assigning a submit buttton to the variable submit
    submit = SubmitField("Submit")
@app.route('/')
def index(): 
    first_name='Victor'
    pizza=['mushrom', 'pepperoni', 30]
    stuff='this is a <strong>bold</strong> text'
    return render_template("index.html",
                           first_name=first_name,
                           pizza=pizza,
                           stuff=stuff)

#creating a link for the database
@app.route('/user/add', methods=['GET', 'POST'])
#note that Users is the class that contains the table in the database
def add_user():
    #making the input box empty
    name=None
    #assigning the class UserForm to the var form
    form = UserForm()
    #telling the code what will happen after the form has been submitted
    if form.validate_on_submit():
#creating a query(performs a search) that finds which email that matches the email on the database and brings out the first matching email if no user is found it returns none
          user = Users.query.filter_by(email=form.email.data).first()
#if none is found we add the name and email to the database          
          if user is None:
              #extracting the name and email and assigning it to the variable user
              user=Users(name=form.name.data, email=form.email.data)
              #submitting the name and email
              db.session.add(user)
              #committing what we've added
              db.session.commit()
          name=form.name.data
          form.name.data=''
          form.email.data=''
          flash('User added successfully')  
#creates a query on the table then arranging it(order_by) by the date added(Users.date_added), it can be arranged anyhow also           
    our_users=Users.query.order_by(Users.date_added)      
    return render_template("add_user.html", 
                           form =form,
                           name=name,
                           our_users=our_users)

#creating a function thats is based on submitting and generating the result
#methods=get and post means it would retrieve the data from the server THEN SUBMITS THE DATA(name inputed) TO THe server
@app.route('/name', methods=['GET', 'POST'])
def name():
    #name = none means there shouldnt be any data in the input field
    name= None
    #assigning the class NamerForm to the variable form
    form = NamerForm()
    #.validate_on_submit is a method that checks if the form is submitted and is valid
    if form.validate_on_submit():
    #if it is valid we assign the data we submitted in the input box to the variable name    
        name =form.name.data
    #after submitting we then reset the input box    
        form.name.data =''
    #flash messages are like alert so we just put what ww want to say    
        flash(" Submitted Successful!!!")
    return render_template('name.html', name=name, form=form)  
  
@app.route('/user/<name>')
#the argument name is given because we want to pass the name from the url into the function so as to make use of it in the function
def user(name):
    return render_template("user.html", name=name)
#app.errorhandler(status code) , error handler helps register an error handler for the status code
# e the argument representing a function parameter representing an error exception
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
    


if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 
#now to activate the database from your terminal 👇
#python, from 'application_name' import app, db
#with app.app_context():
    #db.create_all()
    #press enter
#exit()    