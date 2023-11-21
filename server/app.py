from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_migrate import Migrate
from models import Cheese, Producer, db
from flask_restful import Api, Resource



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


#@app.route("/")
#def index():
 #   response = make_response({"message": "Hello Fromagers!"}, 200)
  #  return response
  
class ProducerResource(Resource):
    def get(self):
        producers = Producer.query.all()
        response_data = [producer.serialize() for producer in producers]
        return make_response(jsonify(response_data), 200)
    
    def get(self, producer_id):
        producer = Producer.query.get_or_404(producer_id)
        response_data = producer.serialize()
        return make_response(jsonify(response_data), 200)
    
    def delete(self, producer_id):
        producer = Producer.query.get_or_404(producer_id)
        db.session.delete(producer)
        db.session.commit()
        return make_response('', 204)
    
class CheeseResource(Resource):
    def post(self):
        data = request.get_json()
        
        try:
            producer_id = data["producer_id"]
            producer = Producer.query.get_or_404(producer_id)
        except KeyError:
            return make_response(jsonify({"error": "Invalid request, missing 'producer_id'"}), 400)
        
        cheese_data = {
            "kind": data["kind"],
            "is_raw_milk": data["is_raw_milk"],
            "production_date": data["production_date"],
            "image": data["image"],
            "price": data["price"],
            "producer": producer
        }
        
        cheese = Cheese(**cheese_data)
        
        db.session.add(cheese)
        db.session.commit()
        
        response_data = cheese.to_dict()
        return make_response(jsonify(response_data), 201)
    
    def patch(self, cheese_id):
        cheese = Cheese.query.get_or_404(cheese_id)
        data = request.get_json()
        
        try:
            cheese.is_raw_milk = data["is_raw_milk"]
            cheese.production_date = data["production_date"]
        except KeyError:
            return make_response(jsonify({"error": "Invalid request, missing 'is_raw_milk' or 'production_date'"}), 400)
        
        db.session.commit()
        response_data = cheese.serialize()
        return make_response(jsonify(response_data), 200)
    
    def delete(self, cheese_id):
        cheese = Cheese.query.get_or_404(cheese_id)
        db.session.delete(cheese)
        db.session.commit()
        return make_response('', 204)
    
api.add_resource(ProducerResource, '/producers', '/producers/<int:producer_id>')
api.add_resource(CheeseResource, '/cheeses', '/cheeses/<int:cheese_id>')


if __name__ == "__main__":
    app.run(port=5555, debug=True)
