# main_menu.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QSequentialAnimationGroup, QPropertyAnimation
from animated_button import AnimatedButton

class MainMenu(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        buttons = [
            self.create_button('Mode 1: Repeat Numbers', lambda: self.main_window.switch_to_mode(1)),
            self.create_button('Mode 2: Reverse Order', lambda: self.main_window.switch_to_mode(2)),
            self.create_button('Mode 3: Ascending Order', lambda: self.main_window.switch_to_mode(3)),
            self.create_button('Mode 4: Descending Order', lambda: self.main_window.switch_to_mode(4))
        ]

        for button in buttons:
            layout.addWidget(button)

        self.setLayout(layout)
        self.animate_buttons(buttons)

    def create_button(self, text, method):
        button = AnimatedButton(text)
        button.clicked.connect(method)
        return button

    def animate_buttons(self, buttons):
        animation_group = QSequentialAnimationGroup(self)
        for button in buttons:
            animation = QPropertyAnimation(button, b'opacity')
            animation.setDuration(350)
            animation.setStartValue(0)
            animation.setEndValue(1)
            animation_group.addAnimation(animation)
        animation_group.start()
