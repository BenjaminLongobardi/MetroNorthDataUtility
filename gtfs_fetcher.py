import requests
from google.transit import gtfs_realtime_pb2
from datetime import datetime
import time

class GTFSFetcher:
    def __init__(self, api_url):
        self.api_url = api_url
        
    def fetch_feed(self):
        """Fetch and parse the GTFS-RT feed"""
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            
            # Parse the protobuf data
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            
            return feed
        except requests.exceptions.RequestException as e:
            print(f"Error fetching feed: {e}")
            return None