from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtWidgets import QFrame, QCheckBox, QLabel, QHBoxLayout

class CustomListWidgetItem(QFrame):
    # Define a signal that emits when the checkbox is toggled
    checked_changed = pyqtSignal(str, bool)

    def __init__(self, text):
        super().__init__()

        # Set frame style for the QFrame
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

        self.layout = QHBoxLayout()
        self.checkbox = QCheckBox()
        self.checkbox.setCursor(QCursor(Qt.PointingHandCursor))
        self.checkbox.setText(text)

        # Add widgets to the layout
        self.layout.addWidget(self.checkbox)
        self.setLayout(self.layout)

        # Connect the checkbox state change to emit the signal
        self.checkbox.stateChanged.connect(self.emit_signal)

        # Make the entire widget clickable
        self.mousePressEvent = self.handle_row_click

    def emit_signal(self):
        """Emit the signal with the material name and whether it's checked."""
        is_checked = self.checkbox.isChecked()
        self.checked_changed.emit(self.get_material_name(), is_checked)

    def handle_row_click(self, event):
        """Handle clicks on the row and toggle the checkbox."""
        self.toggle_checked()

    def is_checked(self):
        """Return the checkbox checked state."""
        return self.checkbox.isChecked()

    def get_material_name(self):
        """Return the text of the label (the material name)."""
        return self.checkbox.text()

    def toggle_checked(self):
        """Toggle the state of the checkbox."""
        self.checkbox.toggle()

    def set_check_false(self):
        """Set the checkbox to False if it's checked."""
        if self.checkbox.isChecked():
            self.checkbox.setChecked(False)
