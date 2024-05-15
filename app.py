from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from qt_material import apply_stylesheet


class ClientView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Typing Speed Test Application")
        self.app_layout = AppLayout()
        self.setCentralWidget(self.app_layout)


class AppWidget(QWidget):
    def __init__(self):
        super().__init__()


class AppLayout(QWidget):
    def __init__(self):
        super().__init__()


def main():
    # Create the application instance
    app = QApplication([])
    # Create the main window
    window = ClientView()
    # Apply style using qt material styles
    apply_stylesheet(app, theme="dark_teal.xml")
    # Show the main window
    window.show()
    # Run the application event loop
    app.exec()


if __name__ == "__main__":
    main()
