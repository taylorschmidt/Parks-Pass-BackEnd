# https://parkspassport-api-heroku.herokuapp.com/

from flask import Flask, request, jsonify, g, session
from flask_session import Session
from redis import Redis
from flask_cors import CORS
from flask_login import LoginManager
from flask_redis import Redis

import os 

import models
from resources.park import park
from resources.person import person
from resources.person_park import person_park



# instantiate the app
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'redis'
app.config['SECRET_KEY'] = 'fignewton'
app.config.from_pyfile('config.py')
redis = Redis()
redis.init_app(app)
sess = Session()
sess.init_app(app)



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
    g.user = current_user
    g.db.connect()


@app.after_request
def after_request(response):
    g.db = models.DATABASE
    g.db.close()
    return response


@app.route('/')
def hello_world():
    return 'hello this flask app is working'



CORS(app,\
     origins=['http://localhost:3000', 'https://parks-passport.herokuapp.com'],\
     supports_credentials=True)

app.register_blueprint(park, url_prefix='/api/v1/park')
app.register_blueprint(person, url_prefix='/api/v1/user')
app.register_blueprint(person_park, url_prefix='/api/v1/person_park')
CORS(park)
CORS(person)
CORS(person_park)

if 'ON_HEROKU' in os.environ:
    app.secret_key = 'fignewton'
    print('hitting ')
    models.initialize()

if __name__ == '__main__':
    app.secret_key = 'fignewton'
    models.initialize()
    app.run(port=8000, debug=True)