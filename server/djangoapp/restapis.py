import requests
import json
# import related models here
from .models import *
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    json_data = []
    try:      
        if 'api_key' in kwargs:
            print("with api_key req")
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            print("no api_key req")
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)

        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)                                    
    except:
        # If any error occurs
        print("Network exception occurred")
    
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print("json_payload: {}".format(json_payload))
    print("POST from {} ".format(url))

    response = requests.post(url, params=kwargs, json=json_payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))

    json_data = json.loads(response.text)
    print("json_data: {}".format(json_data))

    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:

        for dealer in json_result:
            dealer_doc = dealer
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)

    dealer_obj = {}

    if json_result:
        print(json_result)
        dealers = json_result           
        dealer_doc = dealers[0]
        dealer_obj = CarDealer(
            address = dealer_doc["address"], city = dealer_doc["city"], id = dealer_doc["id"],
            lat = dealer_doc["lat"], long = dealer_doc["long"], full_name = dealer_doc["full_name"],
            st = dealer_doc["st"], zip = dealer_doc["zip"], short_name = dealer_doc["short_name"])

    return dealer_obj

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, id=dealer_id)

    if json_result:
        for review in json_result:
            review_doc = review

            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"],
                                   review=review_doc["review"], purchase_date=review_doc["purchase_date"], car_make=review_doc["car_make"],
                                   car_model=review_doc["car_model"],
                                   car_year=review_doc["car_year"], sentiment=analyze_review_sentiments(review_doc["review"]), id=review_doc["id"])
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    # - Call get_request() with specified arguments
    # - Get the returned sentiment label such as Positive or Negative
    URL = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/12431dd7-5cb4-4660-b415-f3550e81c015"
    API_KEY = "ErgndgHJTQu8y_oLjTMMpV663KIJPSbzA0IH3r5948g-"

    authenticator = IAMAuthenticator(API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator)
    natural_language_understanding.set_service_url(URL)
    response = natural_language_understanding.analyze(text=text,language='en', features=Features(
        sentiment=SentimentOptions(targets=[text]))).get_result()
      
    sentiment_label = label = response['sentiment']['document']['label']
    print(text + " sentiment = " + sentiment_label)

    return sentiment_label

