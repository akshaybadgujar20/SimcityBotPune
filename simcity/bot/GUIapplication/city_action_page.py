import logging
from logging import fatal

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QLineEdit, QMessageBox, QScrollArea, QApplication,QCheckBox
)
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt, QTimer
from concurrent.futures import ThreadPoolExecutor

from simcity.bot.enums.city_actions import CityAction
from simcity.bot.enums.material import Material
from simcity.bot.main import material_dict
from simcity.bot.material_data_loader import load_material_info_data


class CityActionPage(QWidget):
    def __init__(self, city_name, city, parent):
        super().__init__()
        self.city_name = city_name
        self.city = city
        self.parent = parent
        self.initUI()
        self.chip_widgets = {}
        self.search_timer = QTimer(self)
        self.search_timer.setInterval(300)  # Set the delay (300 ms, adjust as needed)
        self.search_timer.timeout.connect(self.filter_materials)

    def initUI(self):
        try:
            self.setWindowTitle(f"Actions for {self.city_name}")
            main_layout = QVBoxLayout()
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.setSpacing(5)

            self.add_page_header(main_layout)
            self.add_top_layout(main_layout)

            vbox_layout = QVBoxLayout()
            self.add_actions_in_left_side_panel(vbox_layout)

            grid_container_layout = QHBoxLayout()
            grid_container_layout.addLayout(vbox_layout)
            grid_container_layout.setAlignment(Qt.AlignLeft)

            self.listWidget = QListWidget()
            self.add_list_widget_items()

            search_layout = QHBoxLayout()
            self.add_search_section()

            clear_button = self.add_clear_button()
            search_layout.addWidget(self.material_search)
            search_layout.addWidget(clear_button)

            confirm_button = self.add_confirm_action_button()
            materials_label = self.create_search_label()

            chip_scroll_area = QScrollArea()
            chip_scroll_area.setWidgetResizable(True)
            chip_widget = QWidget()
            self.chip_layout = QHBoxLayout()
            self.chip_layout.setAlignment(Qt.AlignLeft)

            right_layout = QVBoxLayout()
            right_layout.addWidget(materials_label)
            right_layout.addLayout(search_layout)
            right_layout.addLayout(self.chip_layout)
            right_layout.addWidget(self.listWidget)
            right_layout.addWidget(confirm_button)

            grid_container_layout.addLayout(right_layout)
            grid_container_layout.setAlignment(Qt.AlignRight)

            main_layout.addLayout(grid_container_layout)
            self.setLayout(main_layout)
            self.executor = ThreadPoolExecutor(max_workers=1)
        except Exception as e:
            print(f"Error during UI initialization: {e}")

    def create_search_label(self):
        materials_label = QLabel("Materials:")
        font = QFont()
        font.setPointSize(12)
        materials_label.setFont(font)
        return materials_label

    def add_top_layout(self, main_layout):
        top_button_layout = QHBoxLayout()
        top_button_layout.setContentsMargins(0, 0, 0, 0)
        back_button = self.create_go_back_button()
        top_button_layout.addWidget(back_button)
        top_button_layout.addStretch(1)
        exit_button = self.create_exit_button()
        top_button_layout.addWidget(exit_button)
        main_layout.addLayout(top_button_layout)

    def add_list_widget_items(self):
        sorted_materials = sorted(self.city['materials'])
        for material in sorted_materials:
            checkbox = QCheckBox(material)
            checkbox.setFont(QFont('Arial', 12))
            list_item = QListWidgetItem()
            list_item.setSizeHint(checkbox.sizeHint())
            self.listWidget.addItem(list_item)
            self.listWidget.setItemWidget(list_item, checkbox)
            checkbox.stateChanged.connect(lambda state, material=material: self.handle_item_toggled(material, state == Qt.Checked))

    def add_clear_button(self):
        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet('padding: 10px;')
        clear_button.setFont(QFont('Arial', 12))
        clear_button.setCursor(QCursor(Qt.PointingHandCursor))
        clear_button.clicked.connect(self.clear_search)
        return clear_button

    def add_search_section(self):
        self.material_search = QLineEdit()
        self.material_search.setPlaceholderText("Search materials...")
        self.material_search.setFont(QFont('Arial', 12))
        self.material_search.textChanged.connect(self.on_text_changed)

    def add_confirm_action_button(self):
        confirm_button = QPushButton("Confirm Selection")
        confirm_button.setStyleSheet('padding: 10px;')
        confirm_button.setFont(QFont('Arial', 12))
        confirm_button.setCursor(QCursor(Qt.PointingHandCursor))
        confirm_button.clicked.connect(self.confirm_selection)
        return confirm_button

    def add_actions_in_left_side_panel(self, vbox_layout):
        for i, action in enumerate(self.city['actions']):
            action_button = QPushButton(action['name'].value)
            action_button.setFont(QFont('Arial', 12))
            action_button.setStyleSheet('padding: 10px;')
            action_button.setCursor(QCursor(Qt.PointingHandCursor))
            action_button.clicked.connect(lambda checked, action=action: self.perform_action(action))
            vbox_layout.addWidget(action_button)

    def create_exit_button(self):
        exit_button = QPushButton("Exit")
        exit_button.setFont(QFont('Arial', 12))
        exit_button.setStyleSheet('padding: 10px;')
        exit_button.clicked.connect(self.close_application)
        exit_button.setCursor(QCursor(Qt.PointingHandCursor))
        return exit_button

    def create_go_back_button(self):
        back_button = QPushButton("Go Back")
        back_button.setFont(QFont('Arial', 12))
        back_button.setStyleSheet('padding: 10px;')
        back_button.clicked.connect(self.go_back)
        back_button.setCursor(QCursor(Qt.PointingHandCursor))
        return back_button

    def perform_action(self, action):
        selected_materials = self.get_selected_material_from_list()
        select_material_list = []
        material_dict = load_material_info_data()
        for material in selected_materials:
            select_material_list.append(material_dict[material])
        logging.info(f'Action", f"You selected: {action['name'].value}')
        # Add actual function call with parameters
        from simcity.bot.main import set_up
        city_port = self.city['port']
        set_up(city_port)
        if action['name'] == CityAction.CONTINUOUS_BUY:
            material_priorities = {}
            for material, index in select_material_list:
                Material[material]: index + 1
            self.executor.submit(action['function_call'], selected_materials, city_port)
        elif action['name'] == CityAction.SELL_WITH_FULL_VALUE:
            materials = select_material_list
            self.executor.submit(action['function_call'], materials, city_port, False, True)
        elif action['name'] == CityAction.SELL_WITH_ZERO_VALUE:
            materials = select_material_list
            self.executor.submit(action['function_call'], materials, city_port, False, False)
        elif action['name'] == CityAction.COLLECT_FROM_FACTORY:
            self.executor.submit(action['function_call'], self.city['no_of_factories'], city_port)
        elif action['name'] == CityAction.COLLECT_FROM_COMMERCIAL:
            self.executor.submit(action['function_call'], self.city['no_of_commercial_buildings'], city_port)
        elif action['name'] == CityAction.COLLECT_SOLD_ITEM_MONEY:
            self.executor.submit(action['function_call'], 1, city_port)
        elif action['name'] == CityAction.ADVERTISE_ITEM_ON_TRADE_DEPOT:
            self.executor.submit(action['function_call'], action.get('param', None))
        elif action['name'] == CityAction.ADD_COMMERCIAL_MATERIAL_TO_PRODUCTION:
            material = select_material_list[0]
            self.executor.submit(action['function_call'], material, city_port)
        elif action['name'] == CityAction.ADD_RAW_MATERIAL_TO_PRODUCTION:
            material = select_material_list[0]
            self.executor.submit(action['function_call'], material, self.city['no_of_factories'], city_port)
        else:
            raise ValueError(f"Unknown action: {action}")

    def go_back(self):
        self.parent.setCurrentIndex(self.parent.count() - 2)

    def close_application(self):
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()

    def filter_materials(self):
        try:
            search_text = self.material_search.text().lower()
            self.listWidget.clear()
            filtered_materials = [m for m in self.city['materials'] if search_text in m.lower()]
            for material in filtered_materials:
                checkbox = QCheckBox(material)
                checkbox.setFont(QFont('Arial', 12))
                list_item = QListWidgetItem()
                list_item.setSizeHint(checkbox.sizeHint())
                self.listWidget.addItem(list_item)
                self.listWidget.setItemWidget(list_item, checkbox)
                checkbox.stateChanged.connect(lambda state, material=material: self.handle_item_toggled(material, state == Qt.Checked))
        except Exception as e:
            print(f"filter_materials: {e}")

    def confirm_selection(self):
        selected_materials = self.get_selected_material_from_list()
        if selected_materials:
            QMessageBox.information(self, "Selected Materials", f"You selected: {', '.join(selected_materials)}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select at least one material.")

    def get_selected_material_from_list(self):
        selected_materials = []
        for index in range(self.listWidget.count()):
            list_item = self.listWidget.item(index)  # Get the QListWidgetItem
            item_widget = self.listWidget.itemWidget(list_item)  # Get the associated widget (checkbox)

            if isinstance(item_widget, QCheckBox) and item_widget.isChecked():
                selected_materials.append(item_widget.text())  # Get the material name from the checkbox text

        return selected_materials

    def clear_search(self):
        self.material_search.clear()
        self.clear_chips()

        # Reset checkboxes without disconnecting/reconnecting signals multiple times
        for index in range(self.listWidget.count()):
            list_item = self.listWidget.item(index)
            checkbox = self.listWidget.itemWidget(list_item)

            # Check if the widget is a QCheckBox and uncheck it if it's checked
            if isinstance(checkbox, QCheckBox):
                if checkbox.isChecked():
                    checkbox.setChecked(False)  # Reset the checkbox state

                # Try reconnecting the signal to handle toggles
                try:
                    checkbox.toggled.disconnect(self.handle_item_toggled)
                except TypeError:
                    # Signal was not connected; continue without error
                    pass

                # Ensure signal is connected to handle toggles
                checkbox.toggled.connect(self.handle_item_toggled)

        # Re-filter the materials (optional, for search behavior)
        self.filter_materials()

    def on_text_changed(self):
        self.search_timer.start()

    def create_chip(self, material_name):
        if material_name in self.chip_widgets:
            return

        # Create the chip widget and layout
        chip_widget = QWidget()
        chip_layout = QHBoxLayout()
        chip_layout.setContentsMargins(5, 5, 5, 5)

        # Chip label
        chip_label = QLabel(material_name)
        chip_label.setStyleSheet("border: none;")
        chip_label.setFont(QFont('Arial', 10))

        # Remove button for the chip
        remove_button = QPushButton("✕")
        remove_button.setStyleSheet("border: none;")
        remove_button.setCursor(QCursor(Qt.PointingHandCursor))
        remove_button.clicked.connect(lambda: self.remove_chip(material_name))

        # Add the label and button to the chip layout
        chip_layout.addWidget(chip_label)
        chip_layout.addWidget(remove_button)

        # Set the layout for the chip widget
        chip_widget.setLayout(chip_layout)
        chip_widget.setStyleSheet("border-radius: 10px;border: 1px solid black;")
        # Store the chip widget and add it to the chip layout
        self.chip_widgets[material_name] = chip_widget
        self.chip_layout.addWidget(chip_widget)
        self.chip_layout.update()

    def remove_chip(self, material_name):
        # Remove the chip from the layout and internal dictionary
        chip_widget = self.chip_widgets.pop(material_name, None)
        if chip_widget:
            chip_widget.setParent(None)

        # Uncheck the corresponding checkbox in the list widget
        for index in range(self.listWidget.count()):
            item_widget = self.listWidget.itemWidget(self.listWidget.item(index))
            if isinstance(item_widget, QCheckBox) and item_widget.text() == material_name:
                item_widget.setChecked(False)  # Uncheck the checkbox
                break  # Stop after finding and unchecking the relevant checkbox

    def clear_chips(self):
        # Loop through the current chip widgets and remove them all
        for material_name in list(self.chip_widgets.keys()):
            self.remove_chip(material_name)

        # Ensure all checkboxes in the list are unchecked
        for index in range(self.listWidget.count()):
            item_widget = self.listWidget.itemWidget(self.listWidget.item(index))
            if isinstance(item_widget, QCheckBox):
                item_widget.setChecked(False)  # Uncheck each checkbox

    def handle_item_toggled(self, material_name, checked):
        if checked:
            self.create_chip(material_name)
        else:
            self.remove_chip(material_name)

    def add_page_header(self, main_layout):
        # Header for the city name
        header = QLabel(f"Actions for {self.city_name}", self)
        header.setFont(QFont('Arial', 24))
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
