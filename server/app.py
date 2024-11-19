#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants_to_dict = [p.to_dict() for p in Plant.query.all()]
        response = make_response(
            plants_to_dict,
            200
        )
        return response
    
    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data.get('name'),
            image=data.get('image'),
            price=data.get('price')
        )
        db.session.add(new_plant)
        db.session.commit()

        response_dict = new_plant.to_dict()
        response = make_response(
            response_dict,
            201
        )
        
api.add_resource(Plants, '/plants')
        
class PlantByID(Resource):
    def get(self, id):
        # Retrieve the plant by ID
        plant = Plant.query.get(id)

        # Check if the plant exists
        if plant is None:
            return make_response({'error': 'Plant not found'}, 404)

        # Convert the plant object to a dictionary
        plant_dict = plant.to_dict()

        # Create a response with the plant data
        response = make_response(
            plant_dict,
            200
        )
        return response

api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
