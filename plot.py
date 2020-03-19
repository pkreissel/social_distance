from sqlalchemy.orm import sessionmaker
from .places import Entry
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime

def get_data():
    with open("database.txt") as f:
        engine = create_engine(f.readline())
    Session = sessionmaker(bind=engine)
    session = Session()

    entries = pd.read_sql_table("entries", con=engine)
    entries.drop_duplicates(["place_id", "place_name"])[["place_id", "place_name"]].to_csv("places.csv", index = False)

    entries["place_relative"] = entries["place_current_popularity"] / entries["place_normal"]
    #entries = entries.set_index("created_on")
    data_today = entries.loc[entries["created_on"].dt.floor("d") == pd.Timestamp.today().floor("d")].groupby("place_name")["place_relative"].mean()
    data_yesterday = entries.loc[entries["created_on"].dt.floor("d") == pd.Timestamp.today().floor("d") - pd.Timedelta('1 days')].groupby("place_name")["place_relative"].mean()
    result = pd.DataFrame(data_yesterday).merge(data_today, how = "outer", on = "place_name", suffixes = ["_yesterday", "_today"])
    return result
