import requests as r
import json

def emotion_detector(text_to_analyse):

    url ='https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    data =  { "raw_document": { "text": text_to_analyse } }

    # Sending a text and recieving a response
    response = r.post(url, headers=header, json=data, timeout=10)

    # Extracting all text from response
    text_data = response.text

    return text_data


def emotion_predictor(text_data):
    # Converting text data to dictionary using json library
    json_data = json.loads(text_data)

    # Fetching the emotionPredictions key from the output
    emotion_set = json_data["emotionPredictions"]

    # Fetching the First index of emotionPredictions and from that we are fetching emotion key
    emotion = emotion_set[0]["emotion"]

    # Returning dictionary
    dominant_emotion =""
    greatest_emotion = 0

    for i in emotion.keys():
        if emotion[i] > greatest_emotion:
            greatest_emotion = emotion[i]
            dominant_emotion = i

    emotion["dominant_emotion"] = dominant_emotion

    return emotion


data = emotion_detector("I am so happy I am doing this.")

print(emotion_predictor(data))