from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
# from .models import related models
from .models import CarDealer, CarMake, CarModel
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_review_id
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def home(request):
    context = {}

    if request.method == 'GET':
        return render(request, '/index.html', context)
# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)

# Create a `signup` view to return a static signup page
#def contact(request):
def sign_up(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/signup.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
def login_request(request):

    error_message = None

    context = {}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
    
        user = authenticate(request, username=username, password=password)
        print("Trying login...")
        if user:
            print("Found user, logging in")
            login(request, user)
            return redirect('..')
        else:
            print("User not found")
            error_message = "Invalid username or password. Please try again."
            return redirect('..')
    
    return render(request, 'djangoapp/index.html', {'error_message': error_message})
        

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    if request.method == 'POST':
        logout(request)
        # Redirect to the desired page after logging out
        return redirect('..')  # Assuming 'home' is the name of your home page URL pattern
    # Handle other cases (GET request or invalid POST request)
    return redirect('..')  # Redirect to home page in other cases as well

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
def register_request(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'djangoapp/index.html', context)

    if request.method == 'POST':
        print("This was a post request!")
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        
        existing_user = User.objects.filter(username=username).first()

        if existing_user:
            print("User already exists, trying again!")
            messages.error(request, 'User already exists. Please try again.')
            return redirect('../signup')
        else:
            print("New user, registering...")
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            return redirect('..')

    print("If successful registration of a new user, this shouldn't happen...")
    return render(request, "djangoapp/index.html", context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):

    context = {}

    if request.method == "GET":
        url = "http://localhost:3300/dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        context['dealerships'] = dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):

    context = {}
    dealership = get_dealers_from_cf(f"http://localhost:3300/dealerships?dealerId={dealer_id}")
    context['dealership'] = dealership[0].full_name
    context['dealership_id'] = dealership[0].id
    if request.method == "GET":
        url = f"http://localhost:5000/review/{dealer_id}"

        reviews = get_dealer_reviews_from_cf(url)

        context['reviews'] = reviews

        return render(request, 'djangoapp/dealer_details.html', context)


# go_to_review_form
def review_form(request, dealer_id):

    context = {
        "id": dealer_id,
    }

    return render(request, "djangoapp/add_review.html", context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):

    url = "http://localhost:5000/review"
    
    json_payload = {
        "dealership": dealer_id
    }

    json_payload['id'] = get_review_id()
    json_payload['name'] = request.user.first_name + " " + request.user.last_name
    json_payload['review'] = request.POST['review']
    json_payload['purchase'] = request.POST['purchase']
    if request.POST['purchase']:
        json_payload['purchase_date'] = datetime.utcnow().isoformat()
        json_payload['car_make'] = "BMW"
        json_payload['car_model'] = "M5"
        json_payload['car_year'] = 2020
    
    result = post_request(url, json_payload)

    print(result)

    dealer_details_url = reverse('djangoapp:dealer_details', kwargs={'dealer_id': dealer_id})

    return redirect(dealer_details_url)

    


