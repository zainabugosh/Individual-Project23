from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import requests,json

# API Setup Start


api_key = "7e934e93"


# api_url="https://futdb.app/api/players"
# API Setup End


# Flask & Firebase Setup Start
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  'apiKey': "AIzaSyB1zMOV8ELwQ589KrjKGLIrCJgRGxD6mjc",
  'authDomain': "meet-project-375716.firebaseapp.com",
  'projectId': "meet-project-375716",
  'storageBucket': "meet-project-375716.appspot.com",
  'messagingSenderId': "596759962974",
  'appId': "1:596759962974:web:f928acd8e88ae706045bcf",
  'measurementId': "G-C0DLNCH67M",
  "databaseURL": "https://meet-project-375716-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()
# Flask & Firebase Setup End


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
		bio=request.form['bio']
		Username=request.form['Username']
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			user={'name':Username,'email':email,'bio':bio,'password':password}
			UID = login_session['user']['localId']
			db.child("Users").child(UID).set(user)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
			print(error)
	return render_template("signup.html")

@app.route('/all_tweets')
def tweeta():
	tweeta=db.child("tweets").get().val(	)
	return render_template("tweets.html",tweeta=tweeta)


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	if request.method == 'POST':
		tex=request.form["text"]
		title=request.form["title"]
		
		try:
			UID = login_session['user']['localId']
			tweet={'uid':UID,'text':tex,"titel":title}
			db.child("tweets").push(tweet)
		except:
			return redirect(url_for('add_tweet'))
	return render_template("add_tweet.html")

@app.route('/search',methods=['GET','POST'])
def search():
	if request.method == "POST":
		result = request.form["searchap"]
		db.child("searches").push({"text":result})
		info = (get_movie_details(result))
		return render_template('result.html', info=info)
	return render_template('search.html')


def get_movie_details(name):
	api_link = f"https://www.omdbapi.com/?apikey={api_key}&t={name}"
	response = requests.get(api_link)
	print(response.json())
	return response.json()


if __name__ == '__main__':
	app.run(debug=True)