import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk


class FirstScreen:

    def __init__(self, root: ThemedTk, saved_data):
        self.root = root
        self.saved_data = saved_data
        self.player_count = 3

    def start_screen(self):
        self.root.withdraw()

        self.first_screen = tk.Toplevel(self.root)
        self.first_screen.geometry("400x300")
        self.first_screen.title("Welcome to Catan")
        self.first_screen.iconbitmap("src/hexagon.ico")

        label = ttk.Label(
            self.first_screen, text="Welcome to Catan!", font=("Arial", 16)
        )
        label.pack(pady=20)
        self.start_button = ttk.Button(
            self.first_screen, text="Start Game", command=self.get_player_count
        )
        self.start_button.pack(pady=10)

        self.player_count_widget = ttk.Entry(self.first_screen)
        self.player_count_widget.pack(pady=10)

        self.load_game_btn = ttk.Button(
            self.first_screen, text="Load Saved Game", command=self.get_saved_game_state
        )
        self.load_game_btn.pack(pady=10)

        if self.saved_data is None:
            self.load_game_btn.config(state="disabled")

        self.root.wait_window(self.first_screen)
        self.root.deiconify()
        return self.player_count  # Default to 3 players if none selected

    def get_player_count(self) -> int:
        try:
            count = int(self.player_count_widget.get())
            if count in [3, 4]:
                self.first_screen.destroy()
                self.player_count = count
                return self.player_count
            else:
                raise ValueError
        except ValueError:
            pass
        return 3  # Default to 3 players if invalid input

    def get_saved_game_state(self) -> int:
        """Check if the user wants to load a saved game. will return -1 if so."""
        self.first_screen.destroy()
        self.player_count = -1
        return self.player_count
