
import sys
import os
import subprocess
import platform
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QLabel,
    QTabWidget,
    QMessageBox,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont

# --- Global Stylesheet ---
STYLESHEET = """
    QMainWindow {
        background-color: #f0f0f0;
    }
    QWidget#sidebar {
        background-color: #2c3e50;
        border-right: 2px solid #253545;
    }
    QPushButton.sidebar-btn {
        background-color: #34495e;
        color: white;
        border: none;
        padding: 15px;
        text-align: left;
        font-size: 16px;
        border-radius: 8px;
    }
    QPushButton.sidebar-btn:hover {
        background-color: #4a6fa5;
    }
    QPushButton.sidebar-btn:checked {
        background-color: #1abc9c;
    }
    QStackedWidget {
        background-color: white;
    }
    QTabWidget::pane {
        border: 1px solid #dcdcdc;
        border-top: none;
    }
    QTabBar::tab {
        background: #f0f0f0;
        border: 1px solid #dcdcdc;
        padding: 10px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
    QTabBar::tab:selected {
        background: white;
        border-bottom-color: white;
    }
    QPushButton {
        background-color: #3498db;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 14px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #2980b9;
    }
    QLabel {
        font-size: 14px;
    }
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modern PySide6 App")
        self.setGeometry(100, 100, 1200, 800)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Sidebar ---
        self.sidebar = self.build_sidebar()
        main_layout.addWidget(self.sidebar)

        # --- Content Area ---
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # --- Build Pages ---
        self.ecom_page = self.build_ecom_page()
        self.youtube_page = self.build_youtube_page()
        self.settings_page = self.build_settings_page()

        self.stacked_widget.addWidget(self.ecom_page)
        self.stacked_widget.addWidget(self.youtube_page)
        self.stacked_widget.addWidget(self.settings_page)

        # --- Initial Page ---
        self.show_ecom_page()

    def build_sidebar(self):
        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("sidebar")
        sidebar_widget.setFixedWidth(200)

        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(15)

        # --- Buttons ---
        self.ecom_button = QPushButton("Ecom")
        self.ecom_button.setCheckable(True)
        self.ecom_button.setProperty("class", "sidebar-btn")
        self.ecom_button.clicked.connect(self.show_ecom_page)
        sidebar_layout.addWidget(self.ecom_button)

        self.youtube_button = QPushButton("YouTube/TikTok")
        self.youtube_button.setCheckable(True)
        self.youtube_button.setProperty("class", "sidebar-btn")
        self.youtube_button.clicked.connect(self.show_youtube_page)
        sidebar_layout.addWidget(self.youtube_button)

        # Spacer to push settings to the bottom
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sidebar_layout.addSpacerItem(spacer)

        self.settings_button = QPushButton("Settings")
        self.settings_button.setCheckable(True)
        self.settings_button.setProperty("class", "sidebar-btn")
        self.settings_button.clicked.connect(self.show_settings_page)
        sidebar_layout.addWidget(self.settings_button)

        return sidebar_widget

    def update_active_button(self, active_button):
        for button in [self.ecom_button, self.youtube_button, self.settings_button]:
            button.setChecked(button is active_button)

    def show_ecom_page(self):
        self.stacked_widget.setCurrentWidget(self.ecom_page)
        self.update_active_button(self.ecom_button)

    def show_youtube_page(self):
        self.stacked_widget.setCurrentWidget(self.youtube_page)
        self.update_active_button(self.youtube_button)

    def show_settings_page(self):
        self.stacked_widget.setCurrentWidget(self.settings_page)
        self.update_active_button(self.settings_button)

    def build_ecom_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        for i in range(1, 5):
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)
            tab_layout.addWidget(QLabel(f"Content for Ecom Future {i}"))
            tab_widget.addTab(tab, f"Future {i}")

        return page

    def build_youtube_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        for i in range(1, 5):
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)
            tab_layout.addWidget(QLabel(f"Content for YouTube/TikTok Future {i}"))
            tab_widget.addTab(tab, f"Future {i}")

        return page

    def build_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(20, 20, 20, 20)

        self.update_button = QPushButton("Update App")
        self.update_button.clicked.connect(self.run_update)
        layout.addWidget(self.update_button)

        self.restart_button = QPushButton("Restart App")
        self.restart_button.clicked.connect(self.restart_app)
        layout.addWidget(self.restart_button)

        self.update_status_label = QLabel("")
        layout.addWidget(self.update_status_label)

        return page

    def restart_app(self):
        """Restarts the current application."""
        try:
            QApplication.quit()
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to restart the application: {e}")

    def run_update(self):
        """Runs the external update script."""
        self.update_status_label.setText("Updating... please wait")
        QApplication.processEvents()

        os_type = platform.system()
        script_name = "update_app.bat" if os_type == "Windows" else "update_app.sh"

        script_path = Path(__file__).parent / script_name
        if not script_path.exists():
            QMessageBox.critical(self, "Error", f"Update script '{script_name}' not found.")
            self.update_status_label.setText(f"Update failed: {script_name} not found")
            return

        try:
            subprocess.run([str(script_path)], check=True, capture_output=True, text=True)
            self.update_status_label.setText("Update successful, restarting...")
            QApplication.processEvents()
            self.restart_app()
        except subprocess.CalledProcessError as e:
            error_message = f"Update failed with exit code {e.returncode}.\\n\\nOutput:\\n{e.stdout}\\n\\nError:\\n{e.stderr}"
            QMessageBox.critical(self, "Update Failed", error_message)
            self.update_status_label.setText("Update failed.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
            self.update_status_label.setText("Update failed.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
