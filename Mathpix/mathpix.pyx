import os
import base64
import requests
import json
import configparser



os.environ['APP_ID'] = "juanw2001_yahoo_com_4bc702"
os.environ['APP_KEY'] = "d55719f68eb72851c0f4"

env = os.environ

default_headers = {
    'app_id': env.get('APP_ID'),
    'app_key': env.get('APP_KEY'),
    'Content-type': 'application/json'
}

service = 'https://api.mathpix.com/v3/latex'


#return base64 encoding of an image with the given filename.

def image_uri(filename):
    image_data = open(filename, "rb").read()
    return "data:image/jpg;base64," + base64.b64encode(image_data).decode()

#call mathpix

def latex(args, headers=default_headers, timeout = 30):
    r = requests.post(service,
        data=json.dumps(args),headers=headers,timeout=timeout)
    return json.loads(r.text)