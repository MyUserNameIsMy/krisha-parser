import json
import re

from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup


class Url(BaseModel):
    url: str


class Apartment(BaseModel):
    link: str
    description: str


app = FastAPI()


@app.post("/parse-apartment")
async def parse(url: Url):
    response = requests.get(url.url)
    soup = BeautifulSoup(response.content,  'html.parser')
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
        return data_object
    else:
        print("No JavaScript object found in the string.")


