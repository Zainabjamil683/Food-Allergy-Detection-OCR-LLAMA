from experta import KnowledgeEngine, Rule, Fact
from fuzzywuzzy import process

# Updated VALID_SYMPTOMS with additional symptoms and food-related triggers
VALID_SYMPTOMS = {
    # General Symptoms
    "sneezing", "runny_nose", "watery_eyes", "outdoor_exposure",
    "coughing", "wheezing", "breathlessness", "dust_exposure",
    "itching", "skin_rash", "stomach_pain", "eaten_nuts",
    "hives", "eczema", "nausea", "vomiting", "abdominal_pain",
    "shortness_of_breath", "swelling_of_face_or_throat", "anaphylaxis",
    "flushed_skin", "abdominal_cramps", "tingling_in_mouth",
    "lightheadedness", "loss_of_consciousness", "face_swelling",
    "throat_swelling", "difficulty_breathing",

    # Food-Related Triggers
    "drank_milk", "ate_eggs", "consumed_peanuts", "ate_shellfish",
    "ate_wheat", "ate_soy", "ate_fish", "ate_sesame", "ate_corn",
    "ate_mustard", "ate_lupin"
}

def correct_symptom(symptom):
    """Finds the closest valid symptom from the predefined list."""
    best_match, score = process.extractOne(symptom, VALID_SYMPTOMS)
    return best_match if score > 80 else None  # Accept only if confidence > 80%

def clean_input(data):
    """Cleans and standardizes input symptoms."""
    cleaned_data = {}
    for key, value in data.items():
        key = key.strip().lower()  # Normalize case and remove spaces
        corrected_key = correct_symptom(key)  # Fix typos
        if corrected_key:
            cleaned_data[corrected_key] = value
    return cleaned_data

class AllergyExpert(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.scores = {}

    def add_score(self, allergy, points=1):
        self.scores[allergy] = self.scores.get(allergy, 0) + points

    # Existing rules for Pollen, Dust, and Peanut allergies
    @Rule(Fact(sneezing=True))
    def pollen_1(self):
        self.add_score("Pollen Allergy", 1)

    @Rule(Fact(runny_nose=True))
    def pollen_2(self):
        self.add_score("Pollen Allergy", 1)

    @Rule(Fact(watery_eyes=True))
    def pollen_3(self):
        self.add_score("Pollen Allergy", 1)

    @Rule(Fact(outdoor_exposure=True))
    def pollen_4(self):
        self.add_score("Pollen Allergy", 1)

    @Rule(Fact(coughing=True))
    def dust_1(self):
        self.add_score("Dust Allergy", 1)

    @Rule(Fact(wheezing=True))
    def dust_2(self):
        self.add_score("Dust Allergy", 1)

    @Rule(Fact(breathlessness=True))
    def dust_3(self):
        self.add_score("Dust Allergy", 1)

    @Rule(Fact(dust_exposure=True))
    def dust_4(self):
        self.add_score("Dust Allergy", 1)

    @Rule(Fact(itching=True))
    def peanut_1(self):
        self.add_score("Peanut Allergy", 1)

    @Rule(Fact(skin_rash=True))
    def peanut_2(self):
        self.add_score("Peanut Allergy", 1)

    @Rule(Fact(stomach_pain=True))
    def peanut_3(self):
        self.add_score("Peanut Allergy", 1)

    @Rule(Fact(eaten_nuts=True))
    def peanut_4(self):
        self.add_score("Peanut Allergy", 2)

    # New rules for additional allergies
    @Rule(Fact(hives=True))
    def wheat_1(self):
        self.add_score("Wheat Allergy", 1)

    @Rule(Fact(eczema=True))
    def wheat_2(self):
        self.add_score("Wheat Allergy", 1)

    @Rule(Fact(nausea=True))
    def wheat_3(self):
        self.add_score("Wheat Allergy", 1)

    @Rule(Fact(vomiting=True))
    def wheat_4(self):
        self.add_score("Wheat Allergy", 1)

    @Rule(Fact(abdominal_pain=True))
    def wheat_5(self):
        self.add_score("Wheat Allergy", 1)

    @Rule(Fact(shortness_of_breath=True))
    def wheat_6(self):
        self.add_score("Wheat Allergy", 1)

    @Rule(Fact(ate_wheat=True))
    def wheat_7(self):
        self.add_score("Wheat Allergy", 2)  # Strong indicator

    @Rule(Fact(swelling_of_face_or_throat=True))
    def shellfish_1(self):
        self.add_score("Shellfish Allergy", 1)

    @Rule(Fact(difficulty_breathing=True))
    def shellfish_2(self):
        self.add_score("Shellfish Allergy", 1)

    @Rule(Fact(anaphylaxis=True))
    def shellfish_3(self):
        self.add_score("Shellfish Allergy", 2)

    @Rule(Fact(ate_shellfish=True))
    def shellfish_4(self):
        self.add_score("Shellfish Allergy", 2)  # Strong indicator

    @Rule(Fact(flushed_skin=True))
    def soy_1(self):
        self.add_score("Soy Allergy", 1)

    @Rule(Fact(coughing=True))
    def soy_2(self):
        self.add_score("Soy Allergy", 1)

    @Rule(Fact(abdominal_cramps=True))
    def soy_3(self):
        self.add_score("Soy Allergy", 1)

    @Rule(Fact(ate_soy=True))
    def soy_4(self):
        self.add_score("Soy Allergy", 2)  # Strong indicator

    @Rule(Fact(face_swelling=True))
    def milk_1(self):
        self.add_score("Milk Allergy", 1)

    @Rule(Fact(difficulty_breathing=True))
    def milk_2(self):
        self.add_score("Milk Allergy", 1)

    @Rule(Fact(abdominal_cramps=True))
    def milk_3(self):
        self.add_score("Milk Allergy", 1)

    @Rule(Fact(drank_milk=True))
    def milk_4(self):
        self.add_score("Milk Allergy", 2)  # Strong indicator

    @Rule(Fact(tingling_in_mouth=True))
    def egg_1(self):
        self.add_score("Egg Allergy", 1)

    @Rule(Fact(lightheadedness=True))
    def egg_2(self):
        self.add_score("Egg Allergy", 1)

    @Rule(Fact(hives=True))
    def egg_3(self):
        self.add_score("Egg Allergy", 1)

    @Rule(Fact(ate_eggs=True))
    def egg_4(self):
        self.add_score("Egg Allergy", 2)  # Strong indicator

    @Rule(Fact(swelling_of_throat=True))
    def peanut_5(self):
        self.add_score("Peanut Allergy", 2)

    @Rule(Fact(loss_of_consciousness=True))
    def peanut_6(self):
        self.add_score("Peanut Allergy", 2)

    @Rule(Fact(consumed_peanuts=True))
    def peanut_7(self):
        self.add_score("Peanut Allergy", 2)  # Strong indicator

    # Add similar rules for other allergies (Tree Nut, Fish, Sesame, Corn, Sulphite, Mustard, Lupin)
    # Example for Tree Nut Allergy:
    @Rule(Fact(hives=True))
    def tree_nut_1(self):
        self.add_score("Tree Nut Allergy", 1)

    @Rule(Fact(face_swelling=True))
    def tree_nut_2(self):
        self.add_score("Tree Nut Allergy", 1)

    @Rule(Fact(coughing=True))
    def tree_nut_3(self):
        self.add_score("Tree Nut Allergy", 1)

    @Rule(Fact(ate_nuts=True))
    def tree_nut_4(self):
        self.add_score("Tree Nut Allergy", 2)  # Strong indicator

    # Add similar rules for Fish, Sesame, Corn, Sulphite, Mustard, and Lupin allergies

    def get_top_allergy(self):
        """Returns the allergy with the highest confidence score."""
        if not self.scores:
            return ["No allergy detected."]
        sorted_allergies = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        return [f"{allergy} (confidence: {score})" for allergy, score in sorted_allergies]

def allergy_prediction(data):
    """Processes user input and returns predicted allergies."""
    cleaned_data = clean_input(data)  # Standardize input
    engine = AllergyExpert()
    engine.reset()
    for key, value in cleaned_data.items():
        if value:  # Declare only True facts
            engine.declare(Fact(**{key: value}))
    engine.run()
    return engine.get_top_allergy()