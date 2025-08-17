import requests
from google.transit import gtfs_realtime_pb2

url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/mnr%2Fgtfs-mnr"

response = requests.get(url)

if response.status_code == 200:
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    print("Data retrieved successfully:")
    print(feed)
else:
    print("Failed to retrieve data:")
    print(response.status_code)