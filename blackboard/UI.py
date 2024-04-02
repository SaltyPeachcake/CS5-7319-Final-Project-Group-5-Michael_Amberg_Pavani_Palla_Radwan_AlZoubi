import tkinter as tk
from tkinter import ttk

def start_new_game():
    print("Starting a new game...")
    draw_board()  # Redraw the board for a new game

def restart_game():
    print("Restarting the game...")
    draw_board()  # Redraw the board to restart the game

def draw_board():
    board_canvas.delete("all")  # Clear the canvas before redrawing
    for row in range(6):
        for col in range(7):
            board_canvas.create_oval(
                col * 80 + 10, row * 80 + 10, col * 80 + 70, row * 80 + 70,
                fill='white', outline='blue'
            )

# Initialize the main window
root = tk.Tk()
root.title("Connect 4 Game")
root.geometry("800x700")  # Adjust the size as needed to fit the screen

# Canvas for the Connect 4 board, adjust dimensions to fit
board_canvas = tk.Canvas(root, width=7*80, height=6*80, bg='blue')
board_canvas.grid(row=0, column=0, padx=20, pady=20)

draw_board()  # Initial draw of the board

# Label to display whose turn it is
turn_label = tk.Label(root, text="Player 1's Turn", font=('Arial', 16), fg='black')
turn_label.grid(row=1, column=0)

# Frame for the menu
menu_frame = tk.Frame(root, bg='light grey')
menu_frame.grid(row=0, column=1, rowspan=2, padx=20, pady=20, sticky='n')

# Buttons for starting a new game or restarting the current game
start_button = tk.Button(menu_frame, text="Start New Game", command=start_new_game)
start_button.pack(pady=10)

restart_button = tk.Button(menu_frame, text="Restart Game", command=restart_game)
restart_button.pack(pady=10)

root.mainloop()
