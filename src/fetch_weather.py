import requests
import pandas as pd
from datetime import datetime, timezone

API_KEY = "f0904a19728ff64d5246df0355df2745"
CITIES = ["Lahore", "Islamabad", "Karachi", "Quetta", "Peshawar"]

def fetch_and_save():
    data_records = []
    for city in CITIES:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        resp = requests.get(url)
        
        if resp.status_code != 200:
            print(f"Failed to fetch data for {city}, status code: {resp.status_code}")
            continue
        
        weather = resp.json()
        temp_k = weather["main"]["temp"]
        temp_c = temp_k - 273.15  # Convert from Kelvin to Celsius
        humidity = weather["main"]["humidity"]
        wind_speed = weather["wind"]["speed"]
        condition = weather["weather"][0]["description"]
        dt = datetime.fromtimestamp(weather["dt"], timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        
        data_records.append({
            "City": city,
            "Temperature": temp_c,
            "Humidity": humidity,
            "Wind Speed": wind_speed,
            "Weather": condition,
            "DateTime": dt
        })
        
    df = pd.DataFrame(data_records)
    df.to_csv("data/raw_data.csv", index=False)
    print("Saved raw_data.csv with", len(df), "records.")

if __name__ == "__main__":
    fetch_and_save()
