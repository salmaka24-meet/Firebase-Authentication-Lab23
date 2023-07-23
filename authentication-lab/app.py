from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = 
{
  "apiKey": "AIzaSyB2td2uBNmfsogRoKzMg2yWMcaD2E01s8Y",
  "authDomain": "salmameet1.firebaseapp.com",
  "projectId": "salmameet1",
  "storageBucket": "salmameet1.appspot.com",
  "messagingSenderId": "14714305978",
  "appId": "1:14714305978:web:faaaf238b40626559af183",
  "measurementId": "G-ZDWLMK23JL" ,
  "databaseURL": " "  
}

firebase = pyrebase.intialize_app(config)
auth = firebase.auth()

app=Flask(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
           return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"

    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
    return render_template("signup.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)