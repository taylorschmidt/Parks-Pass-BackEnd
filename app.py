# https://parkspassport-api-heroku.herokuapp.com/

from flask import Flask, request, jsonify, g, session, make_response
from flask_session import Session
from redis import Redis
from flask_cors import CORS
from flask_login import LoginManager
from flask_redis import Redis
import redis
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

app.config['SECRET_KEY'] = 'fignewton'
app.config.from_pyfile('config.py')
app.config['SESSION_TYPE'] = 'redis'
REDISCLOUD = os.environ.get('REDISCLOUD_URL')
app.config['SESSION_REDIS'] = redis.from_url(REDISCLOUD)
app.config['SESSION_COOKIE_NAME'] = 'my_cookie'
app.config['SESSION_COOKIE_HTTPONLY'] = False
session_cookie = SecureCookieSessionInterface().get_signing_serializer(app)
sess = Session()
sess.init_app(app)
session_cookie = SecureCookieSessionInterface().get_signing_serializer(app)


# create our session secret key
app.config.from_pyfile('config.py')


login_manager = LoginManager() # in JS -- const loginManager = new LoginManager()
login_manager.init_app(app) # initialize the new LoginManager instance in our app


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.Person.get_by_id(user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    # same_cookie = session_cookie.dumps(dict(session))
    response.headers.add("Set-Cookie", f"my_cookie='a cookie'; Secure; HttpOnly; SameSite=None; Path=/;")
    g.db = models.DATABASE
    g.db.close()
    return response


@app.route('/')
def hello_world():
    resp = make_response('Hello, World!')
    resp.set_cookie('cookie1', 'value1', samesite='Lax')
    resp.set_cookie('cookie2', 'value2', samesite='None', secure=True)
    return 'hello this flask app is working'



CORS(app,\
     origins=['http://localhost:3000', 'https://parks-passsport-6mwnb5a4i-taylorschmidt.vercel.app/'],\
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
    app.secret_key = 'fignewton'
    models.initialize()
    app.run(port=8000, debug=True)