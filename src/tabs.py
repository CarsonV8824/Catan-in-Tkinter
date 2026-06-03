from logging import root
from tkinter import ttk  
from ttkthemes import ThemedTk
import tkinter as tk
from player import Player
from game_loop import GameLoop
from game_struct import GameStruct

import random

from typing import Callable

class Tabs:

    def __init__(self, root:ThemedTk):
        self.root = root
        self.biuld_option = None

        self.trade_in_resources_top:tk.Toplevel = None

        self.dice_button:ttk.Button = None
        
        self.first_trade_player_text = None
        self.second_trade_player_text = None
        
        self.first_trade_player = None
        self.second_trade_player = None
        
        self.first_player_items:ttk.Treeview = None
        self.second_player_items:ttk.Treeview = None

        self.player_ports:list| None = None
        self.select_ports:ttk.Combobox | None = None

    def tabs(self):
        tab = ttk.Notebook(self.root)
        tab.pack(expand=True, fill="both")
        return tab
    
    def dice_tab(self, notebook:ttk.Notebook, game_loop: GameLoop, players:list,game_struct:GameStruct):

        dice_tab = ttk.Frame(notebook)
        notebook.add(dice_tab, text="dice")
        
        #===Scrollbar======================================================================================

        canvas = tk.Canvas(dice_tab)
        scrollbar = ttk.Scrollbar(dice_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        frame = ttk.Frame(scrollable_frame)
        frame.pack(expand=True, fill="both")

        #=====================================================================================

        self.dice_button = ttk.Button(frame, text="Roll Dice", command=lambda: game_loop.game_turn(self.dice_button, player_turn_info, players=players, first_dice_label=first_dice, second_dice_label=second_dice, total_of_dice_label=total_of_dice, update_player_stats_tab=lambda: self.update_player_stats(players, game_loop, game_struct)))

        self.dice_button.pack(pady=20)

        player_turn_info = ttk.Label(frame, text=f"{players[game_loop.player_index].name}'s Turn")
        player_turn_info.pack(pady=10)

        first_dice = ttk.Label(frame, text="First Dice Roll: ")
        first_dice.pack()

        second_dice = ttk.Label(frame, text="Second Dice Roll: ")
        second_dice.pack()

        total_of_dice = ttk.Label(frame, text="Total of Dice: ")
        total_of_dice.pack()
        
        return dice_tab
    
    def player_stats_tab(self, notebook:ttk.Notebook, players:list):
        player_stats_tab = ttk.Frame(notebook)
        notebook.add(player_stats_tab, text="player stats")
        
        #===Scrollbar======================================================================================

        canvas = tk.Canvas(player_stats_tab)
        scrollbar = ttk.Scrollbar(player_stats_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        frame = ttk.Frame(scrollable_frame)
        frame.pack(expand=True, fill="both")

        #=====================================================================================

        self.player_stat_vars = {}
        for player in players:
            player:Player = player
            player_frame = ttk.LabelFrame(frame, text=player.name, padding=10)
            player_frame.pack(fill="x", padx=10, pady=5)

            color_var = tk.StringVar(self.root, value=f"Color: {player.color}")
            ttk.Label(player_frame, textvariable=color_var).pack(anchor="w")

            stats_label = ttk.Label(player_frame, text="Stats:")
            stats_label.pack(anchor="w")

            resource_vars = {}
            for resource, amount in player.resources.items():
                res_var = tk.StringVar(self.root, value=f"  {resource}: {amount}")
                resource_vars[resource] = res_var
                ttk.Label(player_frame, textvariable=res_var).pack(anchor="w")

            self.player_stat_vars[player.name] = {"color": color_var, "resources": resource_vars}

        return player_stats_tab
    
    def update_player_stats(self, players: list, game_loop:GameLoop, game_struct:GameStruct):
        for player in players:
            player:Player = player
            vars_map = self.player_stat_vars.get(player.name)
            if not vars_map:
                continue  
            vars_map["color"].set(f"Color: {player.color}")
            for resource, amount in player.resources.items():
                res_var = vars_map["resources"].get(resource)
                if res_var:
                    res_var.set(f"  {resource}: {amount}")

        # updates the select based on player index

        self.player_ports = None
        
        self.player_ports = game_struct.get_all_available_ports_from_player(players[game_loop.player_index].name)
        print(self.player_ports)

        try:
            self.select_ports.set("")

            self.select_ports['values'] = tuple(self.player_ports)
        except AttributeError as e:
            print(f"AttributeError on line 147: {e}")
        


    def trade_tab(self, notebook:ttk.Notebook, players:list, game_loop:GameLoop, game_struct:GameStruct=None):

        trade_tab = ttk.Frame(notebook)
        notebook.add(trade_tab, text="trade")
        
        #===Scrollbar======================================================================================

        canvas = tk.Canvas(trade_tab)
        scrollbar = ttk.Scrollbar(trade_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        frame = ttk.Frame(scrollable_frame)
        frame.pack(expand=True, fill="both")

        #=====================================================================================

        player_player_frame = ttk.Frame(frame, border=2, padding=10, relief="groove")
        player_player_frame.pack(padx=10, pady=10)

        first_trade_player = ttk.Combobox(player_player_frame, values=[player.name for player in players], state="readonly")
        first_trade_player.pack(padx=10, pady=10)

        second_trade_player = ttk.Combobox(player_player_frame, values=[player.name for player in players], state="readonly")
        second_trade_player.pack(padx=10, pady=10)

        first_player = first_trade_player.get()
        second_player = second_trade_player.get()

        def on_select_first(event):
            print("Selected:", first_trade_player.get())
            self.first_trade_player = first_trade_player.get()
            
            try:
                self.first_player_items.destroy()
                self.first_trade_player_text.destroy()
            except Exception:
                pass
            
            self.first_trade_player_text = ttk.Label(player_player_frame, text=f"{self.first_trade_player}'s Resources:")
            self.first_trade_player_text.pack(padx=10, pady=10)
            self.first_player_items = ttk.Treeview(player_player_frame, selectmode="extended", show="tree")
            self.first_player_items.pack(padx=10, pady=10)
            try:
                self.first_player_items.delete(0, tk.END)
            except Exception:
                pass
            for resource, amount in next(player for player in players if player.name == self.first_trade_player).resources.items():
                for _ in range(amount):
                    if resource != "victory_points" and resource != "knight_cards":
                        
                        try:
                            self.first_player_items.insert('', 'end', text=resource)
                        except Exception as e:
                            print(e)
            
            item_count = len(self.first_player_items.get_children())
            self.first_player_items.config(height=item_count if item_count > 0 else 1)
        first_trade_player.bind("<<ComboboxSelected>>", on_select_first)

        def on_select_second(event):
            print("Selected:", second_trade_player.get())
            self.second_trade_player = second_trade_player.get()
            try:
                self.second_player_items.destroy()
                self.second_trade_player_text.destroy()
            except Exception:
                pass
            self.second_trade_player_text = ttk.Label(player_player_frame, text=f"{self.second_trade_player}'s Resources:")
            self.second_trade_player_text.pack(padx=10, pady=10)
            self.second_player_items = ttk.Treeview(player_player_frame, selectmode="extended", show="tree")
            self.second_player_items.pack(padx=10, pady=10)
            try:
                self.second_player_items.delete(0, tk.END)
            except Exception:
                pass
            for resource, amount in next(player for player in players if player.name == self.second_trade_player).resources.items():
                for _ in range(amount):
                    if resource != "victory_points" and resource != "knight_cards":
                        try:
                            self.second_player_items.insert('', 'end', text=resource)
                        except Exception as e:
                            print(e)
            self.second_player_items.config(height=len(self.second_player_items.get_children()) if len(self.second_player_items.get_children()) > 0 else 1)
        
        second_trade_player.bind("<<ComboboxSelected>>", on_select_second)

        def get_trade_selections():
            if not self.first_trade_player or not self.second_trade_player:
                return

            first_selected = list(self.first_player_items.selection())  
            second_selected = list(self.second_player_items.selection()) 
            
            first_items = []
            second_items = []
            
            # Get details from selections
            for item_id in first_selected:
                item_data = self.first_player_items.item(item_id)
                first_items.append(item_data['text'])
            
            for item_id in second_selected:
                item_data = self.second_player_items.item(item_id)
                second_items.append(item_data['text'])
            
            # Update player resources
            for player in players:
                if player.name == self.first_trade_player:
                    for resource in first_items:
                        player.remove_resource(resource, 1)
                    for resource in second_items:
                        player.add_resource(resource, 1)
                elif player.name == self.second_trade_player:
                    for resource in second_items:
                        player.remove_resource(resource, 1)
                    for resource in first_items:
                        player.add_resource(resource, 1)
            
            # Delete items AFTER updating all player resources
            for item_id in first_selected:
                self.first_player_items.delete(item_id)
            
            for item_id in second_selected:
                self.second_player_items.delete(item_id)
            
            # Add new items for trades received
            for resource in second_items:
                self.first_player_items.insert('', 'end', text=resource)
            
            for resource in first_items:
                self.second_player_items.insert('', 'end', text=resource)
            
            # Update heights
            self.first_player_items.config(height=len(self.first_player_items.get_children()) or 1)
            self.second_player_items.config(height=len(self.second_player_items.get_children()) or 1)

        trade_confirm_button = ttk.Button(
            player_player_frame, 
            text="Confirm Trade", 
            command=lambda: get_trade_selections()
        )
        trade_confirm_button.pack(pady=10)

        #===Trade in cards part==================================================================================================

        trade_in_frame = ttk.Frame(frame, padding=10, border=2, relief="groove")
        trade_in_frame.pack(padx=10, pady=10)

        trade_in_label = ttk.Label(trade_in_frame, text="Trade in 4 of the same resource for 1 of your choice")
        trade_in_label.pack(pady=5)

        trade_in_button = ttk.Button(trade_in_frame, text="Trade In Resources", command=lambda: self.trade_in_resources(players, game_loop, game_struct))
        trade_in_button.pack(pady=5)

        # Ports Part

        ports_frame = ttk.Frame(frame,padding=10,border=2, relief="groove")
        ports_frame.pack(padx=10, pady=10)

        self.player_ports = game_struct.get_all_available_ports_from_player(players[game_loop.player_index].name)
        print(self.player_ports)

        self.select_ports = ttk.Combobox(ports_frame, values=self.player_ports, state="readonly")
        self.select_ports.pack(pady=5)

        self.trade_in_port_btn = ttk.Button(ports_frame, command=lambda:confirm_trade(players[game_loop.player_index], game_loop=game_loop, game_struct=game_struct), text="Trade to Port")
        self.trade_in_port_btn.pack(pady=5)

        def trade_in(player:Player, resorce_box:ttk.Combobox, type_of_port:str, resorce_to_trade_in_for_box:ttk.Combobox):
            resorce = resorce_box.get()
            resorce_to_trade_in_for = resorce_to_trade_in_for_box.get()

            if not resorce or not resorce_to_trade_in_for:
                print("Missing selection")
                return

            type_of_port = type_of_port.lower()

            # Normal 3:1 port
            if type_of_port == "norm":
                if player.get_resource_count(resorce) >= 3:
                    player.remove_resource(resorce, 3)
                    player.add_resource(resorce_to_trade_in_for, 1)
                    return
                print("Not enough resources")
                return

            # 2:1 ports
            if player.get_resource_count(type_of_port) >= 2:
                player.remove_resource(type_of_port, 2)
                player.add_resource(resorce_to_trade_in_for, 1)
            else:
                print("Not enough resources")

        def confirm_trade(player:Player, game_loop:GameLoop, game_struct:GameStruct):

            port_type = self.select_ports.get()
            not_last_port_type = port_type[:-1]

            port_toplevel = tk.Toplevel(self.root)

            ttk.Label(port_toplevel, text="Resource you want").pack()
            wanting_combo = ttk.Combobox(
                port_toplevel,
                values=["lime", "green", "yellow", "gray", "brown"],
                state="readonly"
            )
            wanting_combo.pack()

            def make_trade(port_name, combo_widget):
                trade_in(
                    player=player,
                    resorce_box=combo_widget,
                    type_of_port=port_name,
                    resorce_to_trade_in_for_box=wanting_combo
                )
                port_toplevel.destroy()
                self.update_player_stats(players, game_loop, game_struct)

            match not_last_port_type:

                case "PortNorm":
                    ttk.Label(port_toplevel, text="Trade 3 of the same card for any card!").pack()

                    combo = ttk.Combobox(
                        port_toplevel,
                        values=["lime", "green", "yellow", "gray", "brown"],
                        state="readonly"
                    )
                    combo.pack()

                    ttk.Button(
                        port_toplevel,
                        text="Confirm Trade",
                        command=lambda: make_trade("norm", combo)
                    ).pack()

                case "PortGreen":
                    ttk.Label(port_toplevel, text="Trade 2 Green cards for any card!").pack()

                    combo = ttk.Combobox(port_toplevel, values=["green"], state="readonly")
                    combo.pack()

                    ttk.Button(
                        port_toplevel,
                        text="Confirm Trade",
                        command=lambda: make_trade("green", combo)
                    ).pack()

                case "PortYellow":
                    ttk.Label(port_toplevel, text="Trade 2 Yellow cards for any card!").pack()

                    combo = ttk.Combobox(port_toplevel, values=["yellow"], state="readonly")
                    combo.pack()

                    ttk.Button(
                        port_toplevel,
                        text="Confirm Trade",
                        command=lambda: make_trade("yellow", combo)
                    ).pack()

                case "PortBrown":
                    ttk.Label(port_toplevel, text="Trade 2 Brown cards for any card!").pack()

                    combo = ttk.Combobox(port_toplevel, values=["brown"], state="readonly")
                    combo.pack()

                    ttk.Button(
                        port_toplevel,
                        text="Confirm Trade",
                        command=lambda: make_trade("brown", combo)
                    ).pack()

                case "PortLime":
                    ttk.Label(port_toplevel, text="Trade 2 Lime cards for any card!").pack()

                    combo = ttk.Combobox(port_toplevel, values=["lime"], state="readonly")
                    combo.pack()

                    ttk.Button(
                        port_toplevel,
                        text="Confirm Trade",
                        command=lambda: make_trade("lime", combo)
                    ).pack()

        return trade_tab

    def trade_in_resources(self, players:list[Player], game_loop:GameLoop, game_struct:GameStruct|None=None):
            self.trade_in_resources_top = tk.Toplevel(self.root)
            self.trade_in_resources_top.title("Trade In Resources")
            self.trade_in_resources_top.geometry("300x300")
            self.trade_in_resources_top.iconbitmap("src/hexagon.ico")
    
            trade_in_text = ttk.Label(self.trade_in_resources_top, text=f"Select 4 resources to trade in")
            trade_in_text.pack(pady=10)

            trade_in_text.config(text=f"Select 4 resources to trade in {players[game_loop.player_index].name}")
            
            choose_texture_box_from_you = ttk.Label(self.trade_in_resources_top, text="Choose resource to give:")
            choose_texture_box_from_you.pack(pady=10)

            choose_resource_box_from_you = ttk.Combobox(self.trade_in_resources_top, values=["lime", "green", "brown", "yellow", "gray"], state="readonly")
            choose_resource_box_from_you.pack(pady=10)

            choose_texture_box_from_bank = ttk.Label(self.trade_in_resources_top, text="Choose resource to receive:")
            choose_texture_box_from_bank.pack(pady=10)

            choose_resource_box_from_bank = ttk.Combobox(self.trade_in_resources_top, values=["lime", "green", "brown", "yellow", "gray"], state="readonly")
            choose_resource_box_from_bank.pack(pady=10)

            def confirm_trade_in():
                chosen_resource_you = choose_resource_box_from_you.get()
                chosen_resource_bank = choose_resource_box_from_bank.get()
                if not chosen_resource_you or not chosen_resource_bank:
                    return
                
                if players[game_loop.player_index].get_resource_count(chosen_resource_you) < 4:
                    trade_in_text.config(text=f"Not enough {chosen_resource_you} to trade in.")
                    return
                
                players[game_loop.player_index].remove_resource(chosen_resource_you, 4)
                players[game_loop.player_index].add_resource(chosen_resource_bank, 1)

                self.trade_in_resources_top.destroy()
                self.update_player_stats(players, game_loop=game_loop, game_struct=game_struct)
            confirm_trade_in_button = ttk.Button(self.trade_in_resources_top, text="Confirm Trade In", command=confirm_trade_in)
            confirm_trade_in_button.pack(pady=10)
    
    def buy_tab(self, notebook:ttk.Notebook, players:list, game_loop:GameLoop, game_struct:GameStruct):
        
        buy_tab = ttk.Frame(notebook)
        notebook.add(buy_tab, text="buy")
        
        #===Scrollbar======================================================================================

        canvas = tk.Canvas(buy_tab)
        scrollbar = ttk.Scrollbar(buy_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        frame = ttk.Frame(scrollable_frame, border=2, padding=10, relief="groove")
        frame.pack(expand=True, fill="both")

        #=====================================================================================

        road_label = ttk.Label(frame, text="Press r to build road")
        road_label.pack(padx=10, pady=10)

        settlement_label = ttk.Label(frame, text="Press s to build settlement")
        settlement_label.pack(padx=10, pady=10)

        city_label = ttk.Label(frame, text="Press c to build city")
        city_label.pack(padx=10, pady=10)

        draw_card_label = ttk.Label(frame, text="Draw Development Card")
        draw_card_label.pack(padx=10, pady=10)

        draw_card_button = ttk.Button(frame, text="Draw Card", command=lambda: self.choose_development_card(players, game_loop.player_index, lambda players, button: game_loop.place_robber(players, button), lambda players, button: game_loop.place_two_roads(players, button), game_loop=game_loop, game_struct=game_struct))
        draw_card_button.pack(padx=10, pady=10)

        self.card_result_label = ttk.Label(frame, text="Card Result: ")
        self.card_result_label.pack(padx=10, pady=10)

        return buy_tab
    
    def choose_development_card(self, players, current_player_index:int, robber_func:Callable|None=None, road_func:Callable|None=None, game_loop:GameLoop|None=None, game_struct:GameStruct|None=None):
        if players[current_player_index].resources["lime"] < 1 and players[current_player_index].resources["gray"] < 1 and players[current_player_index].resources["yellow"] < 1:
            self.card_result_label.config(text="Not enough resources to buy a development card.")
            return
        
        current_player = players[current_player_index]
        if current_player.resources["lime"] >= 1:
            current_player.remove_resource("lime", 1)
        elif current_player.resources["gray"] >= 1:
            current_player.remove_resource("gray", 1)
        elif current_player.resources["yellow"] >= 1:
            current_player.remove_resource("yellow", 1)
        
        probablities = {}
        probablities["Knight"] = range(1,15)
        probablities["Victory Point"] = range(15,19)
        probablities["Road Building"] = range(19,22)
        probablities["Year of Plenty"] = range(22,24)
        probablities["Monopoly"] = range(24,26)
        
        roll = random.randint(1,25) #test
        chosen_card = None
        for card, rng in probablities.items():
            if roll in rng:
                chosen_card = card
                break
        self.card_result_label.config(text=f"Card Result: {chosen_card}")
        match chosen_card:
            case "Knight":
                if robber_func:
                    robber_func(players, self.dice_button)
                    players[current_player_index].add_resource("knight_cards", 1)
                    self.update_player_stats(players, game_loop=game_loop, game_struct=game_struct)
            case "Victory Point":
                players[current_player_index].add_victory_point(1)
                self.update_player_stats(players, game_loop=game_loop, game_struct=game_struct)
            case "Road Building":
                if road_func:
                    road_func(players, self.dice_button)
                    self.update_player_stats(players, game_loop=game_loop, game_struct=game_struct)
            case "Year of Plenty":
                year_of_plenty_top = tk.Toplevel(self.root)
                year_of_plenty_top.title("Year of Plenty")
                year_of_plenty_top.geometry("300x200")
                ttk.Label(year_of_plenty_top, text="You may choose 2 resources of your choice").pack(pady=10)
                year_of_plenty_top.iconbitmap("src/hexagon.ico")
                
                resources = ["lime", "green", "brown", "yellow", "gray"]
                count_holder = [0]  # Use list to avoid closure issues
                
                def add_resource(resource):
                    count_holder[0] += 1
                    players[current_player_index].add_resource(resource, 1)
                    if count_holder[0] >= 2:
                        count_holder[0] = 0
                        year_of_plenty_top.destroy()
                        self.update_player_stats(players, game_loop=game_loop, game_struct=game_struct)
                
                for r in resources:
                    btn = ttk.Button(year_of_plenty_top, text=f"Add {r}", 
                                    command=lambda res=r: add_resource(res))
                    btn.pack(pady=5)
            case "Monopoly":
                monolopy_top = tk.Toplevel(self.root)
                monolopy_top.title("Monopoly")
                monolopy_top.geometry("300x200")
                ttk.Label(monolopy_top, text="Choose a resource to monopolize:").pack(pady=10)
                monolopy_top.iconbitmap("src/hexagon.ico")
                
                def monopolize_resource(resource):
                    for i, player in enumerate(players):
                        if i != current_player_index:
                            amount = player.get_resource_count(resource)
                            if amount > 0:
                                player.remove_resource(resource, amount)
                                players[current_player_index].add_resource(resource, amount)
                    monolopy_top.destroy()
                    self.update_player_stats(players, game_loop=game_loop, game_struct=game_struct)
                resources = ["lime", "green", "brown", "yellow", "gray"]
                for r in resources:
                    btn = ttk.Button(monolopy_top, text=f"Choose {r}", 
                                    command=lambda res=r: monopolize_resource(res))
                    btn.pack(pady=5)
                
                
                self.update_player_stats(players, game_loop=game_loop, game_struct=game_struct)

        print(f"Chosen Card: {chosen_card}")
        self.update_player_stats(players, game_loop=game_loop, game_struct=game_struct)
    
    def rules_tab(self, notebook:ttk.Notebook):
        
        rules_tab = ttk.Frame(notebook)
        notebook.add(rules_tab, text="rules")
        
        #===Scrollbar======================================================================================

        canvas = tk.Canvas(rules_tab)
        scrollbar = ttk.Scrollbar(rules_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        frame = ttk.Frame(scrollable_frame)
        frame.pack(expand=True, fill="both")

        #=====================================================================================

        def show_rules():
            rules_toplevel = tk.Toplevel(rules_tab)
            rules_toplevel.title("Game Rules")
            rules_toplevel.geometry("600x400")
            rules_toplevel.iconbitmap("src/hexagon.ico")
            
            frame = ttk.Frame(rules_toplevel)
            frame.pack(expand=True, fill="both", padx=10, pady=10)
            
           
            scrollbar = ttk.Scrollbar(frame, orient="vertical")
            scrollbar.pack(side="right", fill="y")
            
            
            rules_text = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set)
            rules_text.pack(side="left", expand=True, fill="both")
            
            
            scrollbar.config(command=rules_text.yview)
            
            with open("config/rules.txt", "r") as file:
                rules_content = file.read()
            rules_text.insert("1.0", rules_content)
            rules_text.config(state="disabled")
            
        rule_button  = ttk.Button(frame, text="Show Rules", command=show_rules)
        rule_button.pack(pady=10)

        return rules_tab
    
    def additional_info_tab(self, notebook:ttk.Notebook, past_data:list[tuple]):
        past_games_tab = ttk.Frame(notebook)
        notebook.add(past_games_tab, text="additional info")
        
        #===Scrollbar======================================================================================

        canvas = tk.Canvas(past_games_tab)
        scrollbar_y = ttk.Scrollbar(past_games_tab, orient="vertical", command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(past_games_tab, orient="horizontal", command=canvas.xview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(xscrollcommand=scrollbar_x.set)
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x.pack(side="bottom", fill="x")  
        scrollbar_y.pack(side="right", fill="y")    
        canvas.pack(side="left", fill="both", expand=True)  
        
        frame = ttk.Frame(scrollable_frame)
        frame.pack(expand=True, fill="both")

        #=====================================================================================

        
            
        return past_games_tab


