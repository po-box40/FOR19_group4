from capp import db
from capp import application
from capp.models import User, Transport


# create data for user_id=3
transport9 = Transport(
    kms=10, transport="car", fuel="diesel", co2=1, total=1.5, user_id=3
)
transport10 = Transport(
    kms=15, transport="bike", fuel="none", co2=0, total=0, user_id=3
)
transport11 = Transport(
    kms=25, transport="plane", fuel="diesel", co2=3, total=4, user_id=3
)
transport12 = Transport(
    kms=12, transport="bus", fuel="petrol", co2=1, total=2, user_id=3
)
db.session.add(transport9)
db.session.add(transport10)
db.session.add(transport11)
db.session.add(transport12)
transport13 = Transport(
    kms=5, transport="motorbike", fuel="diesel", co2=0.7, total=1.3, user_id=3
)
transport14 = Transport(
    kms=7, transport="ferry", fuel="diesel", co2=0.8, total=1, user_id=3
)
transport15 = Transport(
    kms=15, transport="walk", fuel="none", co2=0, total=0, user_id=3
)
transport16 = Transport(
    kms=19, transport="bike", fuel="none", co2=0, total=0, user_id=3
)
db.session.add(transport13)
db.session.add(transport14)
db.session.add(transport15)
db.session.add(transport16)
db.session.commit()
