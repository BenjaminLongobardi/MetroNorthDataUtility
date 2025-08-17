import folium
from folium import plugins
import webbrowser
import os

class TrainVisualizer:
    def __init__(self):
        # Metro North New Haven line approximate bounds
        self.map_center = [41.3, -73.0]  # Connecticut area
        self.zoom_start = 10
        
    def create_map(self, vehicles):
        """Create an interactive map with train positions"""
        # Create base map
        train_map = folium.Map(
            location=self.map_center,
            zoom_start=self.zoom_start,
            tiles='OpenStreetMap'
        )
        
        # Add train markers
        for vehicle in vehicles:
            lat, lon = vehicle['latitude'], vehicle['longitude']
            
            # Create popup with train info
            popup_text = f"""
            <b>Train ID:</b> {vehicle['vehicle_id']}<br>
            <b>Trip ID:</b> {vehicle['trip_id']}<br>
            <b>Route:</b> {vehicle['route_id']}<br>
            <b>Speed:</b> {vehicle.get('speed', 'Unknown')} mph<br>
            <b>Last Update:</b> {vehicle.get('timestamp', 'Unknown')}
            """
            
            # Add train marker (using train icon)
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=f"Train {vehicle['vehicle_id']}",
                icon=folium.Icon(
                    color='blue',
                    icon='train',
                    prefix='fa'  # FontAwesome icons
                )
            ).add_to(train_map)
            
            # Add bearing indicator if available
            if vehicle.get('bearing'):
                self._add_bearing_arrow(train_map, lat, lon, vehicle['bearing'])
        
        return train_map
    
    def _add_bearing_arrow(self, map_obj, lat, lon, bearing):
        """Add directional arrow showing train bearing"""
        # Simple circle marker with rotation (you can enhance this)
        folium.CircleMarker(
            location=[lat, lon],
            radius=3,
            color='red',
            fillColor='red',
            fillOpacity=0.8
        ).add_to(map_obj)
    
    def save_map(self, train_map, filename='metro_north_live.html'):
        """Save map to HTML file"""
        filepath = os.path.join(os.getcwd(), filename)
        train_map.save(filepath)
        return filepath