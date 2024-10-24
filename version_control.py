#basic introduction
from flask import Flask, render_template



#creating a flask instance
app = Flask(__name__)



#creating a route decorator
@app.route('/')
#def index():
#    return'<h1>Hello world<h1>'

def index():
    first_name='victor'
    pizza=['pepperoni','cheeze', 41]
#without using safe the strong function will just be printed out as a text \
#while using striptags it would just cancel out the function totally   
#you caN USE OTHER VARIABLES    
    stuff='This is bold text'
    return render_template("index.html",first_name=first_name,
                           stuff=stuff,
                           pizza=pizza)

 
 #localhost:5000/user/John
 
#user_name=name is getting name which is from the argument in the function and then the argument is getting the name from the app.route
@app.route('/user/<name>') 
def user(name):
    return render_template("user.html", user_name=name)


#creating custom error pages
#invalid url
@app.errorhandler(404)
def page_not_found(e):
     return render_template("404.html"), 404

#internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
  
  
    
if __name__=='__main__':
    app.run(debug=True)