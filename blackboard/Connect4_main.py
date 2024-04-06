import tkinter as tk
from Blackboard import Blackboard
from GameBoardUI import GameBoardUI
from GameMenuUI import UIManager
from MoveProcessor import MoveProcessor
from MoveValidator import MoveValidator
from MonteCarlo import MonteCarlo
from AlphaBetaPrune import AlphaBeta
from WinCheck import WinChecker
from PlayerManager import PlayerManager

from threading import Thread

# class Connect4:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("Connect 4")
#         self.blackboard = Blackboard  # This is passed to every other class, hence why blackboard is the cental architecture
#         self.opponent = AlphaBeta(self.blackboard)
#
#
#         self.game_board_ui = GameBoardUI(self.root, self.blackboard, self.input_handler)
#         self.input_handler.game_board_ui = self.game_board_ui  # Update the placeholder with actual UI reference
#
#
#
#     def run(self):
#         self.root.mainloop()
#
# if __name__ == "__main__":
#     game = Connect4()
#     game.run()

class Connect4:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect 4")
        self.blackboard = Blackboard
        self.game_menu_ui = None
        self.game_board_ui = None
        self.initialize_ui()

    def initialize_ui(self):
        """Initialize the UI manager or directly the GameMenuUI here."""
        self.game_menu_ui = UIManager(self.root, self.start_game)  # Assuming UIManager requires a callback
        self.game_menu_ui.show_menu()  # Assuming there's a method to show the menu

    def start_game(self):
        """Transition from the game menu to the game board."""
        # Clear the menu UI and prepare the game board UI
        self.game_board_ui = GameBoardUI(self.blackboard)
        self.game_board_ui.show_board()  # Assuming there's a method to display the board

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = Connect4()
    game.run()

## Currently need to update the gameloop for tk and then get the game logic implemented with it. A good example im gonna use
# as influence is https://github.com/saiduc/Connect-4-Tkinter/blob/master/gamegui.py
