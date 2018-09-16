from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Resturant, MenuItem

sql_lite_db = create_engine('sqlite:///resturantmenu.db')  # say what database
Base.metadata.bind = sql_lite_db
DBsession = sessionmaker(bind = sql_lite_db)
session = DBsession()


#spinach = session.query(MenuItem).filter_by(item_name = 'Spinach Ice Cream').first()

#print(spinach.resturant.name)

spinach = session.query(MenuItem).filter_by(item_name = 'Spinach Ice Cream').one()
session.delete(spinach)
session.commit()

