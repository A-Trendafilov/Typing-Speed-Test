from PyQt6.QtWidgets import QApplication

from app import ClientViewWindow


def main():
    app = QApplication([])
    window = ClientViewWindow()
    with open("style.css", "r") as file:
        window.setStyleSheet(file.read())
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
