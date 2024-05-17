from flask import Flask, request
from flask_cors import CORS
import json

app = Flask("List of Reviews")
CORS(app)

with open("reviews.json", "r") as reviewfile:
    data = json.load(reviewfile)

@app.route("/review/final")
def getFinalIndex():
    reviews = []
    for review in data["reviews"]:
        reviews.append(review)
    return reviews[-1].id

@app.route("/review")
def getReviews():
    reviews = []
    for review in data["reviews"]:
        reviews.append(review)
    return json.dumps({"reviews": reviews},indent=4)


@app.route("/review/<dealer>")
def getReviewsListByDealer(dealer):
    reviews = []
    for review in data['reviews']:
        if review["dealership"] == int(dealer):
            reviews.append(review)
    return json.dumps({"reviews": reviews},indent=4)

@app.route("/review", methods=["POST"])
def postNewReview():
    newReview = request.get_json()
    data["reviews"].append(newReview)
    with open("reviews.json", "w") as reviewfile:
        json.dump(data, reviewfile, indent=4)
    return json.dumps({"message": "Review added successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
