import populartimes
from datetime import datetime
from itertools import cycle
from sqlalchemy import create_engine, Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time


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

#populartimes.get_id(next(api_keys), "ChIJdRuke6ZXn0cRUxrxk9-6NFg")
#Iterate over Places
def api_call():
    place_ids = [
    "ChIJuVGxxf51nkcRwhxFwvIr7EM",
    "ChIJ4dic-71RqEcRZIsmE3K6r-0",
    "ChIJ25xRQB9OqEcRiDCQLqrmcbA",
    "ChIJe9nAXKZXn0cRGUlOPBMiDIo",
    "ChIJmZ8cBbbCuEcRecCyfQofums",
    "ChIJX34c7jLbmUcRhaEUxVf0H3w",
    "ChIJraB7riH4pkcRGXSvqsL52lM",
    "ChIJ4___HmbPCUcRN5Ub3P2ZfmQ",
    "ChIJcaYkt1gXuUcRPhoGAkKO10k",
    "ChIJDSw1eVUJvUcRWndDicZ7OLo"]
    session = Session()
    for x, place_id in enumerate(place_ids):
        #print(x)
        time.sleep(80)
        try:
            key = next(api_keys)
            data = populartimes.get_id(key, place_id)
        except Exception as e:
            print(e)
            print("Error with key: " + key)
            continue
        print(data["name"])
        if "current_popularity" in data:
            entry = Entry(
                data["name"],
                data["id"],
                data["populartimes"][datetime.now().weekday()]["data"][datetime.now().hour],
                data["current_popularity"]
            )
            session.add(entry)
        else:
            print("No Popularity-Data for " + data["name"])
    session.commit()
    #Lets us know how many Calls we have made so far.
    print("There are now " + str(session.query(Entry).count()) + " Entries in the Database")
    session.close()

#api_call()
