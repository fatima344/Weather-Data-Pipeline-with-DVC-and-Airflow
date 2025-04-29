# src/train_model.py
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

def train_and_save():
    df = pd.read_csv("data/processed_data.csv")
    # Features and target (Temperature is normalized)
    X = df[["Humidity", "Wind Speed"]]
    y = df["Temperature"]
    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, "models/model.pkl")
    print("Model trained and saved to models/model.pkl.")

if __name__ == "__main__":
    train_and_save()
