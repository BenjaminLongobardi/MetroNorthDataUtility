import requests
import time
import datetime
import pandas as pd
import gtfs_realtime_pb2
import os
from google.protobuf.message import DecodeError
from rich.console import Console
from rich.table import Table

# Constants
API_KEY = os.environ.get("MTA_API_KEY")
MNRR_FEED_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/mnr%2Fgtfs-mnr"
NEW_HAVEN_LINE_IDS = ["1", "3"] # New Haven line and New Haven express line IDs

def get_feed():
    """Fetch the GTFS-RT feed from the MTA API."""
    if not API_KEY:
        raise ValueError("MTA_API_KEY environment variable not set")
        
    headers = {"x-api-key": API_KEY}
    response = requests.get(MNRR_FEED_URL, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code} {response.text}")
        
    feed = gtfs_realtime_pb2.FeedMessage()
    try:
        feed.ParseFromString(response.content)
        return feed
    except DecodeError as e:
        raise Exception(f"Failed to parse feed: {e}")

def format_timestamp(timestamp):
    """Convert UNIX timestamp to readable format."""
    return datetime.datetime.fromtimestamp(timestamp).strftime('%I:%M %p')

def get_new_haven_trains():
    """Get all New Haven line trains currently active."""
    feed = get_feed()
    
    trains = []
    current_time = int(time.time())
    
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            trip = entity.trip_update.trip
            route_id = trip.route_id
            
            # Filter for New Haven line trains
            if route_id in NEW_HAVEN_LINE_IDS:
                trip_id = trip.trip_id
                train_id = trip.trip_id.split("_")[1] if "_" in trip.trip_id else trip.trip_id
                
                # Find matching vehicle position for this trip
                vehicle_position = next((e.vehicle for e in feed.entity 
                                       if e.HasField('vehicle') and 
                                       e.vehicle.trip.trip_id == trip_id), None)
                
                if vehicle_position:
                    # Get stop information
                    current_stop = None
                    next_stop = None
                    next_stop_time = None
                    
                    if vehicle_position.stop_id:
                        current_stop = vehicle_position.stop_id
                    
                    # Get the next stop from trip_update
                    stop_times = entity.trip_update.stop_time_update
                    if stop_times:
                        for stop_time in stop_times:
                            if stop_time.HasField('arrival') and stop_time.arrival.time > current_time:
                                next_stop = stop_time.stop_id
                                next_stop_time = stop_time.arrival.time
                                break
                    
                    trains.append({
                        "train_id": train_id,
                        "route_id": "New Haven" if route_id == "1" else "New Haven Express",
                        "direction": "Outbound" if trip.direction_id == 1 else "Inbound",
                        "current_stop": current_stop,
                        "next_stop": next_stop,
                        "next_stop_time": next_stop_time,
                        "latitude": vehicle_position.position.latitude,
                        "longitude": vehicle_position.position.longitude,
                        "status": vehicle_position.current_status
                    })
    
    return trains

def display_trains(trains):
    """Display trains in a readable table format."""
    console = Console()
    
    if not trains:
        console.print("\n[bold red]No New Haven line trains currently active.[/bold red]")
        return
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Train ID")
    table.add_column("Line")
    table.add_column("Direction")
    table.add_column("Current Location")
    table.add_column("Next Stop")
    table.add_column("Arrival Time")
    table.add_column("Status")
    
    for train in trains:
        status_map = {0: "Incoming", 1: "Stopped", 2: "In Transit"}
        status = status_map.get(train["status"], "Unknown")
        
        next_stop_time = format_timestamp(train["next_stop_time"]) if train["next_stop_time"] else "N/A"
        
        table.add_row(
            train["train_id"],
            train["route_id"],
            train["direction"],
            f"{train['current_stop'] or 'Between stations'}\n({train['latitude']:.4f}, {train['longitude']:.4f})",
            train["next_stop"] or "Unknown",
            next_stop_time,
            status
        )
    
    console.print("\n[bold green]Metro North New Haven Line Trains - Current Locations[/bold green]")
    console.print(table)
    console.print(f"\n[italic]Data updated at: {datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}[/italic]")

def main():
    """Main function to run the application."""
    try:
        console = Console()
        with console.status("[bold green]Fetching Metro North train data..."):
            trains = get_new_haven_trains()
        display_trains(trains)
    except Exception as e:
        console = Console()
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        console.print("\n[yellow]Hint: Make sure you have set the MTA_API_KEY environment variable.[/yellow]")
        console.print("You can get an API key from: https://api.mta.info/")

if __name__ == "__main__":
    main()
