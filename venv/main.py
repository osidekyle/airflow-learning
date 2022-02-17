from pendulum import date
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite://my_played_tracks.sqlite"
USER_ID = "osidekyle"
TOKEN = "BQB-M5rv1FOU2sWFun9RlX5Jmg2YmEeyQbfy2i7I9k3wlHCvd5Oamybks78zmyGHfYqAISi5qxYm20iMd5myzFIfW3_ruTLaVeycP6qGkebHT1TJc3JUdwwQyjKTp7JBWFqKDc8PqbSM84SKa-8"

if __name__ == "__main__":
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer " + TOKEN
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after=" + str(yesterday_unix_timestamp),headers = headers)

    data = r.json()

    song_names = []
    artist_names = []
    played_at = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])


song_dict = {
    "song_name": song_names,
    "artist_name": artist_names,
    "played_at": played_at,
    "timestamp": timestamps
}

def check_if_valid_data(df: pd.DataFrame) -> bool:
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False
    
    if pd.Series(df["played_at"]).is_unique:
        pass
    else:
        raise Exception("Primary Key Check is Vioated")

    if df.isnull().values.any():
        raise Exception("Null values found")

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    print(yesterday)
    timestamps = df["timestamp"].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, "%Y-%m-%d") != yesterday:
            raise Exception("Song not from last 24 hours")

    return True

song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp"])


print(song_df)

if check_if_valid_data(song_df):
    print("Valid!")