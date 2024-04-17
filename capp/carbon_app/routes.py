from flask import render_template, Blueprint, request, redirect, url_for, flash
from capp.models import Transport, User
from capp import db
from datetime import timedelta, datetime
from flask_login import login_required, current_user
from json import dumps as json_dumps

from capp.carbon_app.forms import (
    CarForm,
    BusForm,
    TrainForm,
    PlaneForm,
    MotorbikeForm,
    WalkForm,
    BicycleForm,
    FerryForm,
)

efco2 = {
    "Bus": {"Fossil fuel": 0.097, "Electric": 0},
    "Car": {
        "Normal": {
            "Petrol": 0.192,
            "Diesel": 0.171,
            "Hybrid": 0.068,
            "Electric": 0.047,
        },
        "Small": {
            "Petrol": 0.192 * 0.85,
            "Diesel": 0.171 * 0.85,
            "Hybrid": 0.068 * 0.85,
            "Electric": 0.047 * 0.85,
        },
        "Large": {
            "Petrol": 0.192 * 1.15,
            "Diesel": 0.171 * 1.15,
            "Hybrid": 0.068 * 1.15,
            "Electric": 0.047 * 1.15,
        },
    },
    "Plane": {
        "Domestic flight": {"Petrol": 0.246},
        "Short-haul flight": {"Petrol": 0.151},
        "Long-haul flight": {"Petrol": 0.147},
    },
    "Ferry": {"Passanger": {"Diesel": 0.0187}, "With car": {"Diesel": 0.1295}},
    "Train": {"Fossil fuel": 0.041, "Electric": 0.004},
    "Motorbike": {"Petrol": 0.114},
    "Bicycle": {"No Fossil Fuel": 0},
    "Walk": {"No Fossil Fuel": 0},

    'Ferry': {
        'Passenger': {'Diesel':0.0187},
        'Driver alone': {'Diesel':0.1295},
        'Driver with passengers' : {'Diesel':0.1295}
    },
    'Train':{'Fossil fuel': 0.041, 'Electric': 0.004},
    'Motorbike':{'Petrol':0.114},
    'Bicycle':{'No Fossil Fuel':0},
    'Walk':{'No Fossil Fuel':0}}


carbon_app = Blueprint("carbon_app", __name__)


@carbon_app.route("/carbon_app")
def carbon_app_home():
    return render_template("carbon_app/carbon_app.html", title="carbon_app")


@carbon_app.route("/carbon_calculator")
def carbon_calculator_home():
    return render_template("carbon_app/carbon_calculator.html")


@carbon_app.route("/carbon_app/carbon_your_emissions", methods=["GET", "POST"])
def carbon_your_emissions():
    # Your code here
    # get the current user
    current_user = User.query.filter_by(username="test1").first()

    db_entries = Transport.query.filter_by(
        date=datetime.now().date(), author=current_user
    ).all()
    # query the database to get the emission data per date
    db_entries = Transport.query.filter_by(
        date=datetime.now().date(), author=current_user
    ).all()

    emissions_by_transport = (
        db.session.query(db.func.sum(Transport.total), Transport.transport)
        .filter_by(author=current_user)
        .group_by(Transport.transport)
        .order_by(Transport.transport.asc())
        .all()
    )

    # a list to store the emissions by transport
    transport_emissions = [
        {"transport": transport, "total": total}
        for total, transport in emissions_by_transport
    ]

    # Making the dictionary a JSON object
    transport_emissions_json = json_dumps(transport_emissions)
    print(db_entries)

    print(transport_emissions_json)
    print(type(transport_emissions_json))
    print(transport_emissions)
    print(type(transport_emissions))

    return render_template(
        "carbon_app/carbon_your_emissions.html",
        title="Carbon Your Emissions",
        db_entries=db_entries,
        transport_emissions_json=transport_emissions_json,
    )


@carbon_app.route("/carbon_app/new_entry_bus", methods=["GET", "POST"])
def new_entry_bus():
    form = BusForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data

        # Get the CO2 emissions per kilometer for the selected fuel type
        co2 = efco2["Bus"][fuel]

        # Calculate total CO2 emissions
        total_co2_emissions = co2 * kms
        co2 = float(kms) * efco2['Bus'][fuel]
        co2 = round(co2, 4)
    

        return f'Total CO2 emissions for the bus journey: {co2}'

    return render_template(
        "carbon_app/new_entry_bus.html", title="New Entry Bus", form=form
    )


@carbon_app.route("/carbon_app/new_entry_car", methods=["GET", "POST"])
def new_entry_car():
    form = CarForm()
    if form.validate_on_submit():
        kms = form.kms.data
        size = form.size.data
        fuel = form.fuel_type.data

        # Define the CO2 emissions factor based on the size of the car
        if size == "Small":
            factor = 0.85
        elif size == "Large":
            factor = 1.15
        else:
            factor = 1.0  # Normal size

        # Access the appropriate CO2 emissions factor based on the size and fuel type
        co2 = float(kms) * efco2["Car"][size][fuel] * factor

        # Round the CO2 emissions value to two decimal places
        co2 = round(co2, 4)

        return f"CO2 emissions: {co2}"  # Corrected indentation

    return render_template(
        "carbon_app/new_entry_car.html", title="New Entry Car", form=form
    )


@carbon_app.route("/carbon_app/new_entry_train", methods=["GET", "POST"])
def new_entry_train():
    form = TrainForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data

        # Get the CO2 emissions per kilometer for the selected fuel type
        co2 = float(kms) * efco2['Train'][fuel]
        co2 = round (co2, 4)

        return f'Total CO2 emissions for the train journey: {co2}'

    return render_template(
        "carbon_app/new_entry_train.html", title="New Entry Train", form=form
    )


@carbon_app.route("/carbon_app/new_entry_plane", methods=["GET", "POST"])
def new_entry_plane():
    form = PlaneForm()
    if form.validate_on_submit():
        kms = form.kms.data
        flight_type = form.flight_type.data

        # Get the CO2 emissions per kilometer for the selected flight type
        co2 = float(kms) * efco2["Plane"][flight_type]["Petrol"]

        co2 = round(co2, 4)

        return f"Total CO2 emissions for the {flight_type}: {co2}"

    return render_template(
        "carbon_app/new_entry_plane.html", title="New Entry Plane", form=form
    )


@carbon_app.route("/carbon_app/new_entry_motorbike", methods=["GET", "POST"])
def new_entry_motorbike():
    form = MotorbikeForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data

        # Get the CO2 emissions per kilometer for the selected fuel type
        co2 = float(kms) * efco2["Motorbike"][fuel]

        co2 = round(co2, 4)
        
        return f'Total CO2 emissions for the motorbike journey: {co2}'

    return render_template(
        "carbon_app/new_entry_motorbike.html", title="New Entry Motorbike", form=form
    )


@carbon_app.route("/carbon_app/new_entry_walk", methods=["GET", "POST"])
def new_entry_walk():
    form = form = WalkForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data

        co2 = float(kms) * efco2["Walk"][fuel]

        co2 = round(co2, 4)

        return f"Total CO2 emissions for the walking tour: {co2}"

    return render_template(
        "carbon_app/new_entry_walk.html", title="New Entry Walk", form=form
    )


@carbon_app.route("/carbon_app/new_entry_bicycle", methods=["GET", "POST"])
def new_entry_bicycle():
    form = BicycleForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data

        co2 = float(kms) * efco2['Bicycle'][fuel]

        co2 = round(co2, 4)

        return f'Total CO2 emissions for the bicycle journey: {co2}'
    
    return render_template('carbon_app/new_entry_bicycle.html', title='New Entry Bicycle' , form=form)

@carbon_app.route("/carbon_app/new_entry_ferry", methods=["GET", "POST"])
def new_entry_ferry():
    form = FerryForm()
    if form.validate_on_submit():
        kms = form.kms.data
        travel_option = form.travel_option.data
        passengers = form.passengers.data


        if travel_option == 'Passenger':
            co2 = float(kms) * efco2['Ferry'][travel_option]['Diesel']
            co2 = round(co2, 4)


        if travel_option == 'Driver alone':
             co2 = float(kms) * efco2['Ferry'][travel_option]['Diesel']
             co2 = round(co2, 4)
        

        if travel_option == 'Driver with passengers': 

            co2_driver = float(kms) * efco2['Ferry'][travel_option]['Diesel']
            co2_passengers = float(kms) * efco2['Ferry']['Passenger']['Diesel'] * passengers

            co2 = co2_passengers + co2_driver
            co2 = round(co2, 4)

        # Calculate CO2 emissions per passenger
        if travel_option == 'Passenger':
            co2_per_passenger = co2
        if travel_option == 'Driver alone':
            co2_per_passenger = co2
        if travel_option == 'Driver with passengers': 
            P = passengers + 1  # Total number of passengers including the driver
            co2_per_passenger = co2 / P
            co2_per_passenger = round(co2_per_passenger, 4)

        return f'Total CO2 emissions for the ferry journey: {co2}, CO2 emissions per passenger: {co2_per_passenger}'

    return render_template(
        "carbon_app/new_entry_ferry.html", title="New Entry Ferry", form=form
    )
