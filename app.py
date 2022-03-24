from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)


class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valueOne = db.Column(db.Integer, unique=False)
    valueTwo = db.Column(db.Integer, unique=False)
    valueAnswer = db.Column(db.Integer, unique=False)
    operation = db.Column(db.String, unique=False) 

    def __init__(self, valueOne, operation, valueTwo, valueAnswer):
        self.valueOne = valueOne
        self.operation = operation
        self.valueTwo = valueTwo
        self.valueAnswer = valueAnswer

class CalculationSchema(ma.Schema):
    class Meta:
        fields = ('id','valueOne', 'operation', 'valueTwo', 'valueAnswer')

calculation_schema = CalculationSchema()
calculations_schema = CalculationSchema(many=True)




@app.route('/calculation', methods=["POST"])
def add_calculation():
    print(request.get_json())
    valueOne = request.json['valueOne']
    operation = request.json['operation']
    valueTwo = request.json['valueTwo']
    valueAnswer = request.json['valueAnswer']

    new_calculation = Calculation(valueOne, operation, valueTwo, valueAnswer)

    db.session.add(new_calculation)

    db.session.commit()

    calculation = Calculation.query.get(new_calculation.id)

    return calculation_schema.jsonify(calculation)





@app.route('/calculations', methods=["GET"])
def get_calculations():
    all_calculations = Calculation.query.all()
    result = calculations_schema.dump(all_calculations)
    return jsonify(result)





@app.route("/calculation/<id>", methods=["GET"])
def get_calculation(id):
    calculation = Calculation.query.get(id)
    return calculation_schema.jsonify(calculation)






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






@app.route("/calculation/<id>", methods=["DELETE"])
def calculation_delete(id):
    calculation = Calculation.query.get(id)
    print(calculation)
    print(id)
    db.session.delete(calculation)
    db.session.commit()
    return "Calculation was successfully deleted"



if __name__ == '__main__':
    app.run(debug=True)