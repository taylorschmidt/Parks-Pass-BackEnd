# https://parkspassport-api-heroku.herokuapp.com/

from flask import Flask, request, jsonify, g, session
from flask_session import session
from redis import Redis
from flask_cors import CORS
from flask_login import LoginManager

import os 

import models
from resources.park import park
from resources.person import person
from resources.person_park import person_park

sess = Session()

# instantiate the app
app = Flask(__name__)
SESSION_TYPE = 'redis'SESSION_REDIS = Redis(host="parkspassport-api-heroku.herokuapp.com", port=8080)
app.config.from_object(__name__)



# create our session secret key
app.config.from_pyfile('config.py')


login_manager = LoginManager() # in JS -- const loginManager = new LoginManager()
login_manager.init_app(app) # initialize the new LoginManager instance in our app
sess.init_app(app)

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
    g.db.close()
    return response


@app.route('/')
def hello_world():
    session['trial'] = 'working'
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
    print('hitting ')
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(port=8000, debug=True)