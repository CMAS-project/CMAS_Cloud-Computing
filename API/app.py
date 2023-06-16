import random
import json
import pickle
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import io
import tensorflow as tf
import nltk
import googlemaps
import requests

from tensorflow import keras
from tensorflow.keras.utils import img_to_array, load_img
from PIL import Image
from PIL import ImageOps
from google.cloud import storage
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from flask import Flask, request, jsonify

app = Flask(__name__)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'credentials.json'

# Model Predict Image Scan Emotion
# Define emotions
EMOTIONS = {
    0: 'MARAH',
    1: 'JIJIK / RISIH',
    2: 'KETAKUTAN',
    3: 'SENANG / BAHAGIA',
    4: 'NORMAL / BIASA-BIASA SAJA',
    5: 'SEDIH',
    6: 'BAHAGIA'
}

# Load the model
model_predict_image = keras.models.load_model('3052023-2302.h5')
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'credentials.json'

# Create the image transformation function
def transform_image(image):
    resized_image = image.resize((48, 48))
    img_array = img_to_array(resized_image)
    img_array = tf.expand_dims(img_array, 0)
    # grayscale_image = ImageOps.grayscale(resized_image)
    # img_array = img_to_array(grayscale_image) / 255.0
    # img_array = np.expand_dims(img_array, axis=0)

    return img_array

    # resized_image = image.resize((48, 48))
    # img_array = img_to_array(resized_image)
    # img_array = tf.expand_dims(img_array, axis=0)  # Create a batch
    # return img_array

# Create the prediction function
def predict(x):
    predictions = model_predict_image.predict(x)
    score = tf.nn.softmax(predictions[0]).numpy()
    maximum_index = np.argmax(score)
    emotion_label = EMOTIONS[maximum_index]
    rounded_prediction = round(score[maximum_index], 5)
    return emotion_label, rounded_prediction


# Create the Google Cloud Storage client
storage_client = storage.Client()

def upload_to_cloud_storage(file):
    bucket_name = 'scanemo'
    destination_blob_name = file.filename

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file)

    image_url = f"https://storage.googleapis.com/{bucket_name}/{destination_blob_name}"
    return image_url

@app.route("/predict_image", methods=["POST"])
def predict_image():
    if request.method == 'POST':
        file = request.files.get('uploaded_file')
        if file is None or file.filename == '':
            return jsonify({"error": "no file"})

        try:
            image_url = upload_to_cloud_storage(file)
            image = Image.open(file).convert('L')
            tensor = transform_image(image)
            label, value = predict(tensor)

            # Convert value to float before serialization
            value = float(value)

            data = {"label": label, "value": value, "image_url": image_url}
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})


# Model ChatBot

nltk.download('wordnet')
nltk.download('punkt')
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("Silahkan berbicara dengan teman kita Ini")

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    message = data['message']
    ints = predict_class(message)
    res = get_response(ints, intents)
    response = {'response': res}

    return jsonify(response)


# Maps Endpoint
API_KEY = 'AIzaSyCguJFD_30R_if-dbXuIUXEG71j1Fhuxjo'
gmaps = googlemaps.Client(key=API_KEY)

@app.route('/nearby_hospitals', methods=['GET'])
def get_nearby_hospitals():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    try:
        # Membuat permintaan ke Google Places API untuk mendapatkan rumah sakit terdekat
        places_result = gmaps.places_nearby(
            location=(latitude, longitude),
            radius=5000,
            type='hospital'
        )

        hospitals = []
        for place in places_result['results']:
            hospital = {
                'name': place['name'],
                'latitude': place['geometry']['location']['lat'],
                'longitude': place['geometry']['location']['lng']
            }
            hospitals.append(hospital)

        return jsonify({'hospitals': hospitals})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# News Endpoint

@app.route('/news/mental-health', methods=['GET'])
def get_mental_health_news():
    api_key = 'f7682ca0b76b4bb6a89cffdfc059f102'
    url = f'https://newsapi.org/v2/everything?q=mental%20health&apiKey={api_key}'

    response = requests.get(url)
    news_data = response.json()

    articles = news_data.get('articles', [])

    # Mengambil atribut yang relevan dari setiap artikel
    results = []
    for article in articles:
        title = article.get('title')
        description = article.get('description')
        url = article.get('url')

        result = {
            'title': title,
            'description': description,
            'url': url
        }
        results.append(result)

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)