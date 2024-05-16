from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)
from qt_material import apply_stylesheet

DURATION_INT = 60


def secs_to_minsec(secs: int):
    mins = secs // 60
    secs = secs % 60
    minsec = f"{mins:02}:{secs:02}"
    return minsec


class ClientView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Typing Speed Test Application")
        self.app_layout = AppLayout()
        self.setCentralWidget(self.app_layout)


class AppWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.title = QLabel("Test your typing skills")
        self.sample_text = QTextEdit("Example text for test your typing skills")
        self.sample_text.setReadOnly(True)
        self.timer = QLabel("01:00")
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setIcon(QIcon("./image/refresh.png"))
        self.entry_text = QLineEdit()
        self.entry_text.setPlaceholderText("Start typing here...")


class EventHandler:
    def __init__(self, app_widget):
        self.app_widget = app_widget
        self.time_left = None
        self.timer_running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.current_word_index = 0
        self.words = self.app_widget.sample_text.toPlainText().split()
        self.highlight_current_word()
        print(self.words)

    def start_typing(self):
        if not self.timer_running:
            self.start_timer()

        if self.current_word_index < len(self.words):
            entered_word = self.app_widget.entry_text.text().strip().lower()
            current_word = self.words[self.current_word_index].lower()
            if entered_word == current_word:
                self.current_word_index += 1
                self.app_widget.entry_text.clear()
                self.highlight_current_word()

            if self.current_word_index == len(self.words):
                self.stop_timer()
        else:
            self.stop_timer()

    def highlight_current_word(self):
        highlighted_text = ""
        for i, word in enumerate(self.words):
            if i == self.current_word_index:
                highlighted_text += (
                    f"<span style='background-color: black;'>{word}</span> "
                )
            else:
                highlighted_text += f"{word} "
        self.app_widget.sample_text.setHtml(highlighted_text)

    def start_timer(self):
        self.time_left = DURATION_INT
        self.timer_running = True
        self.timer.start(1000)
        self.update_timer()

    def stop_timer(self):
        self.timer.stop()
        self.timer_running = False
        self.time_left = None

    def update_timer(self):
        if self.timer_running:
            minsec = secs_to_minsec(self.time_left)
            self.app_widget.timer.setText(minsec)
            if self.time_left > 0:
                self.time_left -= 1
        else:
            self.stop_timer()

    def reset(self):
        self.stop_timer()
        self.current_word_index = 0
        self.highlight_current_word()
        self.app_widget.entry_text.clear()
        self.app_widget.timer.setText("01:00")


class AppLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.app_widget = AppWidget()
        self.main_layout = QVBoxLayout(self)

        self.sample_frame = QFrame(self)
        self.sample_layout = QHBoxLayout(self.sample_frame)

        self.entry_frame = QFrame(self)
        self.entry_layout = QHBoxLayout(self.entry_frame)

        self.sample_layout.addWidget(self.app_widget.sample_text)
        self.sample_layout.addWidget(self.app_widget.reset_btn)

        self.entry_layout.addWidget(self.app_widget.entry_text)
        self.entry_layout.addWidget(self.app_widget.timer)

        self.main_layout.addWidget(self.app_widget.title, Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.sample_frame, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.entry_frame, Qt.AlignmentFlag.AlignBottom)

        self.event = EventHandler(self.app_widget)
        self.app_widget.reset_btn.clicked.connect(self.event.reset)
        self.app_widget.entry_text.textChanged.connect(self.event.start_typing)


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
