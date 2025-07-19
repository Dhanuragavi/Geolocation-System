# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 02:35:56 2023

@author: arpud
"""

import folium
from geopy.geocoders import Nominatim
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QCheckBox, QPushButton, QCompleter, QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt, QUrl, QTimer, pyqtSlot
from PyQt5.QtWidgets import QTextBrowser
from random import uniform
from geopy.distance import geodesic


class QuadTree:
    def __init__(self, bounds):
        self.bounds = bounds
        self.points = []


    def generate_quadtree_points(self, num_points, depth=3):
        if depth == 0 or num_points == 0:
            return []

        min_x, min_y, max_x, max_y = self.bounds

        mid_x = (min_x + max_x) / 2
        mid_y = (min_y + max_y) / 2

        quad_points = []

        # Recursive call for each quadrant
        quad_points.extend(QuadTree([min_x, min_y, mid_x, mid_y]).generate_quadtree_points(num_points // 4, depth - 1))
        quad_points.extend(QuadTree([mid_x, min_y, max_x, mid_y]).generate_quadtree_points(num_points // 4, depth - 1))
        quad_points.extend(QuadTree([min_x, mid_y, mid_x, max_y]).generate_quadtree_points(num_points // 4, depth - 1))
        quad_points.extend(QuadTree([mid_x, mid_y, max_x, max_y]).generate_quadtree_points(num_points // 4, depth - 1))

        # Add random points within the current quadrant
        quad_points.extend(generate_quadtree_points([min_x, min_y, max_x, max_y], num_points // 2))

        return quad_points


    def find_nearest_points(self, target_point, num_points=5):
        distances = [(point, geodesic(target_point, point).km) for point in self.points]
        distances.sort(key=lambda x: x[1])
        return distances[:num_points]


def generate_quadtree_points(bounds, num_points):
    points = []
    for _ in range(num_points):
        point = [
            uniform(bounds[0], bounds[2]),
            uniform(bounds[1], bounds[3])
        ]
        points.append(point)
    return points


class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.district_input = QComboBox()
        self.city_input = QComboBox()
        self.point_button_group = QButtonGroup()
        self.nearest_points = []
        self.webview = QWebEngineView()
        self.text_browser = QTextBrowser()

        # QTimer for refreshing random points every 30 seconds
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_random_points)

        # QTimer for refreshing random points every 15 seconds after point selection
        self.refresh_after_selection_timer = QTimer(self)
        self.refresh_after_selection_timer.timeout.connect(self.refresh_random_points_after_selection)

        # Stack to store selected points
        self.point_selection_stack = []

        # Counter for discounts
        self.discount_counter = 0

        self.initUI()


    def initUI(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.districts = {
            "Chennai": ["Chennai"],
            "Coimbatore": ["Coimbatore"],
            "Ariyalur":["Ariyalur"],
            "Madurai": ["Madurai"],
            "Cuddalore":["Cuddalore"],
            "Dharmapur":["Dharmapuri"],
            "Dindigul":["Dindigul"],
            "Erode":["Erode"],
            "Kanchipuram":["Kachipuram"],
            "Kanyakumari":["Kanyakumari"],
            "Karur":["Karur"],
            "Krishnagiri":["Krishnagiri"],
            "Nagapattinam":["Nagapattinam"],
            "Namakkal":["Namakkal"],
            "Nilgiris":["Nilgiris"],
            "Perambalur":["Perambalur"],
            "Pudukkotai":["Pudukkotai"],
            "Ramanathapuram":["Ramanathapuram"],
            "Selam":["Selam"],
            "Sivaganga":["Sivaganga"],
            "Thanjavur":["Thanjavur"],
            "Theni":["Theni"],
            "Thoothukudi":["Thoothukudi","Tuticorin"],
            "Tiruchirappalli":["Tiruchirappalli"],
            "Tirunalveli":["Tirunalveli"],
            "Tiruppur":["Tiruppur"],
            "Tiruvallur":["Tiruvallur"],
            "Tiruvannamalai":["Tiruvannamalai"],
            "Tiruvarur":["Tiruvarur"],
            "Vellore":["Vellore"],
            "Viluppuram":["Viluppuram"],
            "Virudhunagar":["Virudhunagar"]
        }

        self.district_input.setEditable(True)
        self.district_input.setPlaceholderText("Select a district")
        self.district_input.currentTextChanged.connect(self.update_districts)

        self.city_input.setEditable(True)
        self.city_input.setPlaceholderText("Select or Enter a city name")

        use_combobox = QCheckBox("Use ComboBox")
        use_combobox.setChecked(False)

        show_map_button = QPushButton("Show on Map")
        show_map_button.clicked.connect(self.show_map)

        completer = QCompleter(self.districts.keys())
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.district_input.setCompleter(completer)

        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)

        layout.addWidget(use_combobox)
        layout.addWidget(self.district_input)
        layout.addWidget(self.city_input)
        layout.addWidget(show_map_button)
        layout.addWidget(self.webview)

        for idx in range(5):
            radio_button = QRadioButton(f"Point {idx + 1}")
            self.point_button_group.addButton(radio_button, idx)
            layout.addWidget(radio_button)

        select_point_button = QPushButton("Select Point")
        select_point_button.clicked.connect(self.select_point)
        layout.addWidget(select_point_button)

        # Start the timer to refresh random points every 30 seconds
        self.refresh_timer.start(30000)  # 30,000 milliseconds = 30 seconds

        self.setCentralWidget(widget)
        self.resize(800, 600)
        self.show()


    @pyqtSlot(str)
    def update_districts(self, text):
        # Update the districts based on the entered text
        filtered_districts = [district for district in self.districts.keys() if district.lower().startswith(text.lower())]
        self.district_input.clear()
        self.district_input.addItems(filtered_districts)


    def show_map(self):
        selected_district = self.district_input.currentText()
        selected_city = self.city_input.currentText()

        if not selected_district or not selected_city:
            print("Please select a district and city from the ComboBox.")
            return

        geolocator = Nominatim(user_agent="geo_locator")
        city_location = geolocator.geocode(selected_city)

        if city_location:
            m = folium.Map(location=[city_location.latitude, city_location.longitude], zoom_start=12)

            popup_html_city = f'<h3>City: {selected_city}</h3>'
            folium.Marker([city_location.latitude, city_location.longitude],
                          popup=folium.Popup(popup_html_city, parse_html=True), icon=folium.Icon(color='red')).add_to(m)

            bounds = [city_location.latitude - 0.02, city_location.longitude - 0.02,
                      city_location.latitude + 0.02, city_location.longitude + 0.02]
            quad_tree = QuadTree(bounds)

            random_points = generate_quadtree_points(bounds, num_points=20)

            for point in random_points:
                quad_tree.points.append(point)
                folium.Marker(point, icon=folium.Icon(color='blue')).add_to(m)

            self.nearest_points = quad_tree.find_nearest_points((city_location.latitude, city_location.longitude), num_points=5)

            nearest_points_html = '<h3>5 Nearest Points:</h3><ul>'
            for point, distance in self.nearest_points:
                folium.Marker(point, icon=folium.Icon(color='green'),
                              popup=f'<h3>Distance to {selected_city}: {distance:.2f} km</h3>').add_to(m)
                nearest_points_html += f'<li><input type="radio" name="point" value="{point}"> Point {point} - Distance: {distance:.2f} km</li>'
                self.point_button_group.button(self.nearest_points.index((point, distance))).setText(f"Point {point} - Distance: {distance:.2f} km")

            nearest_points_html += '</ul>'

            map_html_path = r'D:\SEM 3\data structures\PROJECT\final\my_map.html'
            m.save(map_html_path)

            self.webview.setUrl(QUrl.fromLocalFile(map_html_path))

            self.text_browser.setHtml(nearest_points_html)
            print(nearest_points_html)
        else:
            print(f"Error: Could not find coordinates for {selected_city}")


    def select_point(self):
        selected_button = self.point_button_group.checkedButton()
        if selected_button:
            selected_index = self.point_button_group.id(selected_button)
            selected_point, distance = self.nearest_points[selected_index]
            print(f"Selected Point: {selected_point} - Distance: {distance:.2f} km")

            # Stop the timer for refreshing random points every 30 seconds
            self.refresh_timer.stop()

            # Start the timer for refreshing random points every 15 seconds after point selection
            self.refresh_after_selection_timer.start(15000)  # 15,000 milliseconds = 15 seconds

            # Store selected points in the stack
            self.point_selection_stack.append(selected_point)

            if len(self.point_selection_stack) % 5 == 0:
                self.discount_counter += 1
                print(f"Discount {self.discount_counter}: You have selected points {len(self.point_selection_stack)} times.")

                if self.discount_counter == 2:  # Reset the discount counter after 2 discounts
                    self.discount_counter = 0

                # Implement your discount logic here


    def refresh_random_points(self):
      if not self.nearest_points:
        print("No nearest points available.")
        return

    # Refresh random points and update the map
      bounds = [self.nearest_points[0][0][0] - 0.02, self.nearest_points[0][0][1] - 0.02,
              self.nearest_points[0][0][0] + 0.02, self.nearest_points[0][0][1] + 0.02]
      quad_tree = QuadTree(bounds)

      random_points = generate_quadtree_points(bounds, num_points=20)

      for point in random_points:
        quad_tree.points.append(point)

      self.nearest_points = quad_tree.find_nearest_points(self.nearest_points[0][0], num_points=5)

    # Update the map with the new random points
      self.show_map()



    def refresh_random_points_after_selection(self):
        # Refresh random points after point selection and update the map
        bounds = [self.nearest_points[0][0][0] - 0.02, self.nearest_points[0][0][1] - 0.02,
                  self.nearest_points[0][0][0] + 0.02, self.nearest_points[0][0][1] + 0.02]
        quad_tree = QuadTree(bounds)

        random_points = generate_quadtree_points(bounds, num_points=20)

        for point in random_points:
            quad_tree.points.append(point)

        self.nearest_points = quad_tree.find_nearest_points(self.nearest_points[0][0], num_points=5)

        # Update the map with the new random points
        self.show_map()

        # Stop the timer for refreshing random points every 15 seconds after point selection
        self.refresh_after_selection_timer.stop()

        # Start the timer for refreshing random points every 30 seconds
        self.refresh_timer.start(30000)  # 30,000 milliseconds = 30 seconds


if __name__ == '__main__':
    app = QApplication([])
    window = MapApp()
    app.exec_()
