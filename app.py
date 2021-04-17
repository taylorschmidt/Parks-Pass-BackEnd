from flask import Flask, request, jsonify, g, session, make_response
from flask_session import Session
from flask_cors import CORS
from flask_login import LoginManager
from flask.sessions import SecureCookieSessionInterface
from playhouse.db_url import connect
import os 
import models
from resources.park import park
from resources.person import person
from resources.person_park import person_park

from datetime import timedelta


# instantiate the app
app = Flask(__name__)
app.config.from_pyfile('config.py')


login_manager = LoginManager() # in JS -- const loginManager = new LoginManager()
login_manager.init_app(app) # initialize the new LoginManager instance in the app


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.Person.get_by_id(user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
    response.headers.add("Set-Cookie", f"my_cookie='a cookie'; Secure; SameSite=None;")
    g.db = models.DATABASE
    g.db.close()
    return response


@app.route('/')
def hello_world():
    resp = make_response('Hello, World!')
    return 'hello this flask app is working'


CORS(app,\
     origins=['http://localhost:3000', 'https://parks-passsport.vercel.app', 'https://parkspassport-api-heroku.herokuapp.com/'],\
     supports_credentials=True)

app.register_blueprint(park, url_prefix='/api/v1/park')
app.register_blueprint(person, url_prefix='/api/v1/user')
app.register_blueprint(person_park, url_prefix='/api/v1/person_park')
CORS(park)
CORS(person)
CORS(person_park)

if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(port=8000, debug=True)