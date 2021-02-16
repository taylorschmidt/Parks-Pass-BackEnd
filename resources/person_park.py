import models
from peewee import *
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

person_park = Blueprint('person_park', 'person_park')

@person_park.route('/', methods=["POST"])
def create_person_park():
    payload = request.get_json()
    #payload should have person_id and visited_park_id
    try:
        if current_user.id:
            query = models.PersonPark.get(models.PersonPark.visited_park_id == payload['visited_park_id'], models.PersonPark.person_id == payload['person_id'])
            return jsonify(data={},\
                       status={"code": 401,\
                               "message": "A park relationship with that user already exists."})
    except models.DoesNotExist:
        person_park = models.PersonPark.create(**payload)
        pp_dict = model_to_dict(person_park)
            #create the relationship between dog and user 
        return jsonify(data=pp_dict, status={"code": 201, "message": "Created"})

@person_park.route('/visited', methods=["GET", "POST"])
def get_person_park_visits():
    payload = request.get_json()
    #payload should just have user's email address
    try:
        query = (models.Park.select().join(models.PersonPark).join(models.Person).where(models.Person.email == payload['email']))
        pp_dict = [model_to_dict(item) for item in query]
        return jsonify(data=pp_dict, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message":"Username or password is incorrect."})

#Run below in sql shell to see joins
#SELECT * FROM person INNER JOIN personpark ON person.id = personpark.person_id INNER JOIN park on personpark.visited_park_id = park.id;

@person_park.route('/visited/delete', methods=['GET', 'POST'])
def delete_person_park_visit():
    payload = request.get_json()
    #payload should have person_id and visited_park_id
    try:
        park_person = models.PersonPark.get(**payload)
        park_person.delete_instance()
        pp_dict = model_to_dict(park_person)
        return jsonify(data=pp_dict, status={"code": 200, "message": "Successfully deleted."})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message":"Username or password is incorrect."})
