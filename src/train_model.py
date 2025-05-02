# src/train_model.py
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import json
import os

def train_and_save():
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)
    
    df = pd.read_csv("data/processed_data.csv")
    # Features and target (Temperature is normalized)
    X = df[["Humidity", "Wind Speed"]]
    y = df["Temperature"]
    
    # Split data into train and test sets
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Make predictions and calculate metrics
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Save model
    joblib.dump(model, "models/model.pkl")
    print("Model trained and saved to models/model.pkl.")
    
    # Save metrics
    metrics = {
        "mean_squared_error": mse,
        "r2_score": r2,
        "coefficients": list(model.coef_),
        "intercept": model.intercept_,
        "timestamp": pd.Timestamp.now().isoformat()
    }
    
    with open("metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
    print("Metrics saved to metrics.json")

if __name__ == "__main__":
    train_and_save()