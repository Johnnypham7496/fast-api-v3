import requests
import json


def rest_call_outside_api():
    cats_url= "https://cat-fact.herokuapp.com/facts"
    chuck_url = "https://api.chucknorris.io/jokes/random"
    record_index = 0

    cats_response = requests.get(cats_url).content
    chuck_response = requests.get(chuck_url).content
    
    # convert string to json 
    cat_json = json.loads(cats_response)
    chuck_json = json.loads(chuck_response)

    # get info from json
    cat_fact = cat_json[record_index]["text"]
    chuck_joke = chuck_json["value"]

    # business logic / return custom json message 
    return_message = {"cat_says": cat_fact, "chuck_says": chuck_joke }

    return return_message