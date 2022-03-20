from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#will create a new instance of Flask and will call and store it in this variable. Later can call and run it.

# @app.route("/")
# #creating a route (endpoint)
# def hello():
#     return "Hey Flask"

# Must have base directory so that flask knows where to save table
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
# ^gives us a programmatic way of interacting with the database
ma = Marshmallow(app)
# ^allows us to have schema --> stucture to the database

CORS(app)


class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valueOne = db.Column(db.Integer, unique=False)
    valueTwo = db.Column(db.Integer, unique=False)
    valueAnswer = db.Column(db.Integer, unique=False)
    operation = db.Column(db.String, unique=False) #multiplicatin sum 
    # ^columns and data types

    def __init__(self, valueOne, operation, valueTwo, valueAnswer):
        self.valueOne = valueOne
        self.operation = operation
        self.valueTwo = valueTwo
        self.valueAnswer = valueAnswer

class CalculationSchema(ma.Schema):
    class Meta:
        fields = ('valueOne', 'operation', 'valueTwo', 'valueAnswer')
        # is there a way to add a column based on the operation button that was selected?

calculation_schema = CalculationSchema()
# ^a single guide schema
calculations_schema = CalculationSchema(many=True)
# ^a multiple guides schema




#Endpoint to create a new calculation
@app.route('/calculation', methods=["POST"])
#^anytime you want to create something in the database
def add_calculation():
    print(request.get_json())
    valueOne = request.json['valueOne']
    # ^will get this object and then be able to parse it
    operation = request.json['operation']
    valueTwo = request.json['valueTwo']
    valueAnswer = request.json['valueAnswer']

    new_calculation = Calculation(valueOne, operation, valueTwo, valueAnswer)

    db.session.add(new_calculation)
    # ^creates a new database session and adds a new guide inside of it

    db.session.commit()

    calculation = Calculation.query.get(new_calculation.id)

    return calculation_schema.jsonify(calculation)





# Endpoint to query all calculations
@app.route('/calculations', methods=["GET"])
def get_calculations():
    all_calculations = Calculation.query.all()
    # ^will bring back all of the guides in the system
    result = calculations_schema.dump(all_calculations)
    return jsonify(result)
    # video says result.data (in v3.0 no need to call data, dump already calls data)





# Endpoint for querying a single calculation
@app.route("/calculation/<id>", methods=["GET"])
def get_calculation(id):
    #note that we pass in an argument here
    calculation = Calculation.query.get(id)
    return calculation_schema.jsonify(calculation)






# Endpoint for updating a calculation
@app.route("/calculation/<id>", methods=["PUT"])
def calculation_update(id):
    calculation = Calculation.query.get(id)
    valueOne = request.json['valueOne']
    operation = request.json['operation']
    valueTwo = request.json['valueTwo']
    valueAnswer = request.json['valueAnswer']

    calculation.valueOne = valueOne
    calculation.operation = operation
    calculation.valueTwo = valueTwo
    calculation.valueAnswer = valueAnswer

    db.session.commit()
    return calculation_schema.jsonify(calculation)






# Endpoint for deleting a calculation
@app.route("/calculation/<id>", methods=["DELETE"])
def calculation_delete(id):
    calculation = Calculation.query.get(id)
    db.session.delete(calculation)
    db.session.commit()
    return "Calculation was successfully deleted"



if __name__ == '__main__':
    app.run(debug=True)
    #