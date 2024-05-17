import requests
import json
# import related models here
from.models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")
    return 0

def auth_get_request(url, params, api_key=""):
    print(params)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")
    return 0

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload):
    print("POST from {} ".format(url))
    print("With payload: {}".format(str(json_payload)))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, json=json_payload)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")
    return 0

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def get_dealer_by_id(url, dealerId):
    new_url = url + f"?dealerId={dealerId}"

    return get_dealers_from_cf(new_url)

def get_dealer_by_state(url, state):
    new_url = url + f"?state={state}"

    return get_dealers_from_cf(new_url)
    

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)

    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["reviews"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(
                            review_doc["dealership"],
                            review_doc["name"],
                            review_doc["purchase"],
                            review_doc["review"],
                            review_doc["purchase_date"],
                            review_doc["car_make"],
                            review_doc["car_model"],
                            review_doc["car_year"],
                            "nan",
                            review_doc["id"]
                        )
            review_obj.sentiment = analyze_review_sentiments(review_obj.review[0])
            review_obj.review = review_obj.review[0]
            review_obj.name = review_obj.name[0]
            review_obj.car_model = review_obj.car_model[0]
            review_obj.car_make = review_obj.car_make[0]
            review_obj.purchase_date = review_obj.purchase_date[0]  
            results.append(review_obj)

    return results  
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):

    url = "https://sentiment-analysis9.p.rapidapi.com/sentiment"

    payload = [
        {
            "id": "1",
            "language": "en",
            "text": dealerreview
        }
    ]
    headers = {
        "content-type": "application/json",
        "Accept": "application/json",
        "X-RapidAPI-Key": "",
        "X-RapidAPI-Host": ""
    }

    response = requests.post(url, json=payload, headers=headers)
    print(f"Analyzing: {dealerreview}")
    sentiment = response.json()[0]['predictions'][0]['prediction']

    return sentiment

def get_review_id():
    url = "http://localhost:5000/review/final"

    final_index = get_request(url)

    return final_index + 1


