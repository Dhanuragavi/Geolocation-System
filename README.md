# 🗺️Geolocation system to find Nearest Neighbour

## 🎯 Objective

The aim of this project is to build a geolocation-based system capable of identifying the nearest neighbors such as vehicles, hospitals, hotels, or any points of interest in real time.
By combining efficient spatial data structures with intuitive user interfaces and map rendering, the system allows users to find the closest options based on location input, supporting applications in ride-hailing, navigation, emergency services, and urban planning.

## 🧰 Tools Used

* Python: Core programming language.
* PyQt5: For building the desktop GUI interface.
* Folium: For map visualization using Leaflet.js.
* Geopy & Nominatim API: To convert city names into geographic coordinates.
* QuadTree: For efficient spatial indexing and nearest-neighbor searching.
* QTimer: To simulate real-time environment with periodic point updates.
* Stack-based reward system: To track and encourage user interactions.



## ⚙️ How It Works

1. **City Input via GUI**:
   The user selects a city from a dropdown in the PyQt5-based interface.

2. **Location Geocoding**:
   Using Nominatim, the selected city name is converted to its geographical coordinates.

3. **Random Point Generation**:
   A set of random points is generated near the city to simulate nearby entities (e.g., vehicles).

4. **QuadTree Spatial Indexing**:
   The generated points are indexed in a QuadTree structure to allow fast proximity-based queries.

5. **K-Nearest Neighbour Search**:
   The system computes and highlights the nearest `k` points to the selected city.

6. **Map Rendering**:
   A Folium map is embedded into the GUI using WebEngineView, showing:

   * Red marker: selected city
   * Blue markers: all generated points
   * Green markers: nearest neighbors

7. **Dynamic Update with Timer**:
   The map and data refresh at intervals, simulating real-time tracking.

8. **Reward System**:
   A simple stack-based reward mechanism tracks selected cities and applies point-based discounts (ideal for gamification in real apps).



## ✅ Results

The system efficiently detects and displays the **nearest neighbors** for any selected city. It accurately:

* Converts city names to coordinates
* Simulates surrounding points
* Retrieves the closest locations using QuadTree
* Renders results on an interactive map
* Supports periodic data refresh
* reward logic for user engagement

## 🚀 Future Work

To enhance real-world applicability, the system can be improved by:

* **Real-Time GPS Integration:** Use of APIs like Google Maps or OpenStreetMap for live tracking of vehicles and services.
* **Cross-Platform Support:** This can be Extended to web/mobile applications via Flutter, React, or Electron for broader accessibility.
* **Backend Integration:** Databases like  PostgreSQL, firebase can be created to store user data, history, and map interactions.
* **Improved Scalability:** Optimized algorithms can be used with QuadTree for large datasets.
* **Smart Filtering & Rewards:** Category-based search(hospitals,hotels), user login, and real-time reward tracking can be Enabled.
* **UI/UX Enhancements:** Animated routes, clustering, and heatmaps can be included for richer map interaction.




## 🧠 Conclusion

This project provides a scalable concept for finding nearest neighbors using geolocation applicable to services like Uber, nearby hospitals or hotels, or any smart city solution requiring real-time proximity detection. By integrating spatial indexing, map visualization, and GUI interaction, it demonstrates the core logic behind location-aware applications.

 *Note: This is a conceptual prototype using simulated data and a desktop interface, intended to showcase the foundational design. It can be extended with live GPS, mobile support, and backend integration for real-world deployment.*




