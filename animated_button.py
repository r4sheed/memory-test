# animated_button.py

from PyQt5.QtWidgets import QPushButton, QSizePolicy, QGraphicsOpacityEffect
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtGui import QFont

class AnimatedButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFont(QFont('Roboto', 14))
        self.setStyleSheet("""
            QPushButton {
                height: 30px; 
                background-color: #6c63ff; 
                color: white; 
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #5752d0;
            }
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setGraphicsEffect(self.create_opacity_effect(0))

    def create_opacity_effect(self, opacity):
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(opacity)
        return opacity_effect

    def set_opacity(self, opacity):
        self.graphicsEffect().setOpacity(opacity)

    opacity = pyqtProperty(float, fset=set_opacity)
