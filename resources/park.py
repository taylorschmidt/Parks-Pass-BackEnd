import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

park = Blueprint('park', 'park')

@park.route('/all', methods=["GET"])
def get_all_parks():
    ## find the parks and change each one to a dictionary into a new array
    try:
        parks = [model_to_dict(park) for park in models.Park.select()]
        print(parks)
        return jsonify(data=parks, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@park.route('/', methods=["GET", "POST"])
def findOrCreatePark():
    payload = request.get_json()
    try:
        park = models.Park.get((models.Park.park_code == payload['park_code']))
        park_dict = model_to_dict(park)
        return jsonify(data=park_dict, status={"code": 200, "message": "Success finding that park."})
    except models.Park.DoesNotExist:
        newPark = models.Park.create(**payload)
        new_park_dict = model_to_dict(newPark)
        return jsonify(data=new_park_dict, status={"code": 201, "message": "Success creating that park."})
