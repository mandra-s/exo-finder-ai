import joblib
import inspect
import os

MODEL_PATH = "app/models/exoplanet_model2.pkl"  # sesuaikan jika perlu

def inspect_model(model, level=0):
    indent = "  " * level
    if isinstance(model, dict):
        print(f"{indent}- Dictionary dengan {len(model)} key:")
        for k, v in model.items():
            print(f"{indent}  • {k}: {type(v)}")
            inspect_model(v, level + 1)
    elif hasattr(model, "predict"):
        print(f"{indent}- Objek model dengan method .predict() ({type(model)})")
        params = None
        try:
            params = model.get_params()
            print(f"{indent}  Parameter model:")
            for key, value in list(params.items())[:10]:  # tampilkan 10 saja
                print(f"{indent}    {key}: {value}")
        except Exception:
            pass
    else:
        print(f"{indent}- Tipe lain: {type(model)}")

def main():
    if not os.path.exists(MODEL_PATH):
        print(f"❌ File model tidak ditemukan di: {MODEL_PATH}")
        return

    try:
        print(f"🔍 Memuat model dari: {MODEL_PATH}")
        model = joblib.load(MODEL_PATH)
        print(f"✅ Berhasil dimuat: {type(model)}\n")
        inspect_model(model)
    except Exception as e:
        print("❌ Gagal memuat model:")
        print(e)

if __name__ == "__main__":
    main()
