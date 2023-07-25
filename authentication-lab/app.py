from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyB2td2uBNmfsogRoKzMg2yWMcaD2E01s8Y",
  "authDomain": "salmameet1.firebaseapp.com",
  "projectId": "salmameet1",
  "storageBucket": "salmameet1.appspot.com",
  "messagingSenderId": "14714305978",
  "appId": "1:14714305978:web:faaaf238b40626559af183",
  "measurementId": "G-ZDWLMK23JL" ,
  "databaseURL": "https://salmameet1-default-rtdb.europe-west1.firebasedatabase.app/"  
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db= firebase.database()

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
        fullname = request.form['fname']
        user = request.form['username']
        bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user ={"email":email, "fname": fullname, "username":user, "bio":bio }
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except Exception as e:
            print(e)
            error = "Authentication failed"

    return render_template("signup.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error = ""
    if request.method == 'POST':
        try:
            title = request.form['title']
            discription = request.form['discrip']
            UID = login_session['user']['localId']
            tweet = {"title":title, "discrip": discription, "uid":UID}
            db.child("Tweets").push(tweet)
            return render_template('add_tweet.html')
        except:
            error = "Authentication failed"
    return render_template("add_tweet.html")

@app.route('/all_tweets')
def all_tweets():
    tweets = db.child("Tweets").get().val()
    return render_template("all_tweets.html", tweets=tweets)


if __name__ == '__main__':
    app.run(debug=True)