import json
import re
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware


class Url(BaseModel):
    url: str


class Apartment(BaseModel):
    link: str
    live_rooms: int
    price: int
    live_square: float
    text: str
    country: str
    region: str
    city: str
    street: str
    house_num: str


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/parse-apartment")
async def parse(url: Url):
    response = requests.get(url.url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script = soup.find('script', id='jsdata')
    pattern = r'var data = ({.*?});'

    # Find the JavaScript object using regular expression
    match = re.search(pattern, script.get_text())

    if match:
        # Extract the JavaScript object
        data_object_str = match.group(1)
        # Parse the extracted JSON string into a Python object
        data_object = json.loads(data_object_str)
        print("Retrieved object:", data_object)
        apartment = Apartment(
            price=data_object['advert']['price'],
            link=url.url,
            live_square=data_object['advert']['square'],
            live_rooms=data_object['advert']['rooms'],
            text=data_object['adverts'][0]['description'],
            country=data_object['advert']['address']['country'],
            region=data_object['advert']['address']['region'],
            city=data_object['advert']['address']['city'],
            street=data_object['advert']['address']['street'],
            house_num=data_object['advert']['address']['house_num'],
        )
        return apartment
    else:
        print("No JavaScript object found in the string.")
