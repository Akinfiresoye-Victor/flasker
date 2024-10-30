from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Creating a Flask instance
app = Flask(__name__)

# Creating a secret key
app.config['SECRET_KEY'] = "handsomeguy4"

# Creating a form class 
class NamerForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Creating a route decorator for the home page
@app.route('/')
def index():
    first_name = 'Victor'
    pizza = ['pepperoni', 'cheese', 41]
    # Without using 'safe', the string function will be printed as text
    stuff = 'This is bold text'
    return render_template("index.html", first_name=first_name, stuff=stuff, pizza=pizza)

# Creating a route for the name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()  # Correctly initialize the form here
    # Validate form submission
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''  # Clear the form field after submission
    return render_template('name.html', name=name, form=form)

# Creating a route for the user page
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

# Creating custom error pages
# Invalid URL (404 error)
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal server error (500 error)
@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

if __name__ == '__main__':
    app.run(debug=True)
