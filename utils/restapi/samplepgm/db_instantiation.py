from application import db
from application import Drink

db.create_all()

drink1 = Drink(name="Mango Juice", description="Summer's Refresher")
db.session.add(drink1)

drink2 = Drink(name="Sugarcane Juice", description="Sweet & Healthy Juice")
db.session.add(drink2)

db.session.commit()
