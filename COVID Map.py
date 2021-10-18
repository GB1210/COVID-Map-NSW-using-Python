import pandas as pd
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import matplotlib.pyplot as plt
import folium
from folium.plugins import FastMarkerCluster

locator = Nominatim(user_agent="myGeocoder")
location = input("Where are you? (# STREET, POSTCODE) >>> ")
location = locator.geocode(location)
print(location.address)
print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))

df = pd.read_csv("COVID Data MAN.csv")
df.head()

df['ADDRESS'] = df['Venue'].astype(str) + ',' + ' Australia'

df.head()

from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
df['location'] = df['ADDRESS'].apply(geocode)
df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)

df['point'][0][0]

# split point column into latitude, longitude and altitude columns
df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)
df.head()

df.columns

df = df.drop(['Last updated', 'Type', 'Suburb', 'Venue', 'Date and time of exposure','Health advice'], axis=1)
df.head()

df.latitude.isnull().sum()

df = df[pd.notnull(df["latitude"])]

map1 = folium.Map(
    location=[location.latitude, location.longitude],
    tiles='cartodbpositron',
    zoom_start=12,
)

df.apply(lambda row:folium.CircleMarker(location=[row["latitude"], row["longitude"]]).add_to(map1), axis=1)
map1

map1.save("map1.html")



folium_map = folium.Map(location=[location.latitude, location.longitude],
                        zoom_start=12,
                        tiles='CartoDB dark_matter')


FastMarkerCluster(data=list(zip(df['latitude'].values, df['longitude'].values))).add_to(folium_map)
folium.LayerControl().add_to(folium_map)
folium_map

folium_map.save("map2.html")
