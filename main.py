
"""
---------------------------------------
    * Course: 100 Days of Code - Dra. Angela Yu
    * Author: Noah Louvet
    * Day: 38
    * Subject: Workout Tracker - Environment variables - API - Google sheets
---------------------------------------
"""


import os
import requests
from datetime import datetime

# Very useful in this code: ENVIRONMENT VARIABLE !!!

GENDER = "male"
WEIGHT_KG = 63
HEIGHT_CM = 169
AGE = 23


APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
TOKEN = os.environ["TOKEN"]


ENDPOINT = "https://trackapi.nutritionix.com"
exercise_endpoint = f"{ENDPOINT}/v2/natural/exercise"

SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]

exercise_text = input("what exercise did you do today?: ")

params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

response = requests.post(url=exercise_endpoint, json=params, headers=headers)
result = response.json()
print(result["exercises"][0])

today = datetime.now()

# Bearer Token Authentication
bearer_headers = {
    "Authorization": f"Bearer {TOKEN}"
}

for exercise in result["exercises"]:
    sheety_params = {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%X"),
            "exercise": (result["exercises"][0]["name"]).title(),
            "duration": result["exercises"][0]["duration_min"],
            "calories": result["exercises"][0]["nf_calories"]
        }
    }

    sheet_response = requests.post(SHEETY_ENDPOINT, json=sheety_params, headers=bearer_headers)
    print(sheet_response.text)

