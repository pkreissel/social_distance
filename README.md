# social_distance
Use Google Public popularity data to check if people adhere to social distancing

requirements:
all the requirements in requirements.txt
a file database.txt that has a single link to a postgresql database
a file api_keys.txt with some Google Console API Keys with Maps API enabled (you have 5000 free requests per month, we are trying to get Google to give us more)

clock.py runs a service that regularly calls the API
places.py has a Google-Cloud-API-call-func that gets called by clock.py. the result of this function is saved to a database. 

app.py is the Web-Service that currently runs on Heroku and supplys DataWrapper with the data
plot.py is called by app.py to get the data out of the database and into a nice table that is then parsed as csv in app.py

In places.py you have to exchange the place ids for the ones that you want to query. This is quite challenging because not all places feature popularity counts. Its best if you check Google Maps for places that have popularity counts, and then use this page to get the ID of the place: https://developers.google.com/places/web-service/place-id?hl=de This is also not trivial, because sometimes there are multiple places with the same name and only one has popularity data.


