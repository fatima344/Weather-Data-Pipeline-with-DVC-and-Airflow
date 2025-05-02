# src/generate_metrics.py
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import json

def generate_metrics():
    # Load the model and data
    model = joblib.load("models/model.pkl")
    df = pd.read_csv("data/processed_data.csv")
    
    # Features and target
    X = df[["Humidity", "Wind Speed"]]
    y = df["Temperature"]
    
    # Generate predictions
    y_pred = model.predict(X)
    
    # Calculate metrics
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    # Save metrics to JSON
    metrics = {
        "mse": mse,
        "r2": r2,
        "timestamp": pd.Timestamp.now().isoformat()
    }
    
    with open("metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
    
    print(f"Metrics saved to metrics.json: MSE={mse}, R²={r2}")

if __name__ == "__main__":
    generate_metrics()