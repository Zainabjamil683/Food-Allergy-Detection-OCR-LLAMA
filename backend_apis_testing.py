
import requests
import json

def test_predict_allergy():
    url = "http://127.0.0.1:5000/predict_allergy"
    test_data = {
        "drank_milk": True,
        "ate_eggs": True,
    "face_swelling": True,
    "difficulty_breathing": True
    }
    response = requests.post(url, json=test_data)
    try:
        response_data = response.json()
        print("Test Predict Allergy Response:", response_data)
    except json.JSONDecodeError:
        print("Error: Invalid JSON response from predict_allergy API")

def test_process_image_pf():
    url = "http://127.0.0.1:5000/process_image_pf"
    test_data = {"image_path": r"D:\\AllergenAlert_Backend - Copy\\test_data\\packaged_food_img.jpg"}
    response = requests.post(url, json=test_data)
    try:
        response_data = response.json()
        print("Test Process Image PF Response:", response_data)
        return response_data  # Output goes to allergens_pf
    except json.JSONDecodeError:
        print("Error: Invalid JSON response from process_image_pf API")

def test_allergens_pf(process_image_pf_output):
    url = "http://127.0.0.1:5000/allergens_pf"
    response = requests.post(url, json=process_image_pf_output)
    try:
        response_data = response.json()
        print("Test Allergens PF Response:", response_data)
        return response_data  # Output goes to safe_unsafe_check
    except json.JSONDecodeError:
        print("Error: Invalid JSON response from allergens_pf API")

def test_process_image_upf():
    url = "http://127.0.0.1:5000/process_image_upf"

    with open(r"D:\\FYP\AllergenAlert_Backend\\test_data\\samosa.jpg", "rb") as img_file:
        files = {"file": img_file}
        response = requests.post(url, files=files)
        try:
            response_data = response.json()
            print("Test Process Image UPF Response:", response_data)
            return response_data.get("prediction", "")  # Output goes to allergens_upf
        except json.JSONDecodeError:
            print("Error: Invalid JSON response from process_image_upf API")

def test_allergens_upf(food_name):
    url = "http://127.0.0.1:5000/allergens_upf"
    test_data = {"prediction": food_name}
    response = requests.post(url, json=test_data)
    try:
        response_data = response.json()
        print("Test Allergens UPF Response:", response_data)
        return response_data  # Output goes to safe_unsafe_check
    except json.JSONDecodeError:
        print("Error: Invalid JSON response from allergens_upf API")

def test_safe_unsafe_check(allergens_detected):
    url = "http://127.0.0.1:5000/safe_unsafe_check"
    response = requests.post(url, json={"allergens_detected": allergens_detected})
    try:
        response_data = response.json()
        print("Test Safe/Unsafe Check Response:", response_data)
    except json.JSONDecodeError:
        print("Error: Invalid JSON response from safe_unsafe_check API")

if __name__ == "__main__":

#    test_predict_allergy()
#     # Test packaged food flow
    # process_image_pf_output = test_process_image_pf()
    # if process_image_pf_output:
    #     allergens_pf_output = test_allergens_pf(process_image_pf_output)
    #     if allergens_pf_output:
    #         test_safe_unsafe_check(allergens_pf_output.get("allergies_detected", {}))

    # Test unpackaged food flow
    food_name = test_process_image_upf()
    if food_name:
        allergens_upf_output = test_allergens_upf(food_name)
        if allergens_upf_output:
            test_safe_unsafe_check(allergens_upf_output.get("allergens", {}))

