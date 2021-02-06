import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

park = Blueprint('park', 'park')

@park.route('/', methods=["GET"])
def get_all_parks():
    ## find the dogs and change each one to a dictionary into a new array
    try:
        parks = [model_to_dict(park) for park in models.Park.select()]
        print(parks)
        return jsonify(data=parks, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@park.route('/', methods=["POST"])
def create_park():
    ## see request payload anagolous to req.body in express
    payload = request.get_json()
    try:
        park = models.Park.create(**payload)
        ## see the object
        print(park.__dict__)
        ## Look at all the methods
        print(dir(park))
        # Change the model to a dict
        print(model_to_dict(park), 'model to dict')
        park_dict = model_to_dict(park)
        return jsonify(data=park_dict, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error creating the park."})