# # Import libraries
# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# import io
# import tensorflow as tf
# from tensorflow import keras
# import numpy as np
# from tensorflow.keras.utils import img_to_array, load_img
# from flask import Flask, request, jsonify
# from PIL import Image
# import json

# # Define emotions
# EMOTIONS = {
#     0: 'MARAH',
#     1: 'JIJIK / RISIH',
#     2: 'KETAKUTAN',
#     3: 'SENANG / BAHAGIA',
#     4: 'NORMAL / BIASA-BIASA SAJA',
#     5: 'SEDIH',
#     6: 'BAHAGIA'
# }

# # Load the model
# model = keras.models.load_model('3052023-2302.h5')

# # Create the image transformation function
# def transform_image(image):
#     resized_image = image.resize((48, 48))
#     img_array = img_to_array(resized_image)
#     img_array = tf.expand_dims(img_array, 0)  # Create a batch
#     return img_array

# # Create the prediction function
# def predict(x):
#     predictions = model.predict(x)
#     score = tf.nn.softmax(predictions[0]).numpy()
#     maximum_index = np.argmax(score)
#     emotion_label = EMOTIONS[maximum_index]
#     rounded_prediction = round(score[maximum_index], 5)
#     return emotion_label, rounded_prediction

# # Create the Flask app
# app = Flask(__name__)


# @app.route("/predict_image", methods=["POST"])
# def predict_image():
#     if request.method == 'POST':
#         file = request.files.get('uploaded_file')
#         if file is None or file.filename == '':
#             return jsonify({"error": "no file"})

#         try:
#             image = Image.open(file).convert('L')
#             tensor = transform_image(image)
#             label, value = predict(tensor)

#             # Convert value to float before serialization
#             value = float(value)

#             data = {"label": label, "value": value}
#             return jsonify(data)
#         except Exception as e:
#             return jsonify({"error": str(e)})


# if __name__ == '__main__':
#     app.run(debug=True)

# Import libraries

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import io
import tensorflow as tf
from tensorflow import keras
import numpy as np
from tensorflow.keras.utils import img_to_array, load_img
from flask import Flask, request, jsonify
from PIL import Image
from google.cloud import storage

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
model = keras.models.load_model('3052023-2302.h5')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'credentials.json'

# Create the image transformation function
def transform_image(image):
    resized_image = image.resize((48, 48))
    img_array = img_to_array(resized_image)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch
    return img_array

# Create the prediction function
def predict(x):
    predictions = model.predict(x)
    score = tf.nn.softmax(predictions[0]).numpy()
    maximum_index = np.argmax(score)
    emotion_label = EMOTIONS[maximum_index]
    rounded_prediction = round(score[maximum_index], 5)
    return emotion_label, rounded_prediction

# Create the Flask app
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)


