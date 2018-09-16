from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Resturant, MenuItem

sql_lite_db = create_engine('sqlite:///resturantmenu.db')  # say what database
Base.metadata.bind = sql_lite_db 
DBsession = sessionmaker(bind = sql_lite_db)
session = DBsession()

PizzaPala = Resturant(name = "Pizza Pala") # crate a new resturant 
session.add(PizzaPala) # add new resturant to staging zone
session.commit() #commit to database

#find all resturants
r = session.query(Resturant).all()
print(r)
cheesePizza = MenuItem(item_name = "Cheeze Pizza", item_type = "entree" , price = "$5.99",  description = "a very good, cheezie goodness" , resturant = PizzaPala)
session.add(cheesePizza)
session.commit()
r = session.query(MenuItem).all
print(r)
