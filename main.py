import sys
import threading
import time
import pygetwindow as gw
import pyautogui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QStackedWidget, QLineEdit, QSpinBox, QShortcut, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class Zoohack(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Zoohack")
        self.setGeometry(200, 200, 400, 400)

        # Set app icon
        self.setWindowIcon(QIcon('zoom.ico'))  # Load the zoom.ico as app icon

        # Set background to black
        self.set_background()

        # Initialize spam raise hand and mass ping state
        self.spam_raise_hand_active = False
        self.spam_raise_hand_thread = None
        self.mass_ping_active = False
        self.mass_ping_thread = None

        # Create central widget and layout
        self.centralWidget = QWidget(self)  # Use centralWidget correctly here
        self.setCentralWidget(self.centralWidget)  # Correct reference here
        layout = QVBoxLayout(self.centralWidget)

        # Create a QStackedWidget to hold the different content
        self.stacked_widget = QStackedWidget(self.centralWidget)

        # Create three tabs (buttons)
        self.tab1_button = QPushButton("General", self)
        self.tab2_button = QPushButton("Exploits", self)
        self.tab3_button = QPushButton("Chat", self)

        # Style the tab buttons
        self.tab1_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: rgba(0, 0, 0, 0.1);
                border: none;
                font-size: 20px;
                padding: 12px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)
        self.tab2_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: rgba(0, 0, 0, 0.1);
                border: none;
                font-size: 20px;
                padding: 12px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)
        self.tab3_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: rgba(0, 0, 0, 0.1);
                border: none;
                font-size: 20px;
                padding: 12px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)

        # Add buttons to the layout for the tabs
        tab_button_layout = QHBoxLayout()
        tab_button_layout.addWidget(self.tab1_button)
        tab_button_layout.addWidget(self.tab2_button)
        tab_button_layout.addWidget(self.tab3_button)
        layout.addLayout(tab_button_layout)

        # Create the content for each tab
        self.tab1 = QWidget(self)
        self.tab2 = QWidget(self)
        self.tab3 = QWidget(self)

        # Add content to Tab 1 (General)
        self.create_feature_toggle("Enable Mic", self.tab1)
        self.create_feature_toggle("Enable Camera", self.tab1)
        self.create_feature_toggle("Enable Camera+Mic", self.tab1)

        # Add content to Tab 2 (Exploits)
        self.create_feature_toggle("Spam Raise Hand", self.tab2)

        # Add content to Tab 3 (Chat)
        self.create_chat_section(self.tab3)

        # Add the tabs to the QStackedWidget
        self.stacked_widget.addWidget(self.tab1)
        self.stacked_widget.addWidget(self.tab2)
        self.stacked_widget.addWidget(self.tab3)
        layout.addWidget(self.stacked_widget)

        # Watermark at the bottom
        self.watermark_label = QLabel("Made by Dopaminess", self)
        self.watermark_label.setAlignment(Qt.AlignCenter)
        self.watermark_label.setStyleSheet("QLabel { font-size: 10px; color: gray; }")
        layout.addWidget(self.watermark_label)

        # Connect the tab buttons to switch between content
        self.tab1_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.tab2_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.tab3_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        # Add a shortcut for mass ping (Ctrl+P) in the Chat tab
        self.shortcut_mass_ping = QShortcut(Qt.CTRL + Qt.Key_P, self)
        self.shortcut_mass_ping.activated.connect(lambda: self.ping_toggle_button.click())

    def set_background(self):
        """Set the background to black."""
        self.setStyleSheet("""
            QWidget {
                background-color: black;  /* Set black background */
                color: white;  /* Set all text color to white */
                font-family: 'Comic Sans MS';  /* Apply Comic Sans MS font */
            }
            QPushButton {
                color: white;  /* Set text color to white for buttons */
                background-color: #333;  /* Dark button background */
                border: 2px solid #555;
                border-radius: 10px;
                font-size: 16px;  /* Increase font size */
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QLabel {
                color: white;  /* Ensure all QLabel text is white */
            }
        """)

    def create_feature_toggle(self, feature_name, tab):
        """Create a label and a toggle switch for a specific feature."""
        feature_layout = QHBoxLayout()

        # Create label with larger font size
        label = QLabel(feature_name, self)
        label.setStyleSheet("QLabel { font-size: 18px; color: white; }")
        feature_layout.addWidget(label)

        # Create toggle button
        toggle_button = QPushButton(self)
        toggle_button.setText("OFF")
        toggle_button.setCheckable(True)
        toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #ccc;
                border-radius: 20px;
                width: 60px;
                height: 30px;
            }
        """)

        # Connect the button click to the toggle function.
        toggle_button.clicked.connect(lambda: self.toggle(toggle_button, feature_name))
        feature_layout.addWidget(toggle_button)

        # Add layout to the given tab
        tab_layout = tab.layout() if tab.layout() else QVBoxLayout(tab)
        tab_layout.addLayout(feature_layout)
        tab.setLayout(tab_layout)

    def create_chat_section(self, tab):
        """Create the mass ping feature in the Chat tab."""
        chat_layout = QVBoxLayout()

        # Label and input for the message
        self.ping_message_input = QLineEdit(self)
        self.ping_message_input.setPlaceholderText("Enter message to spam...")
        self.ping_message_input.setStyleSheet("QLineEdit { font-size: 18px; }")
        chat_layout.addWidget(self.ping_message_input)

        # Input for spam speed (in milliseconds)
        self.speed_input = QSpinBox(self)
        self.speed_input.setMinimum(100)  # Minimum 100ms delay
        self.speed_input.setMaximum(2000)  # Maximum 2 seconds delay
        self.speed_input.setValue(500)  # Default to 500ms delay
        self.speed_input.setStyleSheet("QSpinBox { font-size: 18px; }")
        chat_layout.addWidget(QLabel("Spam Speed (ms):", self))
        chat_layout.addWidget(QLabel("Hotkey: CTRL+P", self))
        chat_layout.addWidget(self.speed_input)

        # Toggle button to start/stop mass ping
        self.ping_toggle_button = QPushButton("Start Chat Spamming", self)
        self.ping_toggle_button.setCheckable(True)
        self.ping_toggle_button.setStyleSheet("""
            QPushButton {
                color: black;
                background-color: #ccc;
                border-radius: 20px;
                width: 160px;
                height: 40px;
            }
        """)
        self.ping_toggle_button.clicked.connect(self.toggle_mass_ping)
        chat_layout.addWidget(self.ping_toggle_button)

        tab.setLayout(chat_layout)

    def toggle(self, toggle_button, feature_name):
        """Toggle the switch state and trigger the feature action."""
        if toggle_button.isChecked():
            toggle_button.setText("ON")
            toggle_button.setStyleSheet("""
                QPushButton {
                    background-color: green;
                    border-radius: 20px;
                    width: 60px;
                    height: 30px;
                }
            """)
            if feature_name == "Spam Raise Hand":
                self.start_spam_raise_hand()
            else:
                self.trigger_zoom_action(feature_name)
        else:
            toggle_button.setText("OFF")
            toggle_button.setStyleSheet("""
                QPushButton {
                    background-color: #ccc;
                    border-radius: 20px;
                    width: 60px;
                    height: 30px;
                }
            """)
            if feature_name == "Spam Raise Hand":
                self.stop_spam_raise_hand()

    def toggle_mass_ping(self):
        """Start or stop mass pinging."""
        if self.ping_toggle_button.isChecked():
            self.ping_toggle_button.setText("Stop Mass Ping")
            self.start_mass_ping()
        else:
            self.ping_toggle_button.setText("Start Mass Ping")
            self.stop_mass_ping()

    def start_mass_ping(self):
        """Start spamming the entered message."""
        if not self.mass_ping_active:
            self.mass_ping_active = True
            self.mass_ping_thread = threading.Thread(target=self.mass_ping_worker, daemon=True)
            self.mass_ping_thread.start()

    def stop_mass_ping(self):
        """Stop spamming the entered message."""
        if self.mass_ping_active:
            self.mass_ping_active = False
            if self.mass_ping_thread:
                self.mass_ping_thread.join(timeout=1)

    def mass_ping_worker(self):
        """Worker thread that repeatedly sends the ping message."""
        message = self.ping_message_input.text()
        speed = self.speed_input.value() / 1000  # Convert to seconds
        while self.mass_ping_active:
            if message and self.bring_zoom_to_front():
                pyautogui.write(message)
                pyautogui.press('enter')
                time.sleep(speed)  # Control spam speed

    def trigger_zoom_action(self, feature_name):
        """Trigger the corresponding Zoom hotkey based on the feature."""
        if self.bring_zoom_to_front():
            if feature_name == "Enable Mic":
                pyautogui.hotkey('alt', 'a')
            elif feature_name == "Enable Camera":
                pyautogui.hotkey('alt', 'v')
            elif feature_name == "Enable Camera+Mic":
                pyautogui.hotkey('alt', 'shift', 'a')
            print(f"{feature_name} toggled.")
        else:
            print("Zoom is not active. Could not bring Zoom to the front.")

    def start_spam_raise_hand(self):
        """Start spamming the raise hand hotkey (Alt+Y)."""
        if not self.spam_raise_hand_active:
            self.spam_raise_hand_active = True
            self.spam_raise_hand_thread = threading.Thread(target=self.spam_raise_hand_worker, daemon=True)
            self.spam_raise_hand_thread.start()
            print("Started spamming raise hand.")

    def stop_spam_raise_hand(self):
        """Stop spamming the raise hand hotkey."""
        if self.spam_raise_hand_active:
            self.spam_raise_hand_active = False
            if self.spam_raise_hand_thread:
                self.spam_raise_hand_thread.join(timeout=1)
            print("Stopped spamming raise hand.")

    def spam_raise_hand_worker(self):
        """Worker thread that continuously sends Alt+Y hotkey."""
        while self.spam_raise_hand_active:
            if self.bring_zoom_to_front():
                pyautogui.hotkey('alt', 'y')
                print("Raise hand hotkey sent.")
            time.sleep(0.5)  # Adjust the delay as needed

    def bring_zoom_to_front(self):
        """Bring the Zoom window to the front."""
        zoom_windows = gw.getWindowsWithTitle('Zoom')
        if not zoom_windows:
            zoom_windows = gw.getWindowsWithTitle('Zoom Meeting')
        if zoom_windows:
            zoom_window = zoom_windows[0]
            zoom_window.activate()
            return True
        else:
            print("Zoom window not found.")
            return False

def main():
    app = QApplication(sys.argv)
    window = Zoohack()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

# Made by @wtirexoo
