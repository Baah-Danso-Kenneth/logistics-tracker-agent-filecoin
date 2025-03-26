import joblib

def save_model(model, filename="trained_model.pkl"):
    joblib.dump(model, filename)

def load_model(filename="trained_model.pkl"):
    try:
        return joblib.load(filename)
    except FileNotFoundError:
        print("⚠️ Model file not found!")
        return None
