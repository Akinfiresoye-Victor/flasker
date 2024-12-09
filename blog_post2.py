#render_template is imported so that we can to refer to other files
#flash is imported so as to display alert messages
from flask import Flask, render_template,flash,request, redirect, url_for
#were importing this so that we would be able to create forms 
#Importing a library that uses flask to make database 
from flask_sqlalchemy import SQLAlchemy
#Importing another library that is used when we make changes to our database, it must be after SQLAlchemy
from flask_migrate import Migrate
#Importing datetime so as to be able to use time which they registered or entered
from datetime import datetime, date
#importing a library for the use of password and user authentication in our database
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import LoginForm, PostForm, UserForm, PasswordForm, NamerForm, SearchForm
from flask_ckeditor import CKEditor

#adding nav bar doesn't affect our code its just the html code we have to deal with

app=Flask(__name__)
#add ckeditor
ckeditor=CKEditor(app)
#adding database to website
#URI-uniform resource indicator
#the value after the equal indicates the database engine(sqlite) the Separator(///), and the name of existing or new file(user.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#creating a secret key helps to protect users session, prevent hackers, and keep cookies
app.config['SECRET_KEY']="zenoid"
#initializing the database 
#SQLAlchemy is used to like connect flask applications and database together
db=SQLAlchemy(app)
#were telling the code to like accept the changes made in the database
migrate= Migrate(app, db)

#flask things for logging in to user
#were assigning the class of login manager to a variable so we can easy access it

#Password initiation
login_manager=LoginManager()
#since app is the name of the flask application we need to like input or infuse login manager to the app(initialize it)
login_manager.init_app(app)
#this makes the webpage act or behave like a normal login page
login_manager.login_view= 'login'


#used to verify the user and load them
@login_manager.user_loader
#creating a function that retrives an entire users data using a their id its basically used for dealing with authentication  
def load_users(user_id):
#it queries the entire database and gets the integer of the id
    return Users.query.get(int(user_id))



#B(ZpJ6sEeGc&j7j


@app.route('/login', methods=['GET', 'POST'])
def login():
#assigning the class LoginForm to the variable form     
    form= LoginForm()
    if form.validate_on_submit():
        #were querying the database looking for the first username stored in the database meaning were actually validated in that aspect
        user= Users.query.filter_by(username=form.username.data).first()
#we want to check the password of the username if its correct        
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Logged in successfully!!')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong Password try again')
        else:
            flash('Username not found please try again')            
    return render_template('login.html', form=form)

#creating a logout function


@app.route('/logout', methods=['GET', 'POST'] )
@login_required
def logout():
    logout_user()
    flash('You have been logged out thanks for stopping by')
    return redirect(url_for('login'))



    

@app.route('/dashboard', methods=['GET', 'POST'])
#once this is put we cant go here until we can login
@login_required
def dashboard():   
    #assigning the class to a variable form
    form=UserForm()
    id= current_user.id
    #searches for an id from the table(user) thats searches and filters whats in the database(query) if none is found error occurs(404.error)
    name_to_update=Users.query.get_or_404(id)
#creating a loop that checks if somebody went to the page
#this request==post sends the thing you searched for to the url to search for     
    if request.method  == "POST":
#name represents the user name while name_to.. represent the variable holding it,request.form helps to retrieve the name submitted 
        name_to_update.name=request.form['name']
#same as email               
        name_to_update.email=request.form['email']
        
        name_to_update.favorite_color=request.form['favorite_color']
        
        name_to_update.username=request.form['username']
#creating a try except short program to show what will happen if an error occurred while updating the database        
        try:
#since the database is saved db.commit actually saves the new changes added to the database always use it if changes are made            
            db.session.commit()
            flash("User updated successfully")
            return render_template('dashboard.html',
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)
        except:
            flash("Error looks like theres a problem..... try again!!")
            return render_template('dashboard.html',
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)
#if a request isn't posted it wouldn't leave the page            
    else:
        return render_template('dashboard.html',
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)    
    


#creating a blog post model like a class
class Post(db.Model):
#we need an id so that we will be able to identify each blog post which will make its management easy    
    id =  db.Column(db.Integer, primary_key=True)
#we need a title for the blog post    
    title= db.Column(db.String(255))
#we also need the content or description of the blog posted text is used to make paragraph of text not straight line(strings) of text    
    content= db.Column(db.Text)
#we need to know who made the post    
    #author= db.Column(db.String(200))
    date_posted= db.Column(db.DateTime, default=datetime.utcnow)
#creating a form of url so that we would be able to see what we searched for its called slug    
    slug= db.Column(db.String(255))
#creating a foreign key to link users(referring to the primary key of the user)
#db.foreignkey is used when creating a foreign key, users.id is used to reference the id of the class User, it is lowercase because we want to query the class so in summary when dealing with foreign key a lowercase is used
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
 

#creating an app route that directs the user to a particular post so were using the id to locate the particular blog post
@app.route('/posts/<int:id>') 
#creating a function and passing the id in the route to the function to generate the id
def post(id):
#querying each aspect and bringing out or generating the id from it      
    post= Post.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_post(id):
    post=Post.query.get_or_404(id)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content= form.content.data
        post.slug= form.slug.data
        db.session.add(post)
        db.session.commit()
        flash('Blog has been updated') 
        return redirect(url_for('post', id=post.id))
    if current_user.id== post.poster_id:
        form.title.data= post.title
        form.content.data=post.content
        form.slug.data=post.slug
        return render_template('edit_post.html', form=form)
    else:
        flash("You aren't Authorized to edit this post")
        posts= Post.query.order_by(Post.date_posted)
        return render_template('posts.html',posts=posts)
        
@app.route('/posts')
def posts():
#trying to gather all the post sent to the database
    posts= Post.query.order_by(Post.date_posted)
    return render_template('posts.html',posts=posts)
@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    blog_to_delete= Post.query.get_or_404(id)
    id= current_user.id
    if  id== blog_to_delete.poster.id:
            
        try:

            db.session.delete(blog_to_delete)
            db.session.commit()
            flash('Blog has been deleted successfully.....')
            posts= Post.query.order_by(Post.date_posted)     
            return render_template('posts.html',posts=posts)

        except:
            flash('oops there was an error try again....')
            return render_template("posts.html", posts=posts)

    else: 
        posts= Post.query.order_by(Post.date_posted)
        flash("You aren't Authorized to delete that post")
        return render_template("posts.html", posts=posts)


#add post page
@app.route('/add-post',methods=['GET','POST'])
@login_required
def add_post():
    
    form = PostForm()
    
    if form.validate_on_submit():
        poster= current_user.id
        post= Post(title=form.title.data,
                   content=form.content.data,
                   poster_id=poster,
                   slug=form.slug.data)
        form.title.data= ''
        form.content.data= ''
       # form.author.data= ''
        form.slug.data= ''
#adding data to db
        db.session.add(post)
        db.session.commit()
        
        flash('Blog has been posted successfully!')
    return render_template("add_post.html", form=form)        
    



#no matter the quotation you use its still double quote that will be in the output asper json
#json(javascript object notation) thing a json is a file that contains data structures they are easy to write and read
@app.route('/date')
def get_current_date():
    favorite_pizza={
        'John': "Pepperoni",
        "Mary": "Cheese",
        "Tim": "Mushroom"
    }
    return(favorite_pizza)
    #return {"Date": date.today()}

@app.context_processor
def base():
    form = SearchForm()
    return dict(search_form=form)



#creating a url for the search bar that accepts things posted from the webpage then the function processes it    
@app.route('/search', methods=["POST"])
def search():
    form=SearchForm()
    if form.validate_on_submit():
        searched= form.searched.data
    #get data from the submitted form
        posts=Post.query.filter(Post.content.like('%' + searched +'%'))
        posts= posts.order_by(Post.title).all()
        
    #query the database

    return render_template("search.html", form=form, searched=searched,posts=posts)
    
    
    
#creating model it is basically used for creating the tables 
class Users(db.Model,UserMixin):
    #note the Column,String, DateTime is case sensitive
    #id indicates the the number of the data inputed then db.integer indicates that the id number will be an integer
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), nullable=False, unique=True)
    #this indicates the field setting it to a string format with the maximum length to be 200words nullable=false means that the field cant to be empty 
    name=db.Column(db.String(200), nullable=False)
    #unique=True because we dont want 2 or more different email
    email=db.Column(db.String(120), nullable=False,unique=True)
    #db.datetime is used for inputting date and time if you want it to be inputed automatically we use default=......
    date_added=db.Column(db.DateTime, default=datetime.utcnow)
    #trying to add something to the database
    favorite_color=db.Column(db.String(120))
    #doing password stuff
    password_hash = db.Column(db.String(128))
    #user can have many post we used capital P because were referencing the class not the database
    #poster is used so that we can easily reference e.g(poster.username) it just creates an imaginary column
    posts= db.relationship('Post', backref='poster')





    #creating an application context for the flask app like creating the database
    with app.app_context():
        #initializes all the tables created in the code so it basically creates all
        db.create_all()
    #property is used when dealing with passwords
    @property
    #creating  functions that will convert set of passwords to hash then checks if the hash password set is correct
    #self is passed so that other functions to can inherit from the function
    def password(self): 
        #if something goes wrong with the password it flashes the readable message...👇
        raise AttributeError('password is not a readable attribute!!!')

    #password setter is used for setting  values to something in this case we want to set the password to hash
    @password.setter
    #creating a function that converts the password entered into an hashed one
    #self and password is passed so that it would inherit the function password
    def password(self, password):
    #were telling the application to take the password inputed in the column and convert it into hashes    
        self._password_hash = generate_password_hash(password)
    #creating a function that checks if the password converted to hashtag is correct    
    def verify_password(self, password):
    #would return true if the password is correct meaning it goes to the next page since we use validators
        return check_password_hash(self._password_hash, password)
        #repr short for representation it is used for converting the objects to string
    def __repr__(self):
        return f"<name'{self.name}'>"
#<int:id> was passed in the route because d id will obviously be an integer(int)     
@app.route('/delete./<int:id>')    
def delete(id):
#this line will query(sample) the database then find the one that matches the id then it assigns it to the variable
    user_to_delete=Users.query.get_or_404(id)
#if the particular id quarried is found it will try     
    try:
        name=None
    #assigning the class UserForm to the var form
        form = UserForm()
    #telling the database what we want to delete which is (user_to_delete)    
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User deleted successfully!!!')
        #we want our table of saved users to show
        our_users=Users.query.order_by(Users.date_added)
#after deleting it will return to the normal page instead of going to an error page 
        return render_template("add_user.html", 
                           form =form,
                           name=name,
                           our_users=our_users)  
#if there was an error do this👇  
    except:   
        flash('oops...There was an issue deleting the user please try again')     
        return render_template("add_user.html", 
                           form =form,
                           name=name,
                           our_users=our_users) 
    

#creating series of code to be able to update our database, <int:id>is passed into the url so as to look for where the record is
@app.route('/update/<int:id>', methods=['GET','POST'])
@login_required
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
        
        name_to_update.favorite_color=request.form['favorite_color']
        
        name_to_update.username=request.form['username']
#creating a try except short program to show what will happen if an error occurred while updating the database        
        try:
#since the database is saved db.commit actually saves the new changes added to the database always use it if changes are made            
            db.session.commit()
            flash("User updated successfully")
            return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)
        except:
            flash("Error looks like theres a problem..... try again!!")
            return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)
#if a request isn't posted it wouldn't leave the page            
    else:
        return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)
                    
#namerform is a class that inherits the attribute of flask form the class handles data, validates, protect, and integrates flask route and templates
   
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
        #hashing the password
        hashed_pw = generate_password_hash(form.password_hash.data, "pbkdf2:sha256")
#creating a query(performs a search) that finds which email that matches the email on the database and brings out the first matching email if no user is found it returns none
        user = Users.query.filter_by(email=form.email.data).first()
#if none is found we add the name and email to the database          
        if user is None:
              #extracting the name and email and assigning it to the variable user
              user=Users(username= form.username.data,name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
              #submitting the name and email
              db.session.add(user)
              #committing what we've added
              db.session.commit()
        name=form.name.data
        #after it has been added it sets the input box empty
        form.name.data=''
        form.username.data=''
        form.email.data=''
        form.favorite_color.data=''
        form.password_hash = ''
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
    
#creating a website for logging in
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    #name = none means there shouldnt be any data in the input field
    email= None
    password = None
    pw_to_check = None
    passed = None
    form= PasswordForm()
    #assigning the class NamerForm to the variable form
    #.validate_on_submit is a method that checks if the form is submitted and is valid
    if form.validate_on_submit():
    #if it is valid we assign the data we submitted in the input box to the variable name    
        email =form.email.data
        password =form.password_hash.data
    #after submitting we then reset the input box    
        form.email.data =''
        form.password_hash.data =''
        
        pw_to_check = Users.query.filter_by(email=email).first()
        passed=check_password_hash(pw_to_check.password_hash, password)
        
    #flash messages are like alert so we just put what ww want to say    
    return render_template('test_pw.html', email=email, password=password,pw_to_check=pw_to_check ,passed=passed, form=form) 

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 

#to test the code
#python -m flask -app password_database.py shell
#from password_database import Users
#u=Users()
#u.password='your desired password'
#u.password (will return what u raised)
#u._password_hash (will return series of code)
#print(u.verify_password('your password'))(returns true if correct and false if 