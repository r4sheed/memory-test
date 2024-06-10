# Memory Test Application

The Memory Test Application is a Python-based application designed to test and improve your memory skills. It offers multiple game modes where users have to remember and input sequences of numbers shown on the screen.

## Features

- **Multiple Game Modes**:
  - **Mode 1**: Repeat Numbers
  - **Mode 2**: Reverse Order
  - **Mode 3**: Ascending Order
  - **Mode 4**: Descending Order
- **Three Rounds Per Game Mode**:
  - Number of numbers increases by 2 with each round.
  - Initial number of numbers is 4.
- **Statistics**:
  - Tracks correct and incorrect answers.
  - Shows results at the end of each game mode.
  - Logs results with date and game mode into a text file.

## Setup

### Prerequisites

- Python 3.6 or higher
- PyQt5 library

### Installation

1. Clone the repository:

```
git clone https://github.com/r4sheed/memory-test.git
cd memory-test
```

2. Install the required libraries:

```
pip install PyQt5
```

## Usage

1. Navigate to the project directory:

```
cd memory-test
```

2. Run the application:

```
python main.py
```

## Code Structure

- `main.py`: Entry point of the application.
- `main_window.py`: Contains the `MainWindow` class.
- `main_menu.py`: Contains the `MainMenu` class.
- `memory_mode.py`: Contains the `MemoryMode` and `BaseMode` classes.
- `game_logic.py`: Contains the `GameLogic` class for generating random numbers.
- `animated_button.py`: Contains the `AnimatedButton` class for creating animated buttons.
- `config.py`: Configuration settings for the application.

## Documentation

### main.py

This is the entry point of the application. It initializes the PyQt application and displays the main window.

### main_window.py

Contains the `MainWindow` class which sets up the main menu and the memory game modes. It handles switching between different game modes.

### main_menu.py

Contains the `MainMenu` class which sets up the main menu with animated buttons for each game mode. It includes animation effects for the buttons.

### memory_mode.py

Contains the `BaseMode` and `MemoryMode` classes. `BaseMode` provides common functionalities for the game modes. `MemoryMode` handles the specific logic for each memory game mode, including generating numbers, showing them, and evaluating the user's input.

### game_logic.py

Contains the `GameLogic` class, which generates unique random numbers for the memory tests.

### animated_button.py

Contains the `AnimatedButton` class, which extends `QPushButton` to add animation effects for better user experience.

### config.py

Contains configuration settings for the application, such as the number of rounds, initial numbers, increment per round, and the range of numbers.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- PyQt5: Python bindings for the Qt application framework.

