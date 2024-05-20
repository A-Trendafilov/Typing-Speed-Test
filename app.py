from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QPushButton, QTextEdit, QVBoxLayout,
                             QWidget)

DURATION_INT = 60
DEFAULT_TEXT = (
    "The quick brown fox jumps over the lazy dog. Jackdaws love my big sphinx of quartz. Mr. Jock, "
    "TV quiz PhD, bags few lynx. Sphinx of black quartz, judge my vow. How razorback-jumping frogs can "
    "level six piqued gymnasts. Crazy Fredericka bought many very exquisite opal jewels. Sixty zippers "
    "were quickly picked from the woven jute bag. Woven silk pyjamas exchanged for blue quartz."
)
RESET_TIME = "01:00"


def secs_to_minsec(secs: int) -> str:
    mins = secs // 60
    secs = secs % 60
    return f"{mins:02}:{secs:02}"


class ClientViewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Typing Speed Test Application")
        self.setFixedSize(800, 600)
        self.setCentralWidget(AppLayoutWidget())


class AppWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.title = None
        self.sample_text = None
        self.time_label = None
        self.countdown_label = None
        self.reset_btn = None
        self.entry_text = None
        self.wpm_label = None
        self.accuracy_label = None
        self.init_ui()
        self.time_left = None
        self.timer_running = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.current_word_index = 0
        self.words = self.sample_text.toPlainText().split()
        self.highlight_current_word()

        self.total_keystrokes = 0
        self.correct_keystrokes = 0

    def init_ui(self):
        self.title = QLabel("Test your typing skills.")

        self.sample_text = QTextEdit(DEFAULT_TEXT)
        self.sample_text.setReadOnly(True)

        self.time_label = QLabel("Time Left: ")
        self.countdown_label = QLabel(RESET_TIME)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setIcon(QIcon("./image/refresh.png"))
        self.reset_btn.clicked.connect(self.reset)

        self.entry_text = QLineEdit(self)
        self.entry_text.setPlaceholderText("Start typing here...")
        self.entry_text.textChanged.connect(self.start_typing)

        self.wpm_label = QLabel("WPM: 0")
        self.accuracy_label = QLabel("Accuracy: 0%")

    def start_typing(self):
        if not self.timer_running:
            self.start_timer()

        if self.current_word_index < len(self.words):
            entered_word = self.entry_text.text().strip().lower()
            current_word = self.words[self.current_word_index].lower()
            self.total_keystrokes += len(entered_word)
            self.correct_keystrokes += sum(
                1 for ec, cc in zip(entered_word, current_word) if ec == cc
            )
            if entered_word == current_word:
                self.current_word_index += 1
                self.entry_text.clear()
                self.highlight_current_word()

            self.update_result()

            if self.current_word_index == len(self.words):
                self.stop_timer()
        else:
            self.stop_timer()

    def highlight_current_word(self):
        highlighted_text = ""
        for i, word in enumerate(self.words):
            if i == self.current_word_index:
                highlighted_text += (
                    f"<span style='background-color: #cc00cc;'>{word}</span> "
                )
            else:
                highlighted_text += f"{word} "
        self.sample_text.setHtml(highlighted_text)

    def start_timer(self):
        self.time_left = DURATION_INT
        self.timer_running = True
        self.timer.start(1000)
        self.update_timer()

    def stop_timer(self):
        self.timer.stop()
        self.timer_running = False
        self.entry_text.setEnabled(False)

    def update_timer(self):
        if self.timer_running and self.time_left is not None:
            self.countdown_label.setText(secs_to_minsec(self.time_left))
            if self.time_left > 0:
                self.time_left -= 1
            else:
                self.stop_timer()
                self.update_result()

    def reset(self):
        self.stop_timer()
        self.current_word_index = 0
        self.highlight_current_word()
        self.entry_text.clear()
        self.countdown_label.setText(RESET_TIME)
        self.wpm_label.setText("WPM: 0")
        self.accuracy_label.setText("Accuracy: 0%")
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.entry_text.setEnabled(True)

    def update_result(self):
        time_spent = (
            DURATION_INT - self.time_left
            if self.time_left is not None
            else DURATION_INT
        )
        words_typed = self.current_word_index
        wpm = words_typed / (time_spent / 60) if time_spent > 0 else 0
        accuracy = (
            (self.correct_keystrokes / self.total_keystrokes * 100)
            if self.total_keystrokes > 0
            else 0
        )
        accuracy = max(0, min(accuracy, 100))
        self.wpm_label.setText(f"WPM: {wpm:.0f}")
        self.accuracy_label.setText(f"Accuracy: {accuracy:.0f}%")


class AppLayoutWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.app_widget = None
        self.main_layout = None
        self.sample_frame = None
        self.sample_layout = None
        self.ctrl_frame = None
        self.ctrl_layout = None
        self.entry_frame = None
        self.entry_layout = None
        self.init_layout()

    def init_layout(self):
        self.app_widget = AppWidget()
        self.main_layout = QVBoxLayout(self)

        self.sample_frame = QFrame(self)
        self.sample_layout = QHBoxLayout(self.sample_frame)

        self.entry_frame = QFrame(self)
        self.entry_layout = QHBoxLayout(self.entry_frame)

        self.ctrl_frame = QFrame(self)
        self.ctrl_layout = QVBoxLayout(self.ctrl_frame)

        self.sample_layout.addWidget(self.app_widget.sample_text)
        self.sample_layout.addWidget(self.ctrl_frame)

        self.ctrl_layout.addWidget(self.app_widget.reset_btn)
        self.ctrl_layout.addWidget(self.app_widget.wpm_label)
        self.ctrl_layout.addWidget(self.app_widget.accuracy_label)

        self.entry_layout.addWidget(self.app_widget.entry_text)
        self.entry_layout.addWidget(self.app_widget.time_label)
        self.entry_layout.addWidget(self.app_widget.countdown_label)

        self.main_layout.addWidget(self.app_widget.title, Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.sample_frame, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.entry_frame, Qt.AlignmentFlag.AlignBottom)
