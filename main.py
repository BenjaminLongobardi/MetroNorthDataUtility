from realtime_monitor import RealtimeMonitor

# Quick start script
if __name__ == "__main__":
    API_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/mnr%2Fgtfs-mnr"
    
    # Create monitor
    monitor = RealtimeMonitor(API_URL, update_interval=60)  # Update every minute
    
    # Run single update to test
    monitor.run_single_update()
    
    #print("Single update completed. Starting continuous monitoring...")
    #monitor.run_continuous_monitoring()

    # run the run_continuous_monitoring
    #monitor.run_continuous_monitoring()
