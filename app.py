import pyrebase
from flask import Flask , render_template
from flask import request

app = Flask(__name__)


config = {
    "apiKey": "AIzaSyBggxfJDtU4lcLAp4nq3DFOmMEIkwrLMiE",
    "authDomain": "flaskapi-e720e.firebaseapp.com",
    "databaseURL": "https://flaskapi-e720e.firebaseio.com",
    "projectId": "flaskapi-e720e",
    "storageBucket": "flaskapi-e720e.appspot.com",
    "messagingSenderId": "285634665957",
    "appId": "1:285634665957:web:69b481519e7c32c28fe30c",
    "measurementId": "G-180LBHWG4C"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/', methods=['GET','POST'])
def hello_world():
    unsuccessful = 'Please check your informations'
    successful = 'Login successful'
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
         auth.sign_in_with_email_and_password(email,password)
         return render_template('new.html', s=successful)
        except:
         return render_template('new.html', us=unsuccessful)
    return render_template('new.html')


if __name__=='__main__':
    app.run()










#email = input('please enter your email \n')
#password = input('please enter your password \n')

#user = auth.create_user_with_email_and_password(email,password)
#user = auth.sign_in_with_email_and_password(email,password)
#auth.send_password_reset_email(email)
#auth.send_email_verification(user['idToken'])
#print(auth.get_account_info(user['idToken']))