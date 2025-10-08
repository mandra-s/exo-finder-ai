# 🔭 ExoFinder: AI-Powered Exoplanet Classifier

### 🌌 NASA Space Apps Challenge 2025  
**HME ITENAS:** ExoFinder | Category: “A World Away: Hunting for Exoplanets with AI”

---

## 🪐 Project Overview

**ExoFinder** is an interactive web platform powered by **Machine Learning** and **NASA’s open exoplanet datasets (Kepler, K2, TESS)**.  
Our mission is to **help scientists, students, and enthusiasts** classify potential exoplanets into three categories:

- 🟢 **Confirmed Planet**  
- 🟡 **Candidate Planet**  
- 🔴 **False Positive**

The model analyzes orbital, stellar, and planetary parameters (such as orbital period, radius, and equilibrium temperature) to predict classification outcomes — all through an easy-to-use web interface.

---

## 🧠 How It Works

1. **Data Source:**  
   Based on NASA’s public datasets:
   - [Kepler](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=cumulative)
   - [K2](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=k2pandc)
   - [TESS](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=TOI)

2. **Machine Learning Model:**  
   - Model: `RandomForestClassifier` wrapped with a custom `ModelWrapper`
   - Trained on merged dataset of Kepler, K2, and TESS
   - Features used:
     - `pl_orbper` – Orbital period (days)
     - `pl_trandurh` – Transit duration (hours)
     - `pl_rade` – Planet radius (Earth radii)
     - `st_rad` – Stellar radius (Solar radii)
     - `pl_eqt` – Equilibrium temperature (K)
     - `st_teff` – Stellar effective temperature (K)
   - Output: `CONFIRMED`, `CANDIDATE`, or `FALSE POSITIVE`
   - Includes confidence probabilities (`predict_proba`)

3. **Backend (FastAPI):**
   - Python-based REST API
   - Endpoints:
     - `/predict` → Upload CSV file
     - `/predict-json` → Send JSON data
   - Supports CORS (for easy integration with web frontends)

4. **Frontend (HTML/JS):**
   - Simple, responsive UI using pure HTML, CSS, and JS
   - Users can:
     - Input parameters manually
     - Upload CSV file for batch predictions
   - Displays prediction results and confidence visualization using Chart.js

---
