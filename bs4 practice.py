import pandas as pd
import requests
from bs4 import BeautifulSoup

df = pd.read_csv("COVID Data.csv")
df.head()

df['ADDRESS'] = df['Venue'].astype(str) + ',' + \
                df['Suburb'] + ',' + ' Australia'   

for address in df['ADDRESS']:
    pass
    url = "https://www.whereis.com/search-results?query=" + str(address)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
#    result = soup.find(class="listing-address")
    result = soup.find("div", class_ = "listing-address")
    print(result)
