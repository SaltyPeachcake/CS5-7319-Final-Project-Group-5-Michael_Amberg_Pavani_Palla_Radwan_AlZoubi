import tkinter as tk
from tkinter import ttk


class UIManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect 4 Game Menu")
        self.root.geometry("400x300")

        self.setup_ui()

    def setup_ui(self):
        # Display the game name with "Connect" in yellow and "-4" in red
        self.title_label = tk.Label(self.root, text="Connect", fg="yellow", font=("Arial", 24))
        self.title_label.pack()
        self.title_label2 = tk.Label(self.root, text="-4", fg="red", font=("Arial", 24))
        self.title_label2.pack()

        # Opponent type selection
        self.opponent_type = tk.StringVar(value="human")
        self.opponents_frame = ttk.LabelFrame(self.root, text="Select Opponent Type")
        self.opponents_frame.pack(padx=10, pady=10, fill="x", expand=True)

        self.radio_human = ttk.Radiobutton(self.opponents_frame, text="Player 2", variable=self.opponent_type,
                                           value="player2")
        self.radio_human.pack(anchor=tk.W, padx=20, pady=5)
        self.radio_monte_carlo = ttk.Radiobutton(self.opponents_frame, text="Monte Carlo AI",
                                                 variable=self.opponent_type, value="monte_carlo")
        self.radio_monte_carlo.pack(anchor=tk.W, padx=20, pady=5)
        self.radio_abp = ttk.Radiobutton(self.opponents_frame, text="Alpha-Beta Pruning AI",
                                         variable=self.opponent_type, value="ABP")
        self.radio_abp.pack(anchor=tk.W, padx=20, pady=5)

        # Start game button
        self.start_game_button = ttk.Button(self.root, text="Start New Game", command=self.start_game)
        self.start_game_button.pack(padx=10, pady=20)

        self.root.mainloop()

    def start_game(self):
        # Placeholder for starting the game
        chosen_opponent = self.opponent_type.get()
        print(f"Starting new game against {chosen_opponent}...")


if __name__ == "__main__":
    ui_manager = UIManager()
