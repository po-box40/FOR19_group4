from capp import db
from capp import application
from capp.models import User, Transport
from datetime import datetime, timedelta

yesterday = datetime.now() - timedelta(days=1)

day_before = datetime.now() - timedelta(days=2)

days_3_ago = datetime.now() - timedelta(days=3)

# create data for user_id=3
transport1 = Transport(
    kms=10, transport="car", fuel="diesel", date=day_before, co2=1, total=1.5, user_id=3
)
# create data for user_id=3 with a different date
transport2 = Transport(
    kms=20,
    transport="car",
    fuel="diesel",
    date=days_3_ago,
    co2=1,
    total=2.5,
    user_id=3,
)
transport3 = Transport(
    kms=30,
    transport="bus",
    fuel="diesel",
    date=yesterday,
    co2=1,
    total=3.5,
    user_id=3,
)

db.session.add(transport1)
db.session.add(transport2)
db.session.add(transport3)
db.session.commit()
