#basic introduction
#render_template is used to make referrence to html files in your templates folders
from flask import Flask, render_template



#creating a flask instance
app = Flask(__name__)



#creating a route decorator
@app.route('/')
#def index():
#    return'<h1>Hello world<h1>'

def index():
    return render_template("index.html")

 
 #localhost:5000/user/John
@app.route('/user/<name>') #<name> indicates that when browsing it is the one ontop you will type
def user(name):
    return f'<h1>Hello {name} <h1>'



    
if __name__=='__main__':
    app.run(debug=True)