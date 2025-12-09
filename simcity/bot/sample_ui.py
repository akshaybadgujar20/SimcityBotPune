import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon, QFont, QCursor
from PyQt5.QtCore import QSize, Qt


class SimcityBotLandingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle("Simcity Buildit Bot")
        self.setGeometry(100, 100, 1300, 600)  # Window size to fit grid layout
        self.setWindowIcon(QIcon('path_to_main_icon.png'))  # Set your main window icon here

        # Create main layout (vertical to hold title and grid)
        main_layout = QVBoxLayout()

        # Header (Title)
        header = QLabel("Simcity Buildit Bot", self)
        header.setFont(QFont('Arial', 32))
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # Grid Layout for 2 rows and 6 columns of buttons
        grid_layout = QGridLayout()

        # Example icon names and labels (replace with your own)
        icons = [
            {"icon": "path_to_icon1.png", "label": "Base City"},
            {"icon": "path_to_icon2.png", "label": "Barleycorn Point"},
            {"icon": "path_to_icon3.png", "label": "Sunshine Valley"},
            {"icon": "path_to_icon4.png", "label": "Traders Ridge"},
            {"icon": "path_to_icon5.png", "label": "Magnolia Wetlands"},
            {"icon": "path_to_icon6.png", "label": "Hokusai Cliffs"},
            {"icon": "path_to_icon7.png", "label": "Nautilus Plateau"},
            {"icon": "path_to_icon8.png", "label": "Petrol Bay"},
            {"icon": "path_to_icon9.png", "label": "Grand Haven"},
            {"icon": "path_to_icon10.png", "label": "Jugband Hills"},
            {"icon": "path_to_icon11.png", "label": "Cottonwood Forest"}
        ]

        # Create 12 buttons (2 rows, 6 columns)
        for i, item in enumerate(icons):
            # Create the button
            button = QPushButton()
            button.setIcon(QIcon(item["icon"]))  # Set icon for the button
            button.setIconSize(QSize(200, 200))  # Set the size of the icon
            button.setText(item["label"])
            button.setFont(QFont('Arial', 18))
            button.setStyleSheet("text-align: bottom;")  # Text label at the bottom
            button.setFixedSize(220, 220)  # Button size slightly bigger than icon size
            button.clicked.connect(lambda ch, label=item["label"]: self.open_page(label))  # Connect to action
            # Set hand cursor for button
            button.setCursor(QCursor(Qt.PointingHandCursor))  # Hand cursor

            # Add button to grid layout
            grid_layout.addWidget(button, i // 6, i % 6)  # Positioning in 2x6 grid

        # Add the grid layout to the main layout
        main_layout.addLayout(grid_layout)

        # Set the main layout to the window
        self.setLayout(main_layout)

    def open_page(self, label):
        # Action when a button is clicked
        QMessageBox.information(self, "Navigation", f"Opening {label} page...")


# Main function to run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimcityBotLandingPage()
    window.show()
    sys.exit(app.exec_())
