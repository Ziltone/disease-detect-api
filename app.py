from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)
CORS(app)

# Load Okra Disease Detection Model
model = tf.keras.models.load_model("okra_disease_cnn_finetuned.h5")
disease_classes = [
    "Healthy Leaves", "Alternaria Leaf Spot", "Cercospora Leaf Spot",
    "Downy Mildew", "Leaf Curl Virus", "Phyllosticta Leaf Spot"
]

@app.route('/')
def home():
    return "Okra Disease Detection Flask Server is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    try:
        image = Image.open(file).resize((224, 224))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)

        prediction = model.predict(image)
        predicted_class = disease_classes[np.argmax(prediction)]
        confidence = float(np.max(prediction))

        return jsonify({"disease": predicted_class, "confidence": confidence})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/healthcheck")
def healthcheck():
    return "OK", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
