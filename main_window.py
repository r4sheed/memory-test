# main_window.py

from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from main_menu import MainMenu
from memory_mode import MemoryMode
from config import GAME_TITLE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(GAME_TITLE)
        self.setFixedSize(300, 300)

        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        self.main_menu = MainMenu(self)
        self.stack.addWidget(self.main_menu)

        self.memory_modes = []
        for i in range(1, 5):
            memory_mode = MemoryMode(self, mode=i, main_window=self)
            self.memory_modes.append(memory_mode)
            self.stack.addWidget(memory_mode)

    def switch_to_mode(self, mode):
        if 1 <= mode <= 4:
            self.stack.setCurrentWidget(self.memory_modes[mode - 1])
            self.memory_modes[mode - 1].start_mode()
