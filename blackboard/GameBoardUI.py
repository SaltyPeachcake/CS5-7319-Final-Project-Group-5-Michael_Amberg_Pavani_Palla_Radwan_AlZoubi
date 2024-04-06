import tkinter as tk
import Blackboard


class GameBoardUI:
    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.root = tk.Tk()
        self.root.title("Connect 4")
        self.create_board_ui()
        self.create_control_ui()
        self.update_turn_label()

    def create_board_ui(self):
        self.canvas = tk.Canvas(self.root, width=560, height=480, bg='blue')
        self.canvas.grid(row=0, column=0, padx=20, pady=20, rowspan=2)  # rowspan=2 to allow control UI to align at the top
        self.canvas.bind("<Button-1>", self.on_board_click)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")  # Clear the canvas before redrawing
        for row in range(6):
            for col in range(7):
                x0 = col * 80 + 10
                y0 = row * 80 + 10
                x1 = col * 80 + 70
                y1 = row * 80 + 70
                color = "white"
                if self.blackboard.board[row][col] == 1:
                    color = "yellow"
                elif self.blackboard.board[row][col] == 2:
                    color = "red"
                self.canvas.create_oval(x0, y0, x1, y1, fill=color, outline="blue")

    def on_board_click(self, event):
        column = event.x // 80
        # Placeholder for making a move
        self.update_game_state()

    def create_control_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=0, column=1, sticky='n', padx=20)

        self.start_new_game_button = tk.Button(control_frame, text="Start New Game", command=self.start_new_game)
        self.start_new_game_button.pack(pady=10)

        self.restart_button = tk.Button(control_frame, text="Restart Game", command=self.restart_game)
        self.restart_button.pack(pady=10)

        self.turn_label = tk.Label(self.root, text="", font=('Arial', 16))
        self.turn_label.grid(row=1, column=0)

    def update_turn_label(self):
        turn_text = f"Player {self.blackboard.current_player}'s Turn"
        self.turn_label.config(text=turn_text)

    def start_new_game(self):
        self.blackboard.board = [[0 for _ in range(7)] for _ in range(6)]

    def restart_game(self):
        self.blackboard.board = [[0 for _ in range(7)] for _ in range(6)]  # You can call start_new_game for restarting, since it resets the state as well

    def update_game_state(self):
        self.draw_board()
        self.update_turn_label()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ui_manager = GameBoardUI(Blackboard.Blackboard())
    ui_manager.run()
