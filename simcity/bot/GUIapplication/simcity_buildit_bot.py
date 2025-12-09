import sys

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QStackedWidget, QWidget
from landing_page import SimcityBotLandingPage

class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simcity Buildit Bot")
        # self.setGeometry(100, 100, 1000, 600)

        # QStackedWidget to handle multiple pages (Landing Page + City Action Pages)
        self.stacked_widget = QStackedWidget()

        # Add landing page
        landing_page = SimcityBotLandingPage(parent=self.stacked_widget)
        self.stacked_widget.addWidget(landing_page)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)


# Main function to run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
