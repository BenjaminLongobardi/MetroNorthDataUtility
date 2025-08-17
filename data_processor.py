class DataProcessor:
    def __init__(self):
        self.new_haven_routes = ['5', '6']  # Metro North New Haven line route IDs
        
    def extract_vehicle_positions(self, feed):
        """Extract vehicle positions for New Haven line"""
        vehicles = []
        
        if not feed:
            return vehicles
            
        for entity in feed.entity:
            if entity.HasField('vehicle'):
                vehicle = entity.vehicle
                tripUpdate = entity.trip_update
                trip = tripUpdate.trip if tripUpdate else None
                route_id = trip.route_id if trip else None
                trip_id = trip.trip_id if trip else None

                # Filter for New Haven line trains
                #if (route_id in self.new_haven_routes):
                if (True):
                    
                    vehicle_data = {
                        'vehicle_id': vehicle.vehicle.id if vehicle.HasField('vehicle') else 'Unknown',
                        'trip_id': trip_id if trip.HasField('trip_id') else None,
                        'route_id': route_id if trip.HasField('route_id') else None,
                        'latitude': vehicle.position.latitude if vehicle.HasField('position') else None,
                        'longitude': vehicle.position.longitude if vehicle.HasField('position') else None,
                        'timestamp': vehicle.timestamp if vehicle.HasField('timestamp') else None,
                    }
                    
                    # Only add if we have valid coordinates
                    if vehicle_data['latitude'] and vehicle_data['longitude']:
                        vehicles.append(vehicle_data)
        
        return vehicles