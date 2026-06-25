from tkinter import ttk
from ttkthemes import ThemedTk
import tkinter as tk
import random
from game_struct import GameStruct
from canvas import Canvas
from typing import Callable
import os
import json

from db import Database


def add_data(
    game_struct: GameStruct,
    PlayerData: list,
    player_count: int,
    player_turn: int,
    dice1:int,
    dice2:int,
    action:str
):
    db_path = os.path.join("database", "Tinkinan.db")
    if not os.path.exists(db_path):
        return None
    try:
        with Database(db_path) as db:
            node_list = list(game_struct.graph.nodes(data=True))
            edge_list = list(game_struct.graph.edges(data=True))

            player_data = []
            for player in PlayerData:
                pdata = {
                    "name": player.name,
                    "color": player.color,
                    "resources": player.resources,
                }
                player_data.append(pdata)

            db.add_data(node_list, edge_list, player_data, player_count, player_turn, action, dice1, dice2)
    except Exception as e:
        raise e


class GameLoop:

    def __init__(self, root: tk.Tk, game_struct: GameStruct, board: Canvas):

        self.root = root
        self.game_struct = game_struct
        self.board: Canvas = board
        self.first_dice = None
        self.second_dice = None
        self.total_of_dice = None

        self.player_index = 0

    """TODO: Make the players choose where to place their initial settlements and roads. 
        Try to keep canvas methods out of game struct class.
        hide tabs untill initial placement is done."""

    def placing_initial_settlements(self, players: list, tabs: ttk.Notebook = None):

        tabs.pack_forget()  # Hide tabs during initial placementl

        total_initial_placements = len(players) * 2
        current_placement = 0
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        while current_placement < total_initial_placements:
            current_player = players[self.player_index]

            self.board.canvas.update()
            self.board.settlement_init(current_player)
            self.board.road_init(current_player)
            current_placement += 1
            self.player_index = (self.player_index + 1) % len(players)

        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        tabs.pack(expand=True, fill="both")  # Show tabs after placement is done

        self.board.canvas.bind(
            "<Button-1>", self.board.on_canvas_click_game_loop
        )  # Re-bind the main game click handler

        self.board.city_mode()  # bind city mode after initial placement

        self.board.road_mode()  # bind road mode after initial placement

        self.board.settlement_mode()  # bind settlement mode after initial placement

    def place_robber(self, players: list, button: ttk.Button):
        self.board.place_robber(
            players[self.player_index],
            players,
            button,
        )

    def place_two_roads(self, players: list, button: ttk.Button):
        button.config(state="disabled")
        self.board.place_two_roads(players[self.player_index])
        button.config(state="normal")

    def game_turn(
        self,
        button: ttk.Button,
        player_info: ttk.Label,
        players: list,
        first_dice_label: ttk.Label = None,
        second_dice_label: ttk.Label = None,
        total_of_dice_label: ttk.Label = None,
        update_player_stats_tab=None,
    ):

        drestory_all = lambda: [
            widget.destroy()
            for widget in self.root.winfo_children()
            if isinstance(widget, tk.Toplevel)
        ]
        drestory_all()

        longest_name, longest_len = self.game_struct.get_player_with_longest_route()
        longest_player = next((p for p in players if p.name == longest_name), None)
        if longest_player and longest_len >= 5:
            current_holder = next(
                (p for p in players if p.resources.get("has_longest_route")), None
            )
            if current_holder != longest_player:
                if current_holder:
                    current_holder.resources["longest_route"] = False
                    current_holder.remove_victory_point(2)
                    if update_player_stats_tab:
                        update_player_stats_tab()
                longest_player.resources["longest_route"] = True
                longest_player.add_victory_point(2)
                if update_player_stats_tab:
                    update_player_stats_tab()

        biggest_army_player = max(players, key=lambda p: p.resources["knight_cards"])
        if biggest_army_player.resources["knight_cards"] >= 3:
            current_holder = next(
                (p for p in players if p.resources.get("largest_army")), None
            )
            if current_holder != biggest_army_player:
                if current_holder:
                    current_holder.resources["largest_army"] = False
                    current_holder.remove_victory_point(2)
                    if update_player_stats_tab:
                        update_player_stats_tab()
                biggest_army_player.resources["largest_army"] = True
                biggest_army_player.add_victory_point(2)
                if update_player_stats_tab:
                    update_player_stats_tab()

        self.board.canvas.update()
        first_die = random.randint(1, 6)
        second_die = random.randint(1, 6)
        first_dice_label.config(text=f"First Dice Roll: {first_die}")
        second_dice_label.config(text=f"Second Dice Roll: {second_die}")
        total = first_die + second_die
        total_of_dice_label.config(text=f"Total of Dice: {total}")

        if total != 7:
            self.game_struct.distribute_resources(total, players)
        elif total == 7:
            # Check which players need to discard
            players[self.player_index].actions.add("placed_robber")
            players_to_discard = []
            for player in players:
                total_resources = sum(
                    [
                        count
                        for resource, count in player.resources.items()
                        if resource != "victory_points" and resource != "knight_cards"
                    ]
                )
                if total_resources > 7:
                    players_to_discard.append(player)

            # If players need to discard, show discard UI
            if players_to_discard:
                button.config(state="disabled")
                self.show_discard_ui(players_to_discard, update_player_stats_tab)
                button.config(state="normal")

            self.place_robber(players, button)

        self.board.canvas.update()

        self.player_index = (self.player_index + 1) % len(players)

        # Update UI after resources are distributed and is now next turn for player's stuff
        if update_player_stats_tab:
            update_player_stats_tab()

        player_info.config(text=f"{players[self.player_index].name}'s Turn")

        self.board.get_player(players[self.player_index])

        self.board.canvas.update()
        players[self.player_index].actions.add("rolled_dice")
        actions = list(players[self.player_index].actions)
        actions = json.dumps(actions)
        add_data(self.game_struct, players, len(players), self.player_index, first_die, second_die, actions) 
        print("added data to datavbase")

    def show_discard_ui(self, players_to_discard: list, update_player_stats_tab=None):
        """Display UI for players to manually discard half their resources."""
        for player in players_to_discard:
            total_resources = sum(
                [
                    count
                    for resource, count in player.resources.items()
                    if resource != "victory_points" and resource != "knight_cards"
                ]
            )
            to_discard = total_resources // 2

            discard_window = tk.Toplevel(self.root)
            discard_window.title(f"Discard Resources - {player.name}")
            discard_window.geometry("400x400")
            discard_window.iconbitmap("src/hexagon.ico")
            discard_window.resizable(False, False)

            discard_window.protocol("WM_DELETE_WINDOW", lambda: None)

            ttk.Label(
                discard_window,
                text=f"{player.name}, you must discard {to_discard} resources",
                font=("Arial", 12),
            ).pack(pady=10)

            resources = ["lime", "green", "brown", "yellow", "gray"]
            discard_counts = {res: tk.IntVar(value=0) for res in resources}

            # Display spinboxes for each resource
            for resource in resources:
                available = player.resources.get(resource, 0)
                frame = ttk.Frame(discard_window)
                frame.pack(pady=5)

                ttk.Label(
                    frame, text=f"{resource.capitalize()} (have {available}):"
                ).pack(side="left", padx=5)
                spinbox = ttk.Spinbox(
                    frame,
                    from_=0,
                    to=available,
                    textvariable=discard_counts[resource],
                    width=5,
                )
                spinbox.pack(side="left", padx=5)

            # Capture variables with default parameters
            def confirm_discard(
                p=player,
                res=resources,
                to_d=to_discard,
                counts=discard_counts,
                window=discard_window,
            ):
                total_selected = sum([counts[r].get() for r in res])
                if total_selected != to_d:
                    ttk.Label(
                        window,
                        text=f"Error: You must discard exactly {to_d} resources",
                        foreground="red",
                    ).pack()
                    return

                # Remove resources from player
                try:
                    for resource in res:
                        amount = counts[resource].get()
                        if amount > 0:
                            p.remove_resource(resource, amount)
                except Exception as e:
                    ttk.Label(window, text=f"Error: {str(e)}", foreground="red").pack()
                    return

                # Update UI and close window
                if update_player_stats_tab:
                    update_player_stats_tab()
                window.destroy()

            ttk.Button(
                discard_window, text="Confirm Discard", command=confirm_discard
            ).pack(pady=10)

            # Wait for this player to discard before moving to next
            self.root.wait_window(discard_window)
            player.actions.add("discard_due_to_robber")
