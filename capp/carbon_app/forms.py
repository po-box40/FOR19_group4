from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import InputRequired


class CarForm(FlaskForm):
    kms = FloatField('Kilometers', validators=[InputRequired()])
    size = SelectField('Size of Car', choices=[('Normal', 'Normal'), ('Small', 'Small'), ('Large', 'Large')], validators=[InputRequired()])
    fuel_type = SelectField('Type of Fuel', choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Hybrid', 'Hybrid'), ('Electric', 'Electric')], validators=[InputRequired()])
    submit = SubmitField('Submit')
