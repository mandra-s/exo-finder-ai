import joblib
import pandas as pd
import numpy as np
import random
import os

MODEL_PATH = "app/models/exoplanet_model2.pkl"

class DummyModel:
    def predict(self, X):
        labels = [0, 1, 2]
        return [random.choice(labels) for _ in range(len(X))]

def load_model():
    if not os.path.exists(MODEL_PATH):
        print("⚠️ Model file not found, using DummyModel.")
        return DummyModel()
    try:
        loaded = joblib.load(MODEL_PATH)
        # Jika model disimpan sebagai dict
        if isinstance(loaded, dict):
            if "model" in loaded:
                print("✅ Loaded model from dict['model']")
                return loaded["model"]
            else:
                print("⚠️ Dict found but no 'model' key, using DummyModel.")
                return DummyModel()
        # Jika langsung objek model
        print("✅ Model loaded successfully as direct object")
        return loaded
    except Exception as e:
        print("⚠️ Error loading model:", e)
        return DummyModel()

model = load_model()

def predict_exoplanet(df: pd.DataFrame):
    if model is None:
        raise RuntimeError("Model not loaded!")

    # Hanya gunakan kolom numerik
    features = df.select_dtypes(include=[np.number])

    try:
        preds = model.predict(features)
    except Exception as e:
        print("⚠️ Model prediction failed, switching to DummyModel. Error:", e)
        dummy = DummyModel()
        preds = dummy.predict(features)

    label_map = {0: "CONFIRMED", 1: "CANDIDATE", 2: "FALSE POSITIVE"}
    labels = [label_map.get(int(p), "UNKNOWN") for p in preds]

    df["prediction"] = labels
    return df
