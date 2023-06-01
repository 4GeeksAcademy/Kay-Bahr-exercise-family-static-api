"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_get_all_members():

    members = jackson_family.get_all_members()
        
    if len(members) == 0:
        # If there are no members in the database, return 404 Not Found
        raise APIException('No members found', status_code=404)

    return jsonify(members), 200



@app.route('/member/<int:id>', methods=['GET'])
def handle_get_member(id):

    member = jackson_family.get_member(id)
    if member is None:
        raise APIException('Member not found', status_code=404)

    return jsonify(member), 200


@app.route('/member', methods=['POST'])
def handle_add_member():
    member = request.get_json()

    if member is None:
        raise APIException("You need to specify the request body as a JSON object", status_code=400)
    if 'first_name' not in member:
        raise APIException('You need to specify the first name', status_code=400)
    if 'age' not in member:
        raise APIException('You need to specify the age', status_code=400)
    if 'lucky_numbers' not in member:
        raise APIException('You need to specify the lucky numbers', status_code=400)

    jackson_family.add_member(member)

    return jsonify(member), 200

@app.route('/member/<int:id>', methods=['PUT'])
def handle_update_member(id):
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a JSON object", status_code=400)
    if 'first_name' not in body:
        raise APIException('You need to specify the first name', status_code=400)
    if 'age' not in body:
        raise APIException('You need to specify the age', status_code=400)
    if 'lucky_numbers' not in body:
        raise APIException('You need to specify the lucky numbers', status_code=400)

    member = jackson_family.get_member(id)
    if member is None:
        raise APIException('Member not found', status_code=404)

    member.first_name = body['first_name']
    member.age = body['age']
    member.lucky_numbers = body['lucky_numbers']

    return jsonify(member), 200
    
@app.route('/member/<int:id>', methods=['DELETE'])
def handle_delete_member(id):
    member = jackson_family.get_member(id)
    if member is None:
        raise APIException('Member not found', status_code=404)

    jackson_family.delete_member(id)
    return jsonify({"done": True}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
