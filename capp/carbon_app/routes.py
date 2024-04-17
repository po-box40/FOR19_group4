from flask import render_template, Blueprint, request, redirect, url_for, flash
from capp.models import Transport
from capp import db
from datetime import timedelta, datetime
from flask_login import login_required, current_user
from capp.carbon_app.forms import CarForm

efco2 = {
    'Bus': {'Fossil fuel': 0.097, 'Electric': 0},
    'Car': {
        'Normal': {
            'Petrol': 0.192,
            'Diesel': 0.171,
            'Hybrid': 0.068,
            'Electric': 0.047
        },
        'Small': {
            'Petrol': 0.192 * 0.85,
            'Diesel': 0.171 * 0.85,
            'Hybrid': 0.068 * 0.85,
            'Electric': 0.047 * 0.85
        },
        'Large': {
            'Petrol': 0.192 * 1.15,
            'Diesel': 0.171 * 1.15,
            'Hybrid': 0.068 * 1.15,
            'Electric': 0.047 * 1.15
        }
    },
    'Plane': {
        'Domestic flight': {'Petrol': 0.246},
        'Short-haul flight': {'Petrol': 0.151},
        'Long-haul flight': {'Petrol': 0.147}
    },
    'Ferry': {
        'Passanger': {'Diesel':0.0187},
        'With car': {'Diesel':0.1295}
    },
    'Train':{'Fossil fuel': 0.041, 'Electric': 0.004},
    'Motorbike':{'Petrol':0.114},
    'Bicycle':{'No Fossil Fuel':0},
    'Walk':{'No Fossil Fuel':0}}


carbon_app=Blueprint('carbon_app',__name__)


@carbon_app.route('/carbon_app')
def carbon_app_home():
    return render_template('carbon_app/carbon_app.html', title='carbon_app')

@carbon_app.route('/carbon_calculator')
def carbon_calculator_home():
    return render_template('carbon_app/carbon_calculator.html')



@carbon_app.route('/carbon_app/new_entry_car', methods=['GET', 'POST'])
def new_entry_car():
    form = CarForm()
    if form.validate_on_submit():
        kms = form.kms.data
        size = form.size.data
        fuel = form.fuel_type.data

        # Define the CO2 emissions factor based on the size of the car
        if size == 'Small':
            factor = 0.85
        elif size == 'Large':
            factor = 1.15
        else:
            factor = 1.0  # Normal size

        # Access the appropriate CO2 emissions factor based on the size and fuel type
        co2 = float(kms) * efco2['Car'][size][fuel] * factor

        # Round the CO2 emissions value to two decimal places
        co2 = round(co2, 2)

        return f'CO2 emissions: {co2}'  # Corrected indentation

    return render_template('carbon_app/new_entry_car.html', title='New Entry Car', form=form)
