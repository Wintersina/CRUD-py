from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Resturant, MenuItem

sql_lite_db = create_engine('sqlite:///resturantmenu.db')  # say what database
Base.metadata.bind = sql_lite_db 
DBsession = sessionmaker(bind = sql_lite_db)
session = DBsession()

results = session.query(MenuItem).all()

for r in results:
   print("name is " +r.item_name)
