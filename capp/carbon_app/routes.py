from flask import render_template, Blueprint, request, redirect, url_for, flash
from capp.models import Transport
from capp import db
from datetime import timedelta, datetime
from flask_login import login_required, current_user
from capp.carbon_app.forms import CarForm, BusForm, TrainForm, PlaneForm, MotorbikeForm, WalkForm, BicycleForm, FerryForm 

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


@carbon_app.route('/carbon_app/new_entry_bus', methods=['GET','POST'])
def new_entry_bus():
    form = BusForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data

        # Get the CO2 emissions per kilometer for the selected fuel type
        co2 = efco2['Bus'][fuel]

        # Calculate total CO2 emissions
        total_co2_emissions = co2 * kms

        return f'Total CO2 emissions for the bus journey: {total_co2_emissions}'

    return render_template('carbon_app/new_entry_bus.html', title='New Entry Bus', form=form)



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



@carbon_app.route('/carbon_app/new_entry_train', methods=['GET','POST'])
def new_entry_train():
    form = TrainForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data

        # Get the CO2 emissions per kilometer for the selected fuel type
        co2= float(kms) * efco2['Train'][fuel]

        # Calculate total CO2 emissions
        total_co2_emissions = co2 * kms 

        return f'Total CO2 emissions for the train journey: {total_co2_emissions}'

    return render_template('carbon_app/new_entry_train.html', title='New Entry Train', form=form)



@carbon_app.route('/carbon_app/new_entry_plane', methods=['GET', 'POST'])
def new_entry_plane():
    form = PlaneForm()
    if form.validate_on_submit():
        kms = form.kms.data
        flight_type = form.flight_type.data

        # Get the CO2 emissions per kilometer for the selected flight type
        co2 = float(kms) * efco2['Plane'][flight_type]['Petrol']

        co2 = round(co2, 2)

        return f'Total CO2 emissions for the {flight_type}: {co2}'

    return render_template('carbon_app/new_entry_plane.html', title='New Entry Plane', form=form)



@carbon_app.route('/carbon_app/new_entry_motorbike', methods=['GET', 'POST'])
def new_entry_motorbike():
    form = MotorbikeForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data

        # Get the CO2 emissions per kilometer for the selected fuel type
        co2 = float(kms) * efco2['Motorbike'][fuel]

        co2 = round(co2, 2)
        
        return f'Total CO2 emissions for the motorbike journey: {co2}'

    return render_template('carbon_app/new_entry_motorbike.html', title='New Entry Motorbike', form=form)


@carbon_app.route('/carbon_app/new_entry_walk', methods=['GET','POST'])
def new_entry_walk():
    form = form = WalkForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data

        co2 = float(kms) * efco2['Walk'][fuel]

        co2 = round(co2, 2)

        return f'Total CO2 emissions for the walking tour: {co2}'
    
    return render_template('carbon_app/new_entry_walk.html', title='New Entry Walk' , form=form)



@carbon_app.route('/carbon_app/new_entry_bicycle', methods=['GET','POST'])
def new_entry_bicycle():
    form = BicycleForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data

        co2 = float(kms) * efco2['Bicycle'][fuel]

        co2 = round(co2, 2)

        return f'Total CO2 emissions for the bicycle journey: {co2}'
    
    return render_template('carbon_app/new_entry_bicycle.html', title='New Entry Bicycle' , form=form)

@carbon_app.route('/carbon_app/new_entry_ferry', methods=['GET', 'POST'])
def new_entry_ferry():
    form = FerryForm()
    if form.validate_on_submit():
        kms = form.kms.data
        travel_option = form.travel_option.data
        passengers = form.passengers.data

        # Get the CO2 emissions per km for the selected travel option and fuel type
        co2_per_km = efco2['Ferry'][travel_option]['Diesel']

        # Define the CO2 emissions per km for one passenger (driver)
        e = co2_per_km

        # Define the CO2 emissions per km for additional passengers
        e_prime = 0  # Assuming no additional emissions for passengers in this case
        if travel_option == 'Driver with passengers':
            e_prime = co2_per_km

        # Calculate total CO2 emissions for the ferry journey
        total_co2_emissions = (e * kms) + (e_prime * kms * passengers)

        # Calculate CO2 emissions per passenger
        if travel_option == 'Alone':
            co2_per_passenger = total_co2_emissions
        else:
            P = passengers + 1  # Total number of passengers including the driver
            co2_per_passenger = total_co2_emissions / P

        return f'Total CO2 emissions for the ferry journey: {total_co2_emissions}, CO2 emissions per passenger: {co2_per_passenger}'

    return render_template('carbon_app/new_entry_ferry.html', title='New Entry Ferry', form=form)
