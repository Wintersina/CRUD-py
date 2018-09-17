# CRUD-py

## requirements 
python3
sqlite

## getstarted
use python3 to run ```python3 database_setup.py```
followed by:
1) create.py
2) lotsofmenu.py
3) read.py
4) update.py
5) delete.py

each will demonstrate the creation of database, and populate, read and update. lastly delete.

you can always open python3 shell and run quaries directly.

you will need: 
```
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Resturant, MenuItem
```
