#render_template is imported so that we can to refer to other files
#flash is imported so as to display alert messages
from flask import Flask, render_template,flash
#were importing this so that we would be able to create forms 
from flask_wtf import FlaskForm
#stringfield is imported so as to make input boxes, submitfield adds a submit button to your form
from wtforms import StringField, SubmitField
#Data required is a validator thats validate if the input box has an input
from wtforms.validators import DataRequired

#adding nav bar doesn't affect our code its just the html code we have to deal with

app=Flask(__name__)
#creating a secret key helps to protect users session, prevent hackers, and keep cookies
app.config['SECRET_KEY']="zenoid"

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
        flash("Form Submitted Successful!!!")
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
    app.run(debug=True) 
