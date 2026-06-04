import networkx as nx
#from collections import deque
import random

import player

class GameStruct:

    def __init__(self):
        
        self.graph = nx.Graph()
        
        self.dice_numbers = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]
        #self.dice_numbers = deque(self.dice_numbers)
        #self.dice_numbers.rotate(random.randint(-len(self.dice_numbers), len(self.dice_numbers)))
        #self.dice_numbers = list(self.dice_numbers)

        #---adds all of the places where a person can place a house or road. Use reference photo (Game_Board.png)---
        
        for i in range(1, 55):
            self.graph.add_node(f"House{i}", Player=None, Type=None)
            if 1 < i < 30:
                self.graph.add_edge(f"House{i-1}", f"House{i}", Player=None)
            elif i == 30:
                self.graph.add_edge(f"House{i-1}", f"House{i}", Player=None)
                self.graph.add_edge("House1", f"House{i}", Player=None)
            elif 31 < i < 48:
                self.graph.add_edge(f"House{i-1}", f"House{i}", Player=None)
            elif i == 48:
                self.graph.add_edge(f"House{i}", "House31", Player=None)
                self.graph.add_edge(f"House{i}", f"House{i-1}", Player=None)
            elif 49 < i < 54:
                self.graph.add_edge(f"House{i-1}", f"House{i}", Player=None)
            if i == 54:
                self.graph.add_edge(f"House{i-1}", f"House{i}", Player=None)
                self.graph.add_edge(f"House{i}", "House49", Player=None)
        
        #---connect the rest of the houses---

        self.graph.add_edge("House2", "House31", Player=None)
        self.graph.add_edge("House4", "House33", Player=None)
        self.graph.add_edge("House7", "House34", Player=None)
        self.graph.add_edge("House9", "House36", Player=None)
        self.graph.add_edge("House12", "House37", Player=None)
        self.graph.add_edge("House14", "House39", Player=None)
        self.graph.add_edge("House17", "House40", Player=None)
        self.graph.add_edge("House19", "House42", Player=None)
        self.graph.add_edge("House22", "House43", Player=None)
        self.graph.add_edge("House24", "House45", Player=None)
        self.graph.add_edge("House27", "House46", Player=None)
        self.graph.add_edge("House29", "House48", Player=None)

        self.graph.add_edge("House49", "House32", Player=None)
        self.graph.add_edge("House50", "House35", Player=None)
        self.graph.add_edge("House51", "House38", Player=None)
        self.graph.add_edge("House52", "House41", Player=None)
        self.graph.add_edge("House53", "House44", Player=None)
        self.graph.add_edge("House54", "House47", Player=None)

        #---tile pieces themselves---

        for i in range(1, 20):

            self.graph.add_node(f"Piece{i}", Resource=None, dice_number=None, Robber=False)
        
        #---piece 1---

        self.graph.add_edge("House1", "Piece1")
        self.graph.add_edge("House2", "Piece1")
        self.graph.add_edge("House31", "Piece1")
        self.graph.add_edge("House48", "Piece1")
        self.graph.add_edge("House29", "Piece1")
        self.graph.add_edge("House30", "Piece1")

        #---piece 2---

        self.graph.add_edge("House2", "Piece2")
        self.graph.add_edge("House3", "Piece2")
        self.graph.add_edge("House4", "Piece2")
        self.graph.add_edge("House33", "Piece2")
        self.graph.add_edge("House32", "Piece2")
        self.graph.add_edge("House31", "Piece2")
        
        #---piece 3---

        self.graph.add_edge("House4", "Piece3")
        self.graph.add_edge("House5", "Piece3")
        self.graph.add_edge("House6", "Piece3")
        self.graph.add_edge("House7", "Piece3")
        self.graph.add_edge("House33", "Piece3")
        self.graph.add_edge("House34", "Piece3")

        #---piece 4---

        self.graph.add_edge("House7", "Piece4")
        self.graph.add_edge("House8", "Piece4")
        self.graph.add_edge("House9", "Piece4")
        self.graph.add_edge("House34", "Piece4")
        self.graph.add_edge("House35", "Piece4")
        self.graph.add_edge("House36", "Piece4")
        #---piece 5---

        self.graph.add_edge("House9", "Piece5")
        self.graph.add_edge("House10", "Piece5")
        self.graph.add_edge("House11", "Piece5")
        self.graph.add_edge("House12", "Piece5")
        self.graph.add_edge("House36", "Piece5")
        self.graph.add_edge("House37", "Piece5")

        #--piece 6---

        self.graph.add_edge("House12", "Piece6")
        self.graph.add_edge("House13", "Piece6")
        self.graph.add_edge("House14", "Piece6")
        self.graph.add_edge("House37", "Piece6")
        self.graph.add_edge("House38", "Piece6")
        self.graph.add_edge("House39", "Piece6")

        #---piece 7---

        self.graph.add_edge("House14", "Piece7")
        self.graph.add_edge("House15", "Piece7")
        self.graph.add_edge("House16", "Piece7")
        self.graph.add_edge("House17", "Piece7")
        self.graph.add_edge("House39", "Piece7")
        self.graph.add_edge("House40", "Piece7")

        #---piece 8---

        self.graph.add_edge("House17", "Piece8")
        self.graph.add_edge("House18", "Piece8")
        self.graph.add_edge("House19", "Piece8")
        self.graph.add_edge("House40", "Piece8")
        self.graph.add_edge("House41", "Piece8")
        self.graph.add_edge("House42", "Piece8")
        
        #---piece 9---

        self.graph.add_edge("House19", "Piece9")
        self.graph.add_edge("House20", "Piece9")
        self.graph.add_edge("House21", "Piece9")
        self.graph.add_edge("House22", "Piece9")
        self.graph.add_edge("House42", "Piece9")
        self.graph.add_edge("House43", "Piece9")

        #--piece 10---

        self.graph.add_edge("House22", "Piece10")
        self.graph.add_edge("House23", "Piece10")
        self.graph.add_edge("House24", "Piece10")
        self.graph.add_edge("House43", "Piece10")
        self.graph.add_edge("House44", "Piece10")
        self.graph.add_edge("House45", "Piece10")

        #--piece 11---

        self.graph.add_edge("House24", "Piece11")
        self.graph.add_edge("House25", "Piece11")
        self.graph.add_edge("House26", "Piece11")
        self.graph.add_edge("House27", "Piece11")
        self.graph.add_edge("House45", "Piece11")
        self.graph.add_edge("House46", "Piece11")
        #---piece 12---

        self.graph.add_edge("House27", "Piece12")
        self.graph.add_edge("House28", "Piece12")
        self.graph.add_edge("House29", "Piece12")
        self.graph.add_edge("House46", "Piece12")
        self.graph.add_edge("House47", "Piece12")
        self.graph.add_edge("House48", "Piece12")
        
        #---piece 13---

        self.graph.add_edge("House31", "Piece13")
        self.graph.add_edge("House32", "Piece13")
        self.graph.add_edge("House47", "Piece13")
        self.graph.add_edge("House48", "Piece13")
        self.graph.add_edge("House49", "Piece13")
        self.graph.add_edge("House54", "Piece13")

        #---piece 14---

        self.graph.add_edge("House32", "Piece14")
        self.graph.add_edge("House33", "Piece14")
        self.graph.add_edge("House34", "Piece14")
        self.graph.add_edge("House35", "Piece14")
        self.graph.add_edge("House49", "Piece14")
        self.graph.add_edge("House50", "Piece14")
        #---piece 15---

        self.graph.add_edge("House35", "Piece15")
        self.graph.add_edge("House36", "Piece15")
        self.graph.add_edge("House37", "Piece15")
        self.graph.add_edge("House38", "Piece15")
        self.graph.add_edge("House50", "Piece15")
        self.graph.add_edge("House51", "Piece15")

        #---piece 16---

        self.graph.add_edge("House38", "Piece16")
        self.graph.add_edge("House39", "Piece16")
        self.graph.add_edge("House40", "Piece16")
        self.graph.add_edge("House41", "Piece16")
        self.graph.add_edge("House51", "Piece16")
        self.graph.add_edge("House52", "Piece16")
        

        #---piece 17---

        self.graph.add_edge("House41", "Piece17")
        self.graph.add_edge("House42", "Piece17")
        self.graph.add_edge("House43", "Piece17")
        self.graph.add_edge("House44", "Piece17")
        self.graph.add_edge("House52", "Piece17")
        self.graph.add_edge("House53", "Piece17")

        #---piece 18---

        self.graph.add_edge("House44", "Piece18")
        self.graph.add_edge("House45", "Piece18")
        self.graph.add_edge("House46", "Piece18")
        self.graph.add_edge("House47", "Piece18")
        self.graph.add_edge("House53", "Piece18")
        self.graph.add_edge("House54", "Piece18")
        
        #---piece 19---

        self.graph.add_edge("House49", "Piece19")
        self.graph.add_edge("House50", "Piece19")
        self.graph.add_edge("House51", "Piece19")
        self.graph.add_edge("House52", "Piece19")
        self.graph.add_edge("House53", "Piece19")
        self.graph.add_edge("House54", "Piece19")

        # Normal Port 1 on House30 and House1 to PortNorm1

        self.graph.add_node("PortNorm1")
        self.graph.add_edges_from([("House30", "PortNorm1"), ("House1", "PortNorm1")])

        # Yellow Port 1 on House3 and House4

        self.graph.add_node("PortYellow1")
        self.graph.add_edges_from([("House3", "PortYellow1"), ("House4", "PortYellow1")])

        # Gray Port 1 on House7 and House8

        self.graph.add_node("PortGray1")
        self.graph.add_edges_from([("House7", "PortGray1"), ("House8", "PortGray1")])

        # Normal Port 2 on House10 and House11

        self.graph.add_node("PortNorm2")
        self.graph.add_edges_from([("House10", "PortNorm2"), ("House11", "PortNorm2")])

        # Sheep Port 1 on House13 and House14

        self.graph.add_node("PortLime1")
        self.graph.add_edges_from([("House13", "PortLime1"), ("House14", "PortLime1")])

        # Normal Port 3 on House 17 and House 18

        self.graph.add_node("PortNorm3")
        self.graph.add_edges_from([("House17", "PortNorm3"), ("House18", "PortNorm3")])

        # Normal Port 4 on House 20 and House 21

        self.graph.add_node("PortNorm4")
        self.graph.add_edges_from([("House20", "PortNorm4"), ("House21", "PortNorm4")])

        # Brick Port 1 on House 23 and House 24

        self.graph.add_node("PortBrown1")
        self.graph.add_edges_from([("House23", "PortBrown1"), ("House24", "PortBrown1")])

        # Wood Port 1 on House 27 and House 28

        self.graph.add_node("PortGreen1")
        self.graph.add_edges_from([("House27", "PortGreen1"), ("House28", "PortGreen1")])

        
    def add_image_color_to_piece(self, piece_number, resource_type):
        node_name = f"Piece{piece_number}"

        self.graph.nodes[node_name]['Resource'] = resource_type

        if resource_type == "tan" or resource_type == "desert":
            dice_number = ""
            self.graph.nodes[node_name]['dice_number'] = dice_number
        else:
            try:
                choosen_number = self.dice_numbers.pop(0)
            except Exception as e:
                print(e)
            dice_number = choosen_number
            self.graph.nodes[node_name]['dice_number'] = dice_number

        print(f"Added {self.graph.nodes[node_name]['Resource']} with dice number {self.graph.nodes[node_name]['dice_number']}")

    def get_piece_resource(self, piece_number):
        node = f"Piece{piece_number}"
        
        return self.graph.nodes[node]['Resource']

    def get_piece_dice_number(self, piece_number):
        node = f"Piece{piece_number}"
        
        return self.graph.nodes[node]['dice_number']

    def distribute_resources(self, dice_roll, players: list):
        
        pieces:list[str] = list(self.graph.nodes)
        for piece in pieces:
            if piece.startswith("Piece"):
                piece_data = self.graph.nodes[piece]
                # Convert dice_number to int for comparison, skip if empty string
                dice_number = piece_data['dice_number']
                if dice_number and piece_data['Robber'] != True and int(dice_number) == dice_roll:
                    connected_houses = [n for n in self.graph.neighbors(piece) if n.startswith("House")]
                    connected_cities = [c for c in self.graph.neighbors(piece) if c.startswith("City")]
                    for house in connected_houses:
                        house_data = self.graph.nodes[house]
                        owner = house_data['Player']
                        if owner:
                            resource = piece_data['Resource']
                            for p in players:
                                if p.name == owner:
                                    p.add_resource(resource, 1)
                                    print(f"{p.name} received 1 {resource} from {piece} due to dice roll {dice_roll}.")
                    for city in connected_cities:
                        city_data = self.graph.nodes[city]
                        owner = city_data['Player']
                        if owner:
                            resource = piece_data['Resource']
                            for p in players:
                                if p.name == owner:
                                    p.add_resource(resource, 2)
                                    print(f"{p.name} received 2 {resource} from {piece} due to dice roll {dice_roll}.")
    
    def check_house_owner(self, house_number: int, player_name: str) -> bool:
        """Returns True if the specified player owns a settlement at this house"""
        try:
            node_name = f"House{house_number}"
            return self.graph.nodes[node_name]['Player'] == player_name 
        except KeyError:
            node_name = f"City{house_number}"
            return self.graph.nodes[node_name]['Player'] == player_name 
    
    def check_house_occupancy_empty(self, house_number:int) -> bool:
        """Returns True if the house is unoccupied"""
        node_name = f"House{house_number}"
        return self.graph.nodes[node_name]['Player'] is None
    
    def check_road_occupancy(self, house_number_1:int, house_number_2:int) -> bool:
        node_1 = f"House{house_number_1}"
        node_2 = f"House{house_number_2}"
        if self.graph.has_edge(node_1, node_2):
            return self.graph.edges[node_1, node_2]['Player'] is None
        else:
            print(f"No edge exists between {node_1} and {node_2}.")
            return False
        
    def is_valid_road_placement(self, house_number_1: int, house_number_2: int, player_name: str) -> bool:
        """
        Returns True if the player can legally place a road between these two houses.
        A road is valid if:
        1. The road is unoccupied
        2. At least one endpoint has a settlement or connected road owned by the player
        """
        # First check if the road is empty
        if not self.check_road_occupancy(house_number_1, house_number_2):
            return False
        
        # Check if player owns a settlement at either endpoint
        if self.check_house_owner(house_number_1, player_name) or self.check_house_owner(house_number_2, player_name):
            return True
        
        # Check if player has a road connected to either endpoint
        node_1 = f"House{house_number_1}"
        node_2 = f"House{house_number_2}"
        
        # Check all neighbors of house_number_1 for player's roads
        for neighbor in self.graph.neighbors(node_1):
            if neighbor.startswith("House"):
                if self.graph.has_edge(node_1, neighbor):
                    if self.graph.edges[node_1, neighbor].get('Player') == player_name:
                        return True
        
        # Check all neighbors of house_number_2 for player's roads
        for neighbor in self.graph.neighbors(node_2):
            if neighbor.startswith("House"):
                if self.graph.has_edge(node_2, neighbor):
                    if self.graph.edges[node_2, neighbor].get('Player') == player_name:
                        return True
        
        return False
    
    def is_valid_house_placement(self, house_number: int, player_name: str) -> bool:
        """
        Returns True if the player can legally place a settlement at this house.
        A house placement is valid if:
        1. The house is unoccupied
        2. At least one adjacent road is owned by the player (or it's the initial placement phase)
        3. No settlement exists on any adjacent house (distance rule)
        """
        # First check if the house is empty
        if not self.check_house_occupancy_empty(house_number):
            return False
        
        node_name = f"House{house_number}"
        
        # Check all adjacent houses - they must be unoccupied (settlement distance rule)
        for neighbor in self.graph.neighbors(node_name):
            if neighbor.startswith("House"):
                if self.graph.nodes[neighbor]['Player'] is not None:
                    print(f"House {house_number} is too close to an existing settlement at {neighbor}.")
                    return False
        
        # Check if player owns at least one adjacent road
        for neighbor in self.graph.neighbors(node_name):
            if neighbor.startswith("House"):
                if self.graph.has_edge(node_name, neighbor):
                    if self.graph.edges[node_name, neighbor].get('Player') == player_name:
                        return True
        
        # If no adjacent road found, return False (settlement must connect to a road)
        print(f"No adjacent road owned by {player_name} at house {house_number}.")
        return False
    
    def is_valid_city_placement(self, house_number:int, player_name:str) -> bool:
        """
        Returns True if the player can legally upgrade a settlement to a city at this house.
        A city placement is valid if:
        1. The player owns a settlement at this house
        """
        return self.check_house_owner(house_number, player_name)

    def change_house_to_city(self, house_number:int, player_name:str):
        node_name = f"House{house_number}"
        if self.graph.nodes[node_name]['Player'] == player_name:
            # Change the node to represent a city
            self.graph.nodes[node_name]['Type'] = "City"
            mapping = {node_name: f"City{house_number}"}
            self.graph = nx.relabel_nodes(self.graph, mapping)
            print(f"Upgraded settlement to city for player {player_name} at {node_name}")
        else:
            print(f"Cannot upgrade to city: {player_name} does not own settlement at {node_name}")

    def add_player_to_house(self, house_number:int, player_name:str, structure_type:str):
        node_name = f"House{house_number}"
        if self.graph.nodes[node_name]['Player'] is not None:
            print(f"House {house_number} is already occupied by {self.graph.nodes[node_name]['Player']}.")
            
        else:
            self.graph.nodes[node_name]['Player'] = player_name
            self.graph.nodes[node_name]['Type'] = structure_type
            print(f"Added {structure_type} for player {player_name} at {node_name}")

    def add_player_to_road(self, house_number_1, house_number_2, player_name):
        node_1 = f"House{house_number_1}"
        node_2 = f"House{house_number_2}"
        if self.graph.has_edge(node_1, node_2):
            self.graph.edges[node_1, node_2]['Player'] = player_name
            print(f"Added road for player {player_name} between {node_1} and {node_2}")
        else:
            print(f"No edge exists between {node_1} and {node_2} to add a road.")

    def clear_robber_off_board(self):
        pieces:list[str] = list(self.graph.nodes)
        for piece in pieces:
            if piece.startswith("Piece"):
                piece_data = self.graph.nodes[piece]
                if piece_data['Robber']:
                    piece_data['Robber'] = False
                    print(f"Robber removed from {piece}")

    def place_robber_on_piece(self, piece_number:int):
        self.clear_robber_off_board()
        node_name = f"Piece{piece_number}"
        self.graph.nodes[node_name]['Robber'] = True
        print(f"Robber placed on {node_name}")

    def get_piece_color(self, piece_number:int) -> str:
        node_name = f"Piece{piece_number}"
        return self.graph.nodes[node_name]['Resource']
    
    def get_players_adjacent_to_piece(self, piece_number:int) -> list[str]:
        node_name = f"Piece{piece_number}"
        adjacent_houses = [n for n in self.graph.neighbors(node_name) if n.startswith("House")]
        players = set()
        for house in adjacent_houses:
            house_data = self.graph.nodes[house]
            owner = house_data['Player']
            if owner:
                players.add(owner)
        return list(players)
    
    def get_robber_piece(self) -> int | None:
        pieces:list[str] = list(self.graph.nodes)
        for piece in pieces:
            if piece.startswith("Piece"):
                piece_data = self.graph.nodes[piece]
                if piece_data['Robber'] == True:
                    return int(piece.replace("Piece", ""))
        return None  # Indicates robber not found

    def is_robber_on_board(self) -> bool:
        pieces:list[str] = list(self.graph.nodes)
        for piece in pieces:
            if piece.startswith("Piece"):
                piece_data = self.graph.nodes[piece]
                if piece_data['Robber'] == True:
                    return True
                
        return False
        
    def check_adjacent_road_owner(self, house_number:int, player_name:str) -> bool:
        """Returns True if the specified player owns a road adjacent to this house"""
        node_name = f"House{house_number}"
        for neighbor in self.graph.neighbors(node_name):
            if neighbor.startswith("House"):
                if self.graph.has_edge(node_name, neighbor):
                    if self.graph.edges[node_name, neighbor].get('Player') == player_name:
                        return True
        return False

    def get_player_with_longest_route(self) -> tuple[str, int] | None:
        
        max_length = 0
        longest_player = None
        players = set()
        
        # Gather all players who have roads on the board
        edges = list(self.graph.edges(data=True))
        for edge in edges:
            player = edge[2].get('Player')
            if player:
                players.add(player)
        
        # For each player, find the longest path of their roads
        for player in players:
            player_edges = [(u, v) for u, v, data in edges if data.get('Player') == player]
            player_graph = nx.Graph()
            player_graph.add_edges_from(player_edges)
            
            # Find the longest path in the player's road graph
            for node in player_graph.nodes():
                lengths = nx.single_source_dijkstra_path_length(player_graph, node)
                longest_from_node = max(lengths.values(), default=0)
                if longest_from_node > max_length:
                    max_length = longest_from_node
                    longest_player = player
        
        return longest_player, max_length
    
    def get_all_available_ports_from_player(self, player_name: str) -> list:
        """Returns all available ports near houses owned by the player."""
        ports = set()

        for node, data in self.graph.nodes(data=True):
            if data.get("Player") == player_name:
                for neighbor in self.graph.neighbors(node):
                    if str(neighbor).startswith("Port"):
                        ports.add(neighbor)

        return list(ports)
    
    def get_all_available_connections_of_ports(self) -> list[tuple[str,str]]:
        """Returns all Nodes that are connected to a port. Sorted By the Port. Like (House, Port)"""

        temp = set()

        for node, _ in self.graph.nodes(data=True):
            for neighbor in self.graph.neighbors(node):
                if str(neighbor).startswith("Port"):
                    temp.add((node, str(neighbor)))


        port_index = 1
        return sorted(list(temp), key = lambda x: x[port_index])
        

    def __str__(self):
        return f"nodes: {len(list(self.graph.nodes))}. number of edges {len(list(self.graph.edges))}"

if __name__ == "__main__":
    game = GameStruct()
    game.add_image_color_to_piece(1, "wood")
    #print(game)