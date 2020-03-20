from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
import os
from places import Entry

def get_data():
    if "DATABASE_URL" in os.environ:
        engine = create_engine(os.environ["DATABASE_URL"])
    else:
        with open("database.txt") as f:
            engine = create_engine(f.readline())

    entries = pd.read_sql_table("entries", con=engine)
    engine.dispose()
    entries["place_relative"] = entries["place_current_popularity"] / entries["place_normal"]
    #entries = entries.set_index("created_on")
    data_today = entries.loc[entries["created_on"].dt.floor("d") == pd.Timestamp.today().floor("d")].groupby("place_name")["place_relative"].mean() * 100
    data_yesterday = entries.loc[entries["created_on"].dt.floor("d") == pd.Timestamp.today().floor("d") - pd.Timedelta('1 days')].groupby("place_name")["place_relative"].mean() * 100
    result = pd.DataFrame(data_yesterday).merge(data_today, how = "outer", on = "place_name", suffixes = ["_yesterday", "_today"])
    result["Trend"] = (data_today-data_yesterday) / data_yesterday * 100
    result = result.append(pd.Series({
        "place_relative_yesterday": result["place_relative_yesterday"].mean(),
        "place_relative_today": result["place_relative_today"].mean(),
        "Trend": (result["place_relative_today"].mean() - result["place_relative_yesterday"].mean())/result["place_relative_yesterday"].mean()*100
    }, name = "Deutschland Durchschnitt"))
    return result
