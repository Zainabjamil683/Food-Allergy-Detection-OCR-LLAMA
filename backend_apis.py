from flask import Flask, request, jsonify
import numpy as np
from PIL import Image
import io
import subprocess
import re
import cv2
import requests

from backend_allergy_detection import allergy_prediction
from backend_pack_food_and_allergens_detection import pf_allergens_db
from backend_unpack_food_and_allergens_detection import preprocess_image,model,classes,upf_allergen_db
from firebase_admin import firestore, initialize_app
from firebase_admin import credentials

# Initialize Firebase with credentials
cred = credentials.Certificate("D:\\FYP\\AllergenAlert_Backend\\awesomeproject-cbf74-firebase-adminsdk-fbsvc-1bb1c7e154.json")  # Replace with the path to your JSON file
# Initialize Firebase
initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

@app.route('/predict_allergy', methods=['POST'])
def predict_allergy():
    data = request.get_json()
    
    # Check if JSON was received properly
    if data is None:
        return jsonify({"error": "Invalid or missing JSON data"}), 400  # Return an error response

    prediction = allergy_prediction(data)

    if not prediction or prediction == ["No allergy detected."]:
        return jsonify({"message": "No significant allergy detected"}), 200  # Explicit response for no allergies
    
    return jsonify({"predicted_allergies": prediction})



# @app.route("/process_image_pf", methods=["POST"])
# def process_image_pf():
#     data = request.json
#     image_path = data.get("image_path")  # Expecting a path from request JSON
#     print(image_path)

#     if not image_path:
#         return jsonify({"error": "Image path is required"}), 400

#     try:
#         result = subprocess.run(
#             ["node", "--no-deprecation", "backend_llama_ocr.js", image_path],
#             capture_output=True, text=True, check=True
#         )
#         ocr_text = result.stdout.strip()  # Get OCR result from stdout
#     except subprocess.CalledProcessError as e:
#         return jsonify({"error": f"OCR failed: {e.stderr}"}), 500

#     return jsonify({"ocr_output": ocr_text})  # Return OCR result as JSON

@app.route("/process_image_pf", methods=["POST"])
def process_image_pf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    image_path = "temp_image.jpg"  # Temporary file for OCR
    file.save(image_path)

    try:
        result = subprocess.run(
            ["node", "--no-deprecation", "backend_llama_ocr.js", image_path],
            capture_output=True, text=True, check=True
        )
        ocr_text = result.stdout.strip()
        print(ocr_text)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"OCR failed: {e.stderr}"}), 500

    return jsonify({"ocr_output": ocr_text})

# Prediction endpoint: Accepts an image and returns the predicted food name and confidence
@app.route("/process_image_upf", methods=["POST"])
def process_image_upf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    image = Image.open(io.BytesIO(file.read()))
    
    # Preprocess the image
    processed_image = preprocess_image(image)
    
    # Make prediction
    predictions = model.predict(processed_image)
    predicted_class = np.argmax(predictions)
    confidence = float(np.max(predictions))
    print("hello",predicted_class)

    return jsonify({
        "prediction": classes[predicted_class],
        "confidence": confidence
    })


@app.route("/allergens_pf", methods=["POST"])
def allergens_pf():
    # ✅ Get OCR output directly from request
    ocr_text = request.json.get("ocr_output", "").lower()
    
    if not ocr_text:
        return jsonify({"error": "No OCR text provided"}), 400
    
    detected_allergies = {}

    for allergy, details in pf_allergens_db.items():
        matching_ingredients = set()
        
        for ingredient in details["Ingredients"] + details["HiddenNames"]:
            pattern = re.compile(re.escape(ingredient), re.IGNORECASE)
            if pattern.search(ocr_text):
                matching_ingredients.add(ingredient)
        
        if matching_ingredients:
            detected_allergies[allergy] = list(matching_ingredients)
    
    if detected_allergies:
        return jsonify({"allergies_detected": detected_allergies})
    else:
        return jsonify({"message": "This product is safe to eat!"})


@app.route("/allergens_upf", methods=["POST"])
def allergens_upf():
    data = request.get_json()
    if not data or "prediction" not in data:
        return jsonify({"error": "No food name provided"}), 400

    food_name = data["prediction"].strip().lower()
    if food_name not in upf_allergen_db:
        return jsonify({"error": f"'{food_name}' not found in the allergen database."}), 404

    food_info = upf_allergen_db[food_name]
    print(food_name)
    return jsonify({
        "food": food_name,
        "allergens": food_info["allergens"],
        "notes": food_info.get("notes", "")
    })



# Mock function to fetch user allergies (since no DB setup)
def fetch_user_allergies():
    # Mimicking a user who is allergic to peanuts, dairy, and gluten
    return ["Peanut", "Dairy", "Gluten", "Dextrose"]


import random

# Mock function to fetch user allergies (since no DB setup)
def fetch_user_allergies(user_id):
    """
    Fetch the user's allergies from Firestore.
    """
    try:
        # Reference to the user's allergies subcollection
        user_allergies_ref = db.collection("users").document(user_id).collection("allergies")
        
        # Fetch all documents in the allergies subcollection
        user_allergies_snapshot = user_allergies_ref.get()
        
        # Extract allergy names from the documents
        user_allergies = [doc.to_dict()["allergyName"] for doc in user_allergies_snapshot]
        return user_allergies
    except Exception as e:
        print("Error fetching user allergies:", e)
        return []  # Return an empty list if there's an error

@app.route("/safe_unsafe_check", methods=["POST"])
def safe_unsafe_check():
    data = request.get_json()
    
    if not data or "allergens_detected" not in data or "user_id" not in data:
        return jsonify({"error": "No allergens detected data or user ID provided"}), 400
    
    detected_allergens = data["allergens_detected"]  # Output from allergens_pf or allergens_upf
    user_id = data["user_id"]  # Get user ID from request

    # Fetch user allergies from Firestore
    user_allergies = fetch_user_allergies(user_id)

    matched_allergens = []

    # Handle the case where detected_allergens is a list of dictionaries
    if isinstance(detected_allergens, list):
        detected_allergen_names = [allergen["name"] for allergen in detected_allergens if "name" in allergen]
    else:
        detected_allergen_names = list(detected_allergens.keys())  # Keep original support for packaged food
    
    for allergy in user_allergies:
        for detected_allergy in detected_allergen_names:
            if allergy.lower() in detected_allergy.lower():
                matched_allergens.append({
                    "allergy": allergy,
                    "item": detected_allergy,  # Include the item name that caused the allergy
                })
    
    if matched_allergens:
        print(matched_allergens)
        return jsonify({
            "status": "unsafe",
            "message": "This food contains allergens that you are sensitive to.",
            "matched_allergens": matched_allergens,  # Include both allergy and item name
        })
    else:
        print(matched_allergens)
        return jsonify({
            "status": "safe",
            "message": "This food appears to be safe for you to eat!",
        })
    
    # Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)



