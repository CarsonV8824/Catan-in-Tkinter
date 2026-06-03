from tkinter import ttk  
from ttkthemes import ThemedTk
import tkinter as tk

from tabs import Tabs
from canvas import Canvas
from game_struct import GameStruct
from db import Database
from game_struct import GameStruct
from game_loop import GameLoop
from player import Player
from first_screen import FirstScreen
import networkx as nx
import random
import os
from typing import Any

def load_data() -> list[Any]|None:
    db_path = os.path.join("database", "Tinkinan.db")
    if not os.path.exists(db_path):
        return None
    try:
        with Database(db_path) as db:
            data = db.get_data()
            if not data:
                return None
        return data
    except Exception as e:
        print (e)
        return None

def add_data(game_struct:GameStruct, PlayerData:list[Player], player_count:int, player_turn:int):
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

            db.add_data(node_list, edge_list, player_data, player_count, player_turn)
    except Exception as e:
        raise e

def rgb(r:int, g:int, b:int):
    return f'#{r:02x}{g:02x}{b:02x}'

def main():
    Database()
    
    root = ThemedTk(theme="breeze")
    
    root.geometry("1200x800")
    root.title("Tinkinan")

    logo_path = os.path.join("src", "hexagon.ico")  
    root.iconbitmap(logo_path)

    first_screen = FirstScreen(root, load_data())
    player_count = first_screen.start_screen()

    if player_count == -1:
        # Load saved game
        saved_data = load_data()
        
        game_struct = GameStruct()
        first_entry = saved_data[0]
        node_list = first_entry[1]
        edge_list = first_entry[2]
        PlayerData = first_entry[3]
        player_count = first_entry[4]
        player_turn = first_entry[5]
        game_struct.graph.add_nodes_from(node_list)
        game_struct.graph.add_edges_from(edge_list)

        board = Canvas(root, game_struct)

        game_loop = GameLoop(root, game_struct, board)

        players = []
        for pdata in PlayerData:
            player = Player(pdata["name"], pdata["color"])
            player.resources = pdata["resources"]
            players.append(player)
        tab = Tabs(root)

        board.draw_board_with_loaded_data(players)

        tabs = tab.tabs()

        game_loop.player_index = player_turn

        board.get_player(players[game_loop.player_index])

        dice_tab = tab.dice_tab(tabs, game_loop, players, game_struct)

        player_stats_tab = tab.player_stats_tab(tabs, players)

        tab.update_player_stats(players, game_loop, game_struct) 
        trade_tab = tab.trade_tab(tabs, players, game_loop, game_struct)

        buy_tab = tab.buy_tab(tabs, players, game_loop)
            
        rules_tab = tab.rules_tab(tabs)

        additional_info_tab = tab.additional_info_tab(tabs, load_data())
            
        running = root.mainloop()

        if not running: #this will run when the window is closed
            print("Exiting Game")

            add_data(game_struct, players, player_count, game_loop.player_index)
            
        return

    else:

        game_struct = GameStruct()
        
        board = Canvas(root, game_struct)

        game_loop = GameLoop(root, game_struct, board)

        players = []
        
        colors = ["red", "blue", "purple", "orange"]
        
        for i in range(player_count):
            
            players.append(Player(f"Player {i+1}", colors[i]))

        tab = Tabs(root)

        tabs = tab.tabs()

        game_loop.placing_initial_settlements(players, tabs=tabs)

        first_player_index  = 0

        board.get_player(players[first_player_index]) #set first player for placement

        dice_tab = tab.dice_tab(tabs, game_loop, players, game_struct)

        player_stats_tab = tab.player_stats_tab(tabs, players)

        tab.update_player_stats(players, game_loop, game_struct) 

        trade_tab = tab.trade_tab(tabs, players, game_loop, game_struct)

        buy_tab = tab.buy_tab(tabs, players, game_loop)
        
        rules_tab = tab.rules_tab(tabs)

        additional_info_tab = tab.additional_info_tab(tabs, load_data())
        
        running = root.mainloop()

        if not running: #this will run when the window is closed
            print("Exiting Game")

            add_data(game_struct, players, player_count, game_loop.player_index)

if __name__ == "__main__":
    main()