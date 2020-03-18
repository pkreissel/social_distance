import populartimes
from datetime import datetime
from itertools import cycle
from sqlalchemy import create_engine, Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Configure Database
with open("database.txt") as f:
    engine = create_engine(f.readline())
Session = sessionmaker(bind=engine)
Base = declarative_base()
class Entry(Base):
    __tablename__ = 'entries'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    place_name = Column(String)
    place_id = Column(String)
    place_normal = Column(Integer)
    place_current_popularity = Column(Integer)
    created_ts = Column('created_on', DateTime, default=datetime.now)

    def __init__(self, place_name, place_id, place_normal,place_current_popularity):
        self.place_name = place_name
        self.place_id = place_id
        self.place_normal = place_normal
        self.place_current_popularity = place_current_popularity
Base.metadata.create_all(engine)


#Enable Key Cycling
with open("api_keys.txt") as f:
    api_keys = cycle([key.strip() for key in f.readlines()])

#Iterate over Places
place_ids = ["ChIJuVGxxf51nkcRwhxFwvIr7EM"]
session = Session()
for place_id in place_ids:
    data = populartimes.get_id(next(api_keys), place_id)
    entry = Entry(
        data["name"],
        data["id"],
        data["populartimes"][datetime.now().weekday()]["data"][datetime.now().hour],
        data["current_popularity"]
    )
    session.add(entry)
session.commit()
#Lets us know how many Calls we have made so far.
print("There are now " + str(session.query(Entry).count()) + " Entries in the Database")
session.close()
