import time
import webbrowser
from datetime import datetime
from gtfs_fetcher import GTFSFetcher
from data_processor import DataProcessor
from visualizer import TrainVisualizer

class RealtimeMonitor:
    def __init__(self, api_url, update_interval=30):
        self.fetcher = GTFSFetcher(api_url)
        self.processor = DataProcessor()
        self.visualizer = TrainVisualizer()
        self.update_interval = update_interval
        
    def run_continuous_monitoring(self, duration_minutes=60):
        """Run continuous monitoring for specified duration"""
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        print(f"Starting Metro North real-time monitoring...")
        print(f"Will run for {duration_minutes} minutes")
        print(f"Updates every {self.update_interval} seconds")
        
        first_run = True
        
        while time.time() < end_time:
            try:
                # Fetch latest data
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Fetching latest train data...")
                feed = self.fetcher.fetch_feed()
                
                if feed:
                    # Process vehicle positions
                    vehicles = self.processor.extract_vehicle_positions(feed)
                    print(f"Found {len(vehicles)} active trains on New Haven line")
                    
                    if vehicles:
                        # Create updated map
                        train_map = self.visualizer.create_map(vehicles)
                        map_file = self.visualizer.save_map(train_map)
                        
                        # Open in browser on first run
                        if first_run:
                            webbrowser.open(f'file://{map_file}')
                            first_run = False
                            
                        print(f"Map updated: {map_file}")
                        
                        # Print train summary
                        for vehicle in vehicles:
                            print(f"  Train {vehicle['vehicle_id']}: "
                                f"Lat {vehicle['latitude']:.4f}, "
                                f"Lon {vehicle['longitude']:.4f}")
                    else:
                        print("No trains currently active on New Haven line")
                else:
                    print("Failed to fetch feed data")
                    
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
            
            # Wait before next update
            print(f"Waiting {self.update_interval} seconds until next update...")
            time.sleep(self.update_interval)
        
        print("Monitoring session completed!")
    
    def run_single_update(self):
        """Run a single update and create map"""
        feed = self.fetcher.fetch_feed()
        if feed:
            vehicles = self.processor.extract_vehicle_positions(feed)
            if vehicles:
                train_map = self.visualizer.create_map(vehicles)
                map_file = self.visualizer.save_map(train_map)
                webbrowser.open(f'file://{map_file}')
                return len(vehicles)
        return 0

# Main execution
if __name__ == "__main__":
    API_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/mnr%2Fgtfs-mnr"
    
    monitor = RealtimeMonitor(API_URL, update_interval=30)
    
    # Run single update first to test
    print("Running single update test...")
    train_count = monitor.run_single_update()
    print(f"Test completed - found {train_count} trains")
    
    # Ask user if they want continuous monitoring
    choice = input("\nStart continuous monitoring? (y/n): ")
    if choice.lower() == 'y':
        duration = int(input("How many minutes to monitor? (default 60): ") or 60)
        monitor.run_continuous_monitoring(duration)