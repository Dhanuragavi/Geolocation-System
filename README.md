# 🗺️Geolocation system to find Nearest Neighbour

## 🎯 Objective

The aim of this project is to build a geolocation-based system capable of identifying the nearest neighbors such as vehicles🚘, hospitals🏥, hotels🏨, or any points of interest in real time.
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



## ✅ Result

The system efficiently detects and displays the **nearest neighbors** for any selected city. It accurately:

* Converts city names to coordinates
* Simulates surrounding points
* Retrieves the closest locations using QuadTree
* Renders results on an interactive map
* Supports periodic data refresh and a reward logic for user engagement



## 🧠 Conclusion

This project provides a **scalable concept** for finding **nearest neighbors** based on geolocation—applicable to **car services like Uber**, **finding nearby hospitals or hotels**, or **any smart city service** that requires real-time proximity detection.
By combining **spatial algorithms** with **map visualization** and **GUI interaction**, this system showcases how geolocation-aware applications can be built for a wide range of real-world use cases.



