from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import io
import os
import sys
import numpy as np
import types

# === Setup path agar bisa load model dengan benar ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "exoplanet_model.pkl")

app = FastAPI(title="ExoFinder API – CSV & JSON Prediction")

# === CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Tambahkan definisi ModelWrapper (agar joblib bisa mengenali class) ===
class ModelWrapper:
    def __init__(self, pipeline, feature_names):
        self.pipeline = pipeline
        self.feature_names_in_ = np.array(feature_names)
    def predict(self, X):
        if isinstance(X, pd.DataFrame):
            X = X[self.feature_names_in_]
        return self.pipeline.predict(X)
    def predict_proba(self, X):
        if isinstance(X, pd.DataFrame):
            X = X[self.feature_names_in_]
        if hasattr(self.pipeline, "predict_proba"):
            return self.pipeline.predict_proba(X)
        elif hasattr(self.pipeline.named_steps.get('clf'), "predict_proba"):
            return self.pipeline.named_steps['clf'].predict_proba(X)
        else:
            raise AttributeError("Underlying classifier has no predict_proba method")
    @property
    def classes_(self):
        if hasattr(self.pipeline, "classes_"):
            return self.pipeline.classes_
        elif 'clf' in self.pipeline.named_steps:
            return self.pipeline.named_steps['clf'].classes_
        return []

# Daftarkan ModelWrapper agar dikenali sebagai modul __main__
try:
    import __main__
    setattr(__main__, "ModelWrapper", ModelWrapper)
except Exception as e:
    print(f"⚠️ Warning: Failed to register ModelWrapper in __main__: {e}")

# === Load model ===
model = None
try:
    if os.path.exists(MODEL_PATH):
        print(f"🔍 Loading model from {MODEL_PATH} ...")
        model = joblib.load(MODEL_PATH)
        print(f"✅ Model loaded successfully from {MODEL_PATH}")
        if hasattr(model, "classes_"):
            print(f"   Classes: {list(model.classes_)}")
    else:
        print(f"❌ Model file not found at {MODEL_PATH}")
except Exception as e:
    import traceback
    print(f"❌ Failed to load model: {e}")
    traceback.print_exc()
    model = None


# === Mapping kolom user-friendly → NASA ===
COLUMN_MAP = {
    "orbital_period": "pl_orbper",
    "transit_depth": "pl_trandurh",
    "planet_radius": "pl_rade",
    "stellar_radius": "st_rad",
    "equilibrium_temp": "pl_eqt",
    "stellar_temp": "st_teff"
}

# === Nilai default jika kolom tidak tersedia ===
DEFAULT_VALUES = {
    "pl_eqt": 250,   # planet equilibrium temperature (K)
    "st_teff": 5700  # stellar effective temperature (K)
}

# === Fungsi prediksi ===
def make_prediction(df: pd.DataFrame):
    if model is None:
        raise RuntimeError("Model not loaded. Check model path or training output.")

    # Ganti nama kolom agar cocok dengan model
    df = df.rename(columns=COLUMN_MAP)

    # Tambahkan default value jika kolom tidak tersedia
    for col, val in DEFAULT_VALUES.items():
        if col not in df.columns:
            df[col] = val

    # Pilih fitur sesuai dengan model
    if hasattr(model, "feature_names_in_"):
        used_features = [f for f in model.feature_names_in_ if f in df.columns]
    else:
        used_features = df.columns.tolist()

    # Prediksi
    preds = model.predict(df[used_features])

    # Jika model punya classes_
    if hasattr(model, "classes_"):
        df["prediction"] = preds
    else:
        df["prediction"] = preds

    return df.to_dict(orient="records")


# === Root endpoint ===
@app.get("/")
async def root():
    return {
        "message": "🚀 ExoFinder API is running",
        "endpoints": {
            "/predict": "Upload CSV file for prediction",
            "/predict-json": "Send JSON array for prediction"
        }
    }


# === Endpoint 1: CSV upload ===
@app.post("/predict")
async def predict_csv(file: UploadFile = File(...)):
    if model is None:
        return {"error": "Model not loaded or invalid path."}

    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        result = make_prediction(df)
        return {"status": "success", "records": result}
    except Exception as e:
        return {"error": str(e)}


# === Endpoint 2: JSON input ===
@app.post("/predict-json")
async def predict_json(payload: dict = Body(...)):
    if model is None:
        return {"error": "Model not loaded or invalid path."}

    try:
        # Terima baik single dict maupun list of dicts
        if isinstance(payload, dict) and "data" in payload:
            data = payload["data"]
        elif isinstance(payload, list):
            data = payload
        else:
            data = [payload]

        df = pd.DataFrame(data)
        result = make_prediction(df)
        return {"status": "success", "records": result}
    except Exception as e:
        return {"error": str(e)}

# === Jalankan server (opsional manual) ===
# uvicorn app.main:app --reload
