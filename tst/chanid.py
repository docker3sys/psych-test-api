import requests

API_KEY = "AIzaSyAxhWIQ-5bdGEp3cKTNeGRXe_Y-rqWU__U"
HANDLE = "ArturSharifov"  # без @

url = "https://www.googleapis.com/youtube/v3/search"

params = {
    "part": "snippet",
    "q": HANDLE,
    "type": "channel",
    "maxResults": 1,
    "key": API_KEY
}

r = requests.get(url, params=params)
data = r.json()

channel_id = data["items"][0]["snippet"]["channelId"]
print(channel_id)
