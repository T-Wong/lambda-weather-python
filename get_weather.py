import pyowm
import boto3
import os
import requests
import json

from ISStreamer.Streamer import Streamer
from base64 import b64decode

LOCATION = 'Bothell, US'
BUCKET_NAME = 'OWM Weather Dashboard'
VAULT_ROOT = 'http://10.0.44.254:8200'

VAULT_TOKEN_ENCRYPTED = os.environ['vault_token']
VAULT_TOKEN = boto3.client('kms').decrypt(CiphertextBlob=b64decode(VAULT_TOKEN_ENCRYPTED))['Plaintext']

def get_vault_secret(token, vault_url, secret):
    headers = {
        'X-Vault-Token': token
    }
    response = requests.get(vault_url, headers=headers).json()

    return response['data'][secret]

def get_weather(location, api_key):
    owm = pyowm.OWM(api_key)
    observation = owm.weather_at_place(location)
    return observation.get_weather()

def send_to_is(bucket_name, bucket_key, access_key, weather):
    try:
        streamer = Streamer(bucket_name, bucket_key, access_key)

        # Temperature
        temp = weather.get_temperature(unit='fahrenheit').get('temp')
        streamer.log('Temperature (F)', temp)

        # Cloud coverage
        cloud = str(weather.get_clouds()) + '%'
        streamer.log('Cloud Coverage', cloud)

        # Detailed status
        detail_status = weather.get_detailed_status()
        streamer.log('Detailed Status', detail_status)

        # Humidity
        humidity = str(weather.get_humidity()) + '%'
        streamer.log('Humidity', humidity)

        # Visibility distance
        visibility_distance = weather.get_visibility_distance()
        streamer.log('Visibility Distance (m)', visibility_distance)

        # Wind speed
        wind_speed = weather.get_wind().get('speed')
        streamer.log('Wind Speed (m/s)', wind_speed)

        # Wind degree
        wind_degree = weather.get_wind().get('deg')
        streamer.log('Wind Degree', wind_degree)

    finally:
        streamer.close()

def lambda_handler(event, context):
    # Get secrets
    OWM_KEY = get_vault_secret(VAULT_TOKEN, VAULT_ROOT + '/v1/secret/owm/api_key', 'api_key')
    BUCKET_KEY = get_vault_secret(VAULT_TOKEN, VAULT_ROOT + '/v1/secret/initialstate/bucket', 'key')
    ACCESS_KEY = get_vault_secret(VAULT_TOKEN, VAULT_ROOT + '/v1/secret/initialstate/access', 'key')

    # Get weather object from OpenWeatherMap
    weather = get_weather(LOCATION, OWM_KEY)

    # Send weather data to InitialState
    send_to_is(BUCKET_NAME, BUCKET_KEY, ACCESS_KEY, weather)

