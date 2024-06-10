# memory_mode.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIntValidator
from game_logic import GameLogic
from config import GAME_CONFIG, LOG_FILE
from datetime import datetime

class BaseMode(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.logic = GameLogic()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.instruction_label = QLabel()
        self.instruction_label.setFont(QFont('Roboto', 14))
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setWordWrap(True)
        self.layout.addWidget(self.instruction_label)

        self.guesses_label = QLabel('')
        self.guesses_label.setFont(QFont('Roboto', 16))
        self.guesses_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.guesses_label)

        self.number_input = QLineEdit()
        self.number_input.setFont(QFont('Roboto', 36))
        self.number_input.setAlignment(Qt.AlignCenter)
        self.number_input.setReadOnly(True)
        self.number_input.setFixedHeight(75)
        self.number_input.setFixedWidth(75)
        self.number_input.setStyleSheet("QLineEdit { border: 1px solid gray; }")
        self.number_input.setValidator(QIntValidator(GAME_CONFIG['number_range'][0], GAME_CONFIG['number_range'][1]))  # Only allow numbers in the generated range
        self.layout.addWidget(self.number_input, alignment=Qt.AlignCenter)

        self.submit_button = QPushButton('Submit')
        self.submit_button.setFont(QFont('Roboto', 14))
        self.submit_button.setStyleSheet("""
            QPushButton {
                height: 40px; 
                width: 200px;
                background-color: #d3d3d3; 
                color: white; 
                border-radius: 10px;
            }
            QPushButton:enabled {
                background-color: #6c63ff; 
                color: white; 
                border-radius: 10px;
            }
            QPushButton:enabled:hover {
                background-color: #5752d0;
            }
        """)
        self.submit_button.clicked.connect(self.submit_wrapper)
        self.submit_button.setEnabled(False)
        self.layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

        self.number_input.returnPressed.connect(self.submit_wrapper)  # Connect the returnPressed signal to the submit method

        self.setLayout(self.layout)

    def submit_wrapper(self):
        if not self.number_input.isReadOnly():
            self.submit()

    def submit(self):
        if self.number_input.isReadOnly():
            return  # Don't allow submission if still showing numbers
        if len(self.user_answers) < len(self.numbers):
            try:
                user_input = int(self.number_input.text())
                if user_input < GAME_CONFIG['number_range'][0] or user_input > GAME_CONFIG['number_range'][1]:
                    QMessageBox.warning(self, "Invalid Input", "Please enter a number within the valid range.")
                    self.number_input.clear()
                    return
                if user_input in self.user_answers:
                    QMessageBox.warning(self, "Duplicate Input", "You have already entered this number. Please enter a different number.")
                    self.number_input.clear()
                    return
                self.user_answers.append(user_input)
                self.update_guesses_label()
                self.number_input.clear()
                if len(self.user_answers) < len(self.numbers):
                    self.number_input.setFocus()
                else:
                    self.submit_button.setEnabled(False)
                    self.evaluate_round_results()
                    if self.current_round < GAME_CONFIG['rounds']:
                        self.current_round += 1
                        self.start_mode()
                    else:
                        self.evaluate_results()
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")
        else:
            self.submit_button.setEnabled(False)
            self.evaluate_results()

    def evaluate_round_results(self):
        if self.mode == 1:
            round_correct = sum([1 for i, j in zip(self.user_answers, self.numbers) if i == j])
        elif self.mode == 2:
            round_correct = sum([1 for i, j in zip(self.user_answers, reversed(self.numbers)) if i == j])
        elif self.mode == 3:
            round_correct = sum([1 for i, j in zip(self.user_answers, sorted(self.numbers)) if i == j])
        elif self.mode == 4:
            round_correct = sum([1 for i, j in zip(self.user_answers, sorted(self.numbers, reverse=True)) if i == j])

        round_incorrect = len(self.numbers) - round_correct
        self.correct_answers += round_correct
        self.incorrect_answers += round_incorrect

class MemoryMode(BaseMode):
    def __init__(self, parent=None, mode=1, main_window=None):
        super().__init__(parent, main_window)
        self.mode = mode
        self.numbers = []
        self.current_index = 0
        self.user_answers = []
        self.set_instructions()
        self.current_round = 1
        self.correct_answers = 0
        self.incorrect_answers = 0

    def set_instructions(self):
        instructions = {
            1: 'Remember the numbers displayed. After all the numbers have been shown, enter them one by one in the same order. Try to get as many correct as possible. Click "Submit" after entering the numbers.',
            2: 'Remember the numbers displayed. After all the numbers have been shown, enter them one by one in reverse order. Try to get as many correct as possible. Click "Submit" after entering the numbers.',
            3: 'Remember the numbers displayed. After all the numbers have been shown, enter them one by one in ascending order. Try to get as many correct as possible. Click "Submit" after entering the numbers.',
            4: 'Remember the numbers displayed. After all the numbers have been shown, enter them one by one in descending order. Try to get as many correct as possible. Click "Submit" after entering the numbers.'
        }
        self.instruction_label.setText(instructions.get(self.mode, ''))

    def start_mode(self):
        self.numbers = self.logic.generate_unique_numbers(
            GAME_CONFIG['initial_numbers'] + GAME_CONFIG['increment_per_round'] * (self.current_round - 1),
            GAME_CONFIG['number_range'][0],
            GAME_CONFIG['number_range'][1]
        )
        self.current_index = 0
        self.user_answers = []
        self.number_input.clear()
        self.guesses_label.setText(self.format_guesses_label())
        self.number_input.setReadOnly(True)
        self.submit_button.setEnabled(False)
        try:
            self.number_input.returnPressed.disconnect(self.submit_wrapper)
        except TypeError:
            pass
        self.show_next_number()

    def show_next_number(self):
        if self.current_index < len(self.numbers):
            self.number_input.setText(str(self.numbers[self.current_index]))
            self.current_index += 1
            QTimer.singleShot(1000, self.clear_number)
        else:
            self.number_input.clear()
            self.number_input.setReadOnly(False)
            self.submit_button.setEnabled(True)
            self.number_input.returnPressed.connect(self.submit_wrapper)
            self.number_input.setFocus()

    def clear_number(self):
        self.number_input.clear()
        QTimer.singleShot(500, self.show_next_number)

    def update_guesses_label(self):
        self.guesses_label.setText(self.format_guesses_label())

    def format_guesses_label(self):
        displayed_numbers = [str(self.user_answers[i]) if i < len(self.user_answers) else "_" for i in range(len(self.numbers))]
        return ' - '.join(displayed_numbers)

    def evaluate_results(self):
        self.show_final_results()
        self.log_results()
        self.current_round = 1
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.main_window.stack.setCurrentWidget(self.main_window.main_menu)

    def show_final_results(self):
        total_answers = self.correct_answers + self.incorrect_answers
        correct_percentage = (self.correct_answers / total_answers) * 100 if total_answers > 0 else 0
        incorrect_percentage = 100 - correct_percentage
        QMessageBox.information(self, "Final Result", 
                                f"Correct: {self.correct_answers}, Incorrect: {self.incorrect_answers}\n"
                                f"Correct percentage: {correct_percentage:.2f}%, Incorrect percentage: {incorrect_percentage:.2f}%")

    def log_results(self):
        total_answers = self.correct_answers + self.incorrect_answers
        correct_percentage = (self.correct_answers / total_answers) * 100 if total_answers > 0 else 0
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(f"{datetime.now()} - Mode {self.mode}\n")
            log_file.write(f"Correct: {self.correct_answers}, Incorrect: {self.incorrect_answers}\n")
            log_file.write(f"Correct percentage: {correct_percentage:.2f}%\n")
            log_file.write("-----------\n")
