from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, Qt
from city_action_page import CityActionPage
from PyQt5.QtGui import QIcon, QFont, QCursor
from PyQt5.QtCore import QSize, Qt

from simcity.bot.cities import get_cities


class SimcityBotLandingPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        # Layout for the main landing page
        layout = QVBoxLayout()

        # Header
        header = QLabel("Simcity Buildit Bot - Choose a City", self)
        header.setFont(QFont('Arial', 24))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        cities = get_cities()

        # Grid Layout for city buttons
        grid_layout = QGridLayout()

        for i, city in enumerate(cities):
            city_button = QPushButton(city["name"])
            # city_button.setIcon(QIcon("..\\..\\..\\resources\\SimCity_BuildIt_icon.png"))  # Replace with actual icon path
            # city_button.setIconSize(QSize(100, 100))
            city_button.setFont(QFont('Arial', 15))
            city_button.setStyleSheet('padding: 10px;')
            city_button.setCursor(Qt.PointingHandCursor)
            # Use lambda with default argument city=city to avoid reference issues
            city_button.clicked.connect(lambda checked, city=city: self.open_city_actions(city))

            grid_layout.addWidget(city_button, i // 4, i % 4)  # Positioning buttons in a grid

        layout.addLayout(grid_layout)
        self.setLayout(layout)

    def open_city_actions(self, city):
        print(f"Opening actions for {city['name']}")
        for index in range(self.parent.count()):
            widget = self.parent.widget(index)
            if isinstance(widget, CityActionPage) and widget.city_name == city["name"]:
                self.parent.setCurrentIndex(index)
                return

        city_action_page = CityActionPage(city_name=city["name"], city=city, parent=self.parent)
        self.parent.addWidget(city_action_page)
        self.parent.setCurrentIndex(self.parent.count() - 1)

