
"""Importing Flask"""

from flask import Flask
import EmotionDetection.emotion_detection as ed

app = Flask(__name__)

"""Defining Emotion Detector"""
@app.route("/emotionDetector")
def display():
    """Defining Display"""
    text = "I think I am having fun"
    data =  ed.emotion_detector(text)
    result = ed.emotion_predictor(data)

    try:
        if text:
            pass
    except FileNotFoundError:
        return "Invalid text! Please try again!"
    try:
        if result:
            return result
    except FileNotFoundError:
        return data, 400

    return result
