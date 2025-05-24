
import numpy as np
from keras.models import load_model
from keras.applications.xception import preprocess_input


# Load the trained model
MODEL_PATH = "Model.h5"
model = load_model(MODEL_PATH)

# Define class labels (same as used during training)
classes = [
    "burger", "butter_naan", "chai", "chapati", "chole_bhature",
    "dal_makhani", "dhokla", "fried_rice", "idli", "jalebi",
    "kaathi_rolls", "kadai_paneer", "kulfi", "masala_dosa", "momos",
    "paani_puri", "pakode", "pav_bhaji", "pizza", "samosa"
]

# Allergen database (food name mapped to allergen info)
upf_allergen_db = {
    "burger": {
        "allergens": [
            {"name": "Gluten", "allergy_type": "Gluten"},
            {"name": "Dairy", "allergy_type": "Dairy"},
            {"name": "Egg", "allergy_type": "Egg"},
            {"name": "Soy", "allergy_type": "Soy"}
        ],
        "notes": "Typically has a wheat bun, cheese, and may contain egg-based sauces or patties."
    },
    "butter_naan": {
        "allergens": [
            {"name": "Gluten", "allergy_type": "Gluten"},
            {"name": "Dairy", "allergy_type": "Dairy"}
        ],
        "notes": "Made with wheat flour and butter."
    },
    "chai": {
        "allergens": [
            {"name": "Milk", "allergy_type": "Milk"}
        ],
        "notes": "Traditionally prepared with milk; spices are generally non-allergenic."
    },
    "chapati": {
        "allergens": [
            {"name": "Gluten", "allergy_type": "Gluten"}
        ],
        "notes": "Prepared from whole wheat flour."
    },
    "chole_bhature": {
        "allergens": [
            {"name": "Gluten", "allergy_type": "Gluten"},
            {"name": "Legumes", "allergy_type": "Legume"},
            {"name": "Dairy", "allergy_type": "Dairy"}
        ],
        "notes": "Bhature is wheat-based and chole is made from chickpeas; sometimes contains dairy like ghee."
    },
    "dal_makhani": {
        "allergens": [
            {"name": "Legumes", "allergy_type": "Legume"},
            {"name": "Dairy", "allergy_type": "Dairy"}
        ],
        "notes": "Made with lentils and kidney beans, enriched with cream and butter."
    },
    "dhokla": {
        "allergens": [
            {"name": "Legumes", "allergy_type": "Legume"}
        ],
        "notes": "Prepared using chickpea flour (besan), a legume-based ingredient."
    },
    "fried_rice": {
        "allergens": [
            {"name": "Soy", "allergy_type": "Soy"},
            {"name": "Egg", "allergy_type": "Egg"},
            {"name": "Gluten", "allergy_type": "Gluten"}
        ],
        "notes": "May include soy sauce (which can contain gluten), egg, and other wheat-based additives."
    },
    "idli": {
        "allergens": [
            {"name": "Legumes", "allergy_type": "Legume"}
        ],
        "notes": "Fermented batter primarily from rice and urad dal (black gram)."
    },
    "jalebi": {
        "allergens": [
            {"name": "Gluten", "allergy_type": "Gluten"},
            {"name": "Dairy", "allergy_type": "Dairy"}
        ],
        "notes": "Made from refined wheat flour; sometimes prepared with ghee or milk in the batter or syrup."
    },
    "kaathi_rolls": {
        "allergens": [
            {"name": "Gluten", "allergy_type": "Gluten"},
            {"name": "Dairy", "allergy_type": "Dairy"},
            {"name": "Egg", "allergy_type": "Egg"}
        ],
        "notes": "The wrap is wheat-based and sauces may include dairy; some variations include egg."
    },
    "kadai_paneer": {
        "allergens": [
            {"name": "Dairy", "allergy_type": "Dairy"},
            {"name": "Nuts", "allergy_type": "Nuts"}
        ],
        "notes": "Paneer is a dairy product and some recipes use cashew paste in the gravy."
    },
    "kulfi": {
        "allergens": [
            {"name": "Dairy", "allergy_type": "Dairy"},
            {"name": "Nuts", "allergy_type": "Nuts"}
        ],
        "notes": "A frozen dessert made predominantly from milk and cream, often garnished with pistachios or almonds."
    },
    "masala_dosa": {
        "allergens": [
            {"name": "Legumes", "allergy_type": "Legume"},
            {"name": "Dairy", "allergy_type": "Dairy"}
        ],
        "notes": "Fermented batter of rice and lentils, often served with ghee or butter."
    },
    "momos": {
        "allergens": [
            {"name": "Gluten", "allergy_type": "Gluten"}
        ],
        "notes": "Dumplings with a wheat-based wrapper; additional allergens depend on the filling and dipping sauce."
    },
    "paani_puri": {
        "allergens": [
            {"name": "Gluten", "allergy_type": "Gluten"}
        ],
        "notes": "Crispy puri shells typically made from wheat flour."
    },
    "pakode": {
        "allergens": [
            {"name": "Legumes", "allergy_type": "Legume"},
            {"name": "Gluten", "allergy_type": "Gluten"}
        ],
        "notes": "Often made with chickpea flour (besan) and may include wheat flour in the batter."
    },
    "pav_bhaji": {
        "allergens": [
            {"name": "Gluten", "allergy_type": "Gluten"},
            {"name": "Dairy", "allergy_type": "Dairy"}
        ],
        "notes": "Pav is a wheat-based bread and the bhaji is enriched with butter."
    },
    "pizza": {
        "allergens": [
            {"name": "Gluten", "allergy_type": "Gluten"},
            {"name": "Dairy", "allergy_type": "Dairy"},
            {"name": "Soy", "allergy_type": "Soy"},
            {"name": "Egg", "allergy_type": "Egg"}
        ],
        "notes": "The crust is typically made from wheat, topped with cheese; some dough recipes or processed toppings may include soy or egg."
    },
    "samosa": {
        "allergens": [
            {"name": "Wheat", "allergy_type": "wheat"},
            {"name": "Dairy", "allergy_type": "Dairy"}
        ],
        "notes": "Fried pastry made with wheat flour and often prepared with butter or ghee."
    }
}

# Function to preprocess images for model prediction
def preprocess_image(image):
    image = image.resize((299, 299))  # Resize to match model input
    image = np.array(image)
    image = preprocess_input(image)   # Apply Xception preprocessing
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image
