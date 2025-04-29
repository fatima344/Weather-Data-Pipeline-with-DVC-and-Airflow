import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def preprocess_and_save():
    # Load the raw data (ensure the file exists before processing)
    df = pd.read_csv("data/raw_data.csv")
    
    # Check if there are any missing values, and handle them
    df = df.fillna(method="ffill")  # Simple forward-fill for demonstration
    # Check if the columns exist before processing them (in case there's an issue with the data)
    if 'Temperature' in df.columns and 'Wind Speed' in df.columns:
        # Normalize Temperature and Wind Speed to the range [0, 1]
        scaler = MinMaxScaler()

        # Ensure that the columns are numeric (handle cases where data might be improperly formatted)
        df[['Temperature', 'Wind Speed']] = df[['Temperature', 'Wind Speed']].apply(pd.to_numeric, errors='coerce')
        
        # Normalize numerical columns
        df[['Temperature', 'Wind Speed']] = scaler.fit_transform(df[['Temperature', 'Wind Speed']])

        # Convert Temperature from Kelvin to Celsius, and round to the nearest integer
        df['Temperature'] = (df['Temperature'] * (df['Temperature'].max() - df['Temperature'].min()) + df['Temperature'].min())
        df['Temperature'] = df['Temperature'].apply(lambda x: round(x, 0))  # Round to nearest integer
        
        # Save the processed data
        df.to_csv("data/processed_data.csv", index=False)
        print("Processed data saved to data/processed/processed_data.csv")
    else:
        print("Error: 'Temperature' or 'Wind Speed' columns missing.")

if __name__ == "__main__":
    preprocess_and_save()
