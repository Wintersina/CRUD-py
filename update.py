from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Resturant, MenuItem

sql_lite_db = create_engine('sqlite:///resturantmenu.db')  # say what database
Base.metadata.bind = sql_lite_db 
DBsession = sessionmaker(bind = sql_lite_db)
session = DBsession()

vegBurger = session.query(MenuItem).filter_by(item_name = 'Veggie Burger')
print("BEFORE UPDATE!!")
for v in vegBurger:
   print("resturant is " + v.resturant.name +" price is: " + v.price)

print("AFTER UPDATE!!")
vegBurger.price = "$2.99"
session.add(vegBurger)
session.commit()
for v in vegBurger:
   print("resturant is " + v.resturant.name +" price is: " + v.price)

