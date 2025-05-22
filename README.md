# Food-Allergy-Detection-OCR-LLAMA
**Predict the allergy. Detect the danger. Protect your health.**  
The **Allergen Alert App** helps users predict allergies and detect food allergens before eating — whether it's packaged snacks or unpackaged meals. Designed for individuals with food sensitivities, this app makes food safety smarter and easier.

---

## 🚀 Features

- 📸 Scan **packaged food** and extract ingredients using OCR.
- 🤖 Detect **potential allergens** based on ingredients.
- 🥗 Analyze **unpackaged food** using image classification.
- 🧠 Take a **symptom-based quiz** to predict allergies.
- ☁️ Store and retrieve user allergy data using Firebase.

---

## 🛠️ Requirements

### ✅ General Requirements

- A PC/laptop with **Python 3.10** or lower  
  ⚠️ *Python 3.11+ is not supported due to model dependencies.*
- **Node.js and npm** (for OCR using `llama-ocr`)
- **React Native** development environment  
  - Expo CLI  
  - Android/iOS emulator or physical device

---

### ✅ Python Dependencies

Install all backend requirements:

```bash
pip install -r requirements.txt
````

Includes:

* Flask
* TensorFlow / Keras
* Firebase Admin SDK
* OpenCV, Pillow
* fuzzywuzzy
* experta

---

## 📁 Folder Structure

```
AllergenAlertApp/
│
├── backend/
│   ├── backend_apis.py
│   ├── backend_allergy_detection.py
│   ├── backend_apis_testing.py
│   ├── backend_pack_food_and_allergens_detection.py
│   ├── backend_unpack_food_and_allergens_detection.py
│   ├── firebase_config.json  <-- Your Firebase credentials (keep private)
│   ├── Model.h5
│   ├── backend_llama_ocr.js
│   ├── package.json
│   ├── package-lock.json
│   ├── .env                <-- Store your TOGETHER_API_KEY here
├── frontend/
│   ├── App.js
│   └── screens/
│
├── requirements.txt
└── README.md

```

---

## ⚙️ Backend Setup

Start your Flask backend:

```bash
cd backend
python backend_apis.py
```

---

## 🧾 OCR Setup (llama-ocr)

This OCR service runs on Node.js and extracts ingredients from packaged food labels.
1. First, you need to get an API key from [Together.ai](https://together.ai/) (sign up and generate your API key).

2. Set your API key as an environment variable before running the OCR server:

```bash
cd ocr-node
npm install
node backend_llama_ocr.js
```

---

## 📱 Frontend Setup (React Native)

Set up the mobile app frontend:
```bash
cd frontend
npm install
npx react-native run-android   # for Android emulator/device
# or
npx react-native run-ios       # for iOS simulator/device
````
> Make sure you have the React Native CLI installed and your emulator or device ready.
> **For Android emulator**, the backend runs on: `http://10.0.2.2:5000`
---

## 🔐 Firebase Setup

Firebase is used to store and retrieve user allergy data.

### ✅ Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add Project"** and follow the setup.
3. Navigate to **Project Settings → Service Accounts**
4. Click **"Generate new private key"** to download a `.json` credentials file.

---

### ✅ Step 2: Add to Backend

1. Rename the file to: `firebase_config.json`
2. Place it in the `backend/` folder.

---

## 🙌 Credits

* React Native (Frontend)
* Flask + Firebase (Backend)
* llama-ocr (OCR for packaged food)
* Keras (Image classification)
* fuzzywuzzy + experta (Symptom-based predictions)

---

## 📩 Need Help?

Open an issue in the repo or contact the maintainer.
If you're not sure where to start, just follow the README step by step!

```

