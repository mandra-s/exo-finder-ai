// === ExoFinder Frontend Integration ===
// Mendukung dua mode input: CSV upload & JSON form input

const API_BASE = "http://127.0.0.1:8000"; // Pastikan backend FastAPI berjalan di port ini

// === Elemen DOM ===
const csvInput = document.getElementById("csv_file");
const predictCSVBtn = document.getElementById("predict_csv_btn");
const predictJSONBtn = document.getElementById("predict_json_btn");
const resultDiv = document.getElementById("result");

// Input manual form
const orbitalPeriod = document.getElementById("orbital_period");
const transitDepth = document.getElementById("transit_depth");
const planetRadius = document.getElementById("planet_radius");
const stellarRadius = document.getElementById("stellar_radius");
const equilibriumTemp = document.getElementById("equilibrium_temp");
const stellarTemp = document.getElementById("stellar_temp");

// === Utility: tampilkan hasil ===
function displayResult(result) {
  resultDiv.innerHTML = "";

  if (result.error) {
    resultDiv.innerHTML = `<p style="color:red;">⚠️ Error: ${result.error}</p>`;
    if (result.hint) resultDiv.innerHTML += `<p>${result.hint}</p>`;
    return;
  }

  if (result.status === "success") {
    resultDiv.innerHTML = `
      <h3>✅ Prediction Results:</h3>
      <pre>${JSON.stringify(result.records, null, 2)}</pre>
    `;
  } else {
    resultDiv.innerHTML = `<p>⚠️ Unexpected response:</p><pre>${JSON.stringify(result, null, 2)}</pre>`;
  }
}

// === MODE 1: Upload CSV ===
predictCSVBtn.addEventListener("click", async () => {
  if (!csvInput.files.length) {
    alert("Please select a CSV file first!");
    return;
  }

  const formData = new FormData();
  formData.append("file", csvInput.files[0]);

  resultDiv.innerHTML = "⏳ Uploading and predicting from CSV...";

  try {
    const response = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      body: formData
    });

    const result = await response.json();
    displayResult(result);
  } catch (err) {
    resultDiv.innerHTML = `<p style="color:red;">❌ Failed to connect to backend.</p>`;
    console.error(err);
  }
});

// === MODE 2: Manual JSON Input ===
predictJSONBtn.addEventListener("click", async () => {
  const data = {
    orbital_period: parseFloat(orbitalPeriod.value),
    transit_depth: parseFloat(transitDepth.value),
    planet_radius: parseFloat(planetRadius.value),
    stellar_radius: parseFloat(stellarRadius.value),
    equilibrium_temp: parseFloat(equilibriumTemp.value),
    stellar_temp: parseFloat(stellarTemp.value)
  };

  resultDiv.innerHTML = "⏳ Sending data for prediction...";

  try {
    const response = await fetch(`${API_BASE}/predict-json`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    displayResult(result);
  } catch (err) {
    resultDiv.innerHTML = `<p style="color:red;">❌ Failed to connect to backend.</p>`;
    console.error(err);
  }
});
