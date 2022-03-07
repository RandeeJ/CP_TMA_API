from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

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

class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valueOne = db.Column(db.Integer, unique=False)
    valueTwo = db.Column(db.Integer, unique=False)
    valueAnswer = db.Column(db.Integer, unique=False)
    # ^columns and data types

    def __init__(self, valueOne, valueTwo, valueAnswer):
        self.valueOne = valueOne
        self.valueTwo = valueTwo
        self.valueAnswer = valueAnswer

class CalculationSchema(ma.Schema):
    class Meta:
        fields = ('valueOne', 'valueTwo', 'valueAnswer')
        # is there a way to add a column based on the operation button that was selected?

calculation_schema = CalculationSchema()
# ^a single guide schema
calculations_schema = CalculationSchema(many=True)
# ^a multiple guides schema

#Endpoint to create a new guide
@app.route('/calculation', methods=["POST"])
#^anytime you want to create something in the database
def add_guide():
    valueOne = request.json['valueOne']
    # ^will get this object and then be able to parse it
    valueTwo = request.json['valueTwo']
    valueAnswer = request.json['valueAnswer']

    new_calculation = Calculation(valueOne, valueTwo, valueAnswer)

    db.session.add(new_calculation)
    # ^creates a new database session and adds a new guide inside of it

    db.session.commit()

    calculation = Calculation.query.get(new_calculation.id)

    return calculation_schema.jsonify(calculation)


if __name__ == '__main__':
    app.run(debug=True)
    #