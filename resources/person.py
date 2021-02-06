import models

from flask import Blueprint, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user

from playhouse.shortcuts import model_to_dict

person = Blueprint('person', 'person')

@person.route('/register', methods=["POST"])
def register():
    payload = request.get_json()
    print(payload, "!!!!!!!!!!!!!!!")
    # make the inputted email lowercase
    payload['email'].lower()

    try:
        # does the user already exist/is the username taken?
        # is there a user in the database whose email matches the one in our payload?
        models.Person.get(models.Person.email == payload['email'])
        return jsonify(data={},\
                       status={"code": 401,\
                               "message": "A user with that email already exists."})
    except models.DoesNotExist:
        # if the user does not already exist, create a user
        # like counter = counter + 1 - we are overwriting the original payload password with the hashed password
        payload['password'] = generate_password_hash(payload['password'])
        person = models.Person.create(username=payload['username'], password=payload['password'], email=payload['email'])
        login_user(person)
        person_dict = model_to_dict(person)
        del person_dict['password'] # don't expose password!
        return jsonify(data=person_dict, status={"code": 201, "message": "Successfully registered."})

@person.route('/login', methods=["POST"])
def login():
    #payload should contain email and password
    payload = request.get_json()
    # make the inputted email lowercase
    payload['email'].lower()
    try:
        # see if user is registered
        person = models.Person.get(models.Person.email == payload['email'])
        person_dict = model_to_dict(person)
        if(check_password_hash(person_dict['password'], payload['password'])):
            del person_dict['password']
            login_user(person)
            return jsonify(data=person_dict, status={"code": 200, "message":"Success"})
        else:
            return jsonify(data={}, status={"code": 401, "message":"Username or password is incorrect."})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message":"Username or password is incorrect."})

@person.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    return jsonify(data={}, status={"code": 200, "message": "Successful logout!"})



