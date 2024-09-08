# **Android Debloater**

This tool provides an easy-to-use graphical interface (GUI) to help users manage and uninstall unnecessary packages (bloatware) on Android devices. It enables a streamlined approach to debloating, with the added option to enable Dark Mode for a more comfortable user experience.

## 💪 Features

- **Package Management**: Easily list, search, and uninstall selected Android packages (bloatware).
- **Dark Mode**: Optional Dark Mode to reduce eye strain.
- **Custom Icon**: The tool includes a custom Android-related icon for a personalized touch.

## 🧩 Requirements

- **ADB (Android Debug Bridge)** must be installed and properly set up on your system [Download](https://developer.android.com/tools/releases/platform-tools).
- **Python 3.x** (for those running the script version)
- **PyQt5** and **Pillow** for image processing (for those running the script version)

## 💻 Installation & Usage

### **Pre-built Executable (Recommended)**

Download the latest executable from the [Releases Section](https://github.com/oop7/Android_debloater/releases).

1. **Connect your Android device** to your computer with USB debugging enabled.
2. **Run the downloaded `.exe` file.**
3. **List Installed Packages**: Click on the `List Installed Packages` button to view all apps installed on your device.
4. **Search Packages**: Use the search bar to filter the list of packages.
5. Uninstall Packages: Select one or more packages and click on `Uninstall Selected Packages`.
6. **Enable Dark Mode**: Check the `Enable Dark Mode` checkbox for a more comfortable interface.

## Running from Source (Optional)

1. **Clone the repository**:
2. ```git clone https://github.com/oop7/Android_debloater.git```
3. **Install required dependencies**:```pip install -r requirements.txt```
4. **Run the tool**:```python android_debloater.py```

## Building the Executable (Optional)

### To build the tool into an executable using PyInstaller:

1. **Install PyInstaller**:```pip install pyinstaller```
2. **Build the executable**:```pyinstaller --onefile android_debloater.py```

This will generate an `.exe` file in the `dist/` directory.

## 📜 License

This project is licensed under the GLP-3.0 License. See the [LICENSE](LICENSE) file for details.

