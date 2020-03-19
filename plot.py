import matplotlib.pyplot as plt
from sqlalchemy.orm import sessionmaker
from places import Entry
from sqlalchemy import create_engine
import pandas as pd

with open("database.txt") as f:
    engine = create_engine(f.readline())
Session = sessionmaker(bind=engine)
session = Session()

entries = pd.read_sql_table("entries", con=engine)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1)

entries["place_relative"] = entries["place_current_popularity"] / entries["place_normal"]
entries = entries.set_index("created_on")
entries.groupby("place_id")["place_relative"].rolling(3).mean().plot(y="place_relative", ax = ax)

fig.savefig("plot.png")
