import os
import json
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
import pickle as pk
import numpy as np

# Load pre-trained models and data
first_check = VGG16(weights='imagenet')
second_check = pk.load(open("C:/Users/Krushnansh/CAR_damage/classifier.pickle", 'rb'))
third_check = pk.load(open("C:/Users/Krushnansh/CAR_damage/FRS/classifier.pickle", 'rb'))
fourth_check = pk.load(open("C:/Users/Krushnansh/CAR_damage/Severity/classifier.pickle", 'rb'))

with open('models/cat_counter.pk', 'rb') as f:
    cat_counter = pk.load(f)

cat_list = [k for k, v in cat_counter.most_common()[:27]]
CLASS_INDEX_PATH = 'C:/Users/Krushnansh/CAR_damage/imagenet_class_index.json'
CLASS_INDEX = None

def get_predictions(preds, top=5):
    global CLASS_INDEX
    if CLASS_INDEX is None:
        with open(CLASS_INDEX_PATH) as f:
            CLASS_INDEX = json.load(f)
    results = []
    for pred in preds:
        top_indices = pred.argsort()[-top:][::-1]
        result = [tuple(CLASS_INDEX[str(i)]) + (pred[i],) for i in top_indices]
        result.sort(key=lambda x: x[2], reverse=True)
        results.append(result)
    return results

def prepare_img_224(img_path):
    try:
        img = load_img(img_path, target_size=(224, 224))
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        return x
    except Exception as e:
        raise ValueError(f"Error loading image: {e}")

def car_categories_check(img_224, model):
    out = model.predict(img_224)
    top = get_predictions(out, top=5)
    for j in top[0]:
        if j[0:2] in cat_list:
            return True
    return False

def car_damage_check(img_path, classifier):
    base_model = first_check
    train_labels = ['Damaged', 'Not Damaged']
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

    img = prepare_img_224(img_path)
    feature = model.predict(img)
    flat = feature.flatten()
    flat = np.expand_dims(flat, axis=0)
    preds = classifier.predict(flat)
    return train_labels[preds[0]]

def location_assessment(img_path, classifier):
    base_model = first_check
    train_labels = ['Front Damage', 'Rear Damage', 'Side Damage']
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

    img = prepare_img_224(img_path)
    feature = model.predict(img)
    flat = feature.flatten()
    flat = np.expand_dims(flat, axis=0)
    preds = classifier.predict(flat)
    return train_labels[preds[0]]

def severity_assessment(img_path, classifier):
    base_model = first_check
    train_labels = ['Minor Damage', 'Moderate Damage', 'Severe Damage']
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

    img = prepare_img_224(img_path)
    feature = model.predict(img)
    flat = feature.flatten()
    flat = np.expand_dims(flat, axis=0)
    preds = classifier.predict(flat)
    return train_labels[preds[0]]

def engine(img_path):
    report = []
    try:
        img_224 = prepare_img_224(img_path)
        if not car_categories_check(img_224, first_check):
            return "The image is not recognized as a car. Please try another image."

        damage_status = car_damage_check(img_path, second_check)
        report.append(f"Damage Status: {damage_status}")
        if damage_status == "Not Damaged":
            return "\n".join(report)

        damage_location = location_assessment(img_path, third_check)
        report.append(f"Damage Location: {damage_location}")

        damage_severity = severity_assessment(img_path, fourth_check)
        report.append(f"Damage Severity: {damage_severity}")

    except Exception as e:
        return f"An error occurred: {e}"

    return "\n".join(report)
print(engine())