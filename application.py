from flask import Flask, render_template
from flask import request, flash

application = Flask(__name__)


@application.route("/")
@application.route("/home")
def home():
    return render_template("home.html")


@application.route("/methodology")
def methodology():
    return render_template("methodology.html", title="methodology")


@application.route("/carbon_app")
def carbon_app():
    return render_template("carbon_app.html", title="carbon_app")


@application.route("/AboutUs")
def AboutUs():
    return render_template("AboutUs.html", title="About Us")


@application.route("/carbon_calculator")
def carbon_calculator():
    return render_template("carbon_calculator.html", title="carbon_calculator")


# a route for the carbon calculator results
@application.route("/calculate-carbon-footprint", methods=["POST"])
def carbon_calculator_results():
    co2_equivalents = {"bus": 68, "train": 14, "car": 156, "plane": 285}

    print(request.get_json())
    # Get the data from the json file
    data = request.get_json()
    print(data)

    # Get the transport method and the number of kilometers from the data
    transport_method = data.get("transportMethod")
    kilometers = data.get("kilometers")

    # Look up the CO2 equivalent value for the transport method
    co2_equivalent = co2_equivalents.get(transport_method)
    # Convert the CO2 equivalent from grans to kilograms
    co2_equivalent = co2_equivalent / 1000

    print(co2_equivalent)

    # convert kilometers to float
    kilometers = float(kilometers)

    # Calculate the carbon footprint
    carbon_footprint = co2_equivalent * kilometers
    # round down to 2 decimal places
    carbon_footprint = round(carbon_footprint, 2)

    print(carbon_footprint)

    return {"carbonFootprint": carbon_footprint}


if __name__ == "__main__":
    application.run(debug=True)
