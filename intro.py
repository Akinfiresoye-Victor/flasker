#basic introduction
from flask import Flask



#creating a flask instance
app=Flask(__name__)

#creating a route decorator
#make sure youre app route is before the function, ('/') means homepage
@app.route('/')
def index():    
    return'<h1>Hello World<h1>'

    
if __name__=='__main__':
    app.run(debug=True)