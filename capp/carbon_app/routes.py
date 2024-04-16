from flask import render_template, Blueprint
from flask_login import login_required, current_user

efco2={'Bus':{'Diesel':0.10231,'CNG':0.08,'Petrol':0.10231,'No Fossil Fuel':0},
    'Car':{'Petrol':0.18592,'Diesel':0.16453,'No Fossil Fuel':0},
    'Plane':{'Petrol':0.24298},
    'Ferry':{'Diesel':0.11131, 'CNG':0.1131, 'No Fossil Fuel':0},
    'Motorbike':{'Petrol':0.09816,'No Fossil Fuel':0},
    'Bicycle':{'No Fossil Fuel':0},
    'Walk':{'No Fossil Fuel':0}}


carbon_app=Blueprint('carbon_app',__name__)


@carbon_app.route('/carbon_app')
def carbon_app_home():
    return render_template('carbon_app/carbon_app.html', title='carbon_app')

@carbon_app.route('/carbon_calculator')
def carbon_calculator_home():
    return render_template('carbon_app/carbon_calculator.html')



