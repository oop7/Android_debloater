import sys
import subprocess
import logging
import base64
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox, QLineEdit, QCheckBox
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

# Set up logging to file
logging.basicConfig(filename="adb_log.txt", level=logging.DEBUG, format='%(asctime)s %(message)s')

class AndroidDebloater(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window title and size
        self.setWindowTitle("Android Debloater")
        self.setGeometry(300, 300, 400, 600)

        # Set application icon
        self.setWindowIcon(self.create_icon_from_base64())

        # Create layout
        self.layout = QVBoxLayout()

        # Search bar to filter packages
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search packages...")
        self.search_bar.textChanged.connect(self.filter_packages)

        # Dark mode toggle
        self.dark_mode_checkbox = QCheckBox("Enable Dark Mode", self)
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)

        # Create buttons and package list
        self.list_button = QPushButton("List Installed Packages", self)
        self.list_button.clicked.connect(self.list_packages)

        self.package_list = QListWidget(self)
        self.package_list.setSelectionMode(QListWidget.MultiSelection)

        self.uninstall_button = QPushButton("Uninstall Selected Packages", self)
        self.uninstall_button.clicked.connect(self.uninstall_packages)

        # Add widgets to layout
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.dark_mode_checkbox)  # Add dark mode checkbox
        self.layout.addWidget(self.list_button)
        self.layout.addWidget(self.package_list)
        self.layout.addWidget(self.uninstall_button)

        # Set layout
        self.setLayout(self.layout)

        # Store the complete list of packages for filtering
        self.all_packages = []

    def create_icon_from_base64(self):
        """Create a QIcon from a Base64-encoded image."""
        # Base64-encoded image string (replace this with your own Base64 string)

        # Convert the Base64 string back to binary data
        image_data = base64.b64decode(base64_string)

        # Create a QPixmap from the binary data
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)

        # Return a QIcon created from the QPixmap
        return QIcon(pixmap)

    def toggle_dark_mode(self, state):
        """Toggle dark mode on or off based on the checkbox."""
        if state == Qt.Checked:
            self.setStyleSheet("""
                QWidget {
                    background-color: #2E2E2E;
                    color: #FFFFFF;
                }
                QPushButton {
                    background-color: #4A4A4A;
                    color: #FFFFFF;
                }
                QListWidget {
                    background-color: #3E3E3E;
                    color: #FFFFFF;
                }
                QLineEdit {
                    background-color: #3E3E3E;
                    color: #FFFFFF;
                }
            """)
        else:
            self.setStyleSheet("")

    def list_packages(self):
        """Fetch the list of installed packages from the Android device."""
        self.package_list.clear()
        self.all_packages.clear()
        try:
            # Run the adb command to list packages
            result = subprocess.run(['adb', 'shell', 'pm', 'list', 'packages'], capture_output=True, text=True)
            packages = result.stdout.splitlines()

            if packages:
                for package in packages:
                    # Only process lines that have the correct format
                    if ":" in package:
                        package_name = package.split(":")[1].strip()
                        self.all_packages.append(package_name)
                self.update_package_list()
            else:
                QMessageBox.warning(self, "Error", "No packages found or device not connected.")
                logging.warning("No packages found or device not connected.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            logging.critical(f"Error listing packages: {str(e)}")

    def filter_packages(self):
        """Filter the displayed packages based on the search input."""
        search_text = self.search_bar.text().lower()
        filtered_packages = [pkg for pkg in self.all_packages if search_text in pkg.lower()]
        self.package_list.clear()
        self.package_list.addItems(filtered_packages)

    def update_package_list(self):
        """Update the package list in the GUI."""
        self.package_list.clear()
        self.package_list.addItems(self.all_packages)

    def uninstall_packages(self):
        """Uninstall selected packages from the Android device."""
        selected_items = self.package_list.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "Warning", "No packages selected.")
            return

        for item in selected_items:
            package_name = item.text()
            logging.debug(f"Uninstalling package: {package_name}")
            if not package_name:
                logging.warning("Package name is empty or invalid.")
                continue

            try:
                # Run ADB uninstall command
                result = subprocess.run(['adb', 'shell', 'pm', 'uninstall', '--user', '0', package_name], capture_output=True, text=True)
                logging.debug(f"ADB result: {result.stdout}")

                # Check the result
                if "Success" in result.stdout:
                    QMessageBox.information(self, "Success", f"Package {package_name} uninstalled.")
                    logging.info(f"{package_name} uninstalled successfully.")
                elif "Failure" in result.stdout:
                    QMessageBox.warning(self, "Error", f"Failed to uninstall {package_name}: {result.stdout}")
                    logging.error(f"Failed to uninstall {package_name}: {result.stdout}")
                else:
                    QMessageBox.warning(self, "Error", f"Unexpected response for {package_name}: {result.stdout}")
                    logging.error(f"Unexpected response for {package_name}: {result.stdout}")

            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                logging.critical(f"Error uninstalling package {package_name}: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AndroidDebloater()
    ex.show()
    sys.exit(app.exec_())