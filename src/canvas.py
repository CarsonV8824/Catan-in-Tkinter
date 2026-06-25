from game_struct import GameStruct
from tkinter import ttk
from ttkthemes import ThemedTk
import tkinter as tk
import math
import random

try:
    from player import Player
except (ImportError, ModuleNotFoundError):
    pass
import json
from pathlib import Path


class Canvas:

    def __init__(self, root: ThemedTk, game_struct: GameStruct):
        self.root = root
        self.game_struct = game_struct
        self.canvas = tk.Canvas(self.root, height=650, width=650)
        self.canvas.configure(bg="lightblue", border=2, relief="ridge", borderwidth=2)
        self.canvas.pack(expand=True, fill="none", side="left")
        self.hexagons = []
        self.pieces = []
        # issue with math.Need to fix
        piece_path = Path("config/piece_coords.json")
        abs_piece_path = piece_path.resolve()
        with open(abs_piece_path, "r") as f:
            data: dict = json.load(f)
            self.piece_coords = {int(k): v for k, v in data.items()}
        # look at Game_Board.png to see how the corner coords are mapped to piece numbers
        coner_path = Path("config/corner_coords.json")
        abs_corner_path = coner_path.resolve()
        with open(abs_corner_path, "r") as f:
            self.corner_coords: dict = json.load(f)
            self.corner_coords = {int(k): v for k, v in self.corner_coords.items()}

        self.__get_pieces()
        self.__draw_board()

        self.current_player: None | Player = (
            None  # to track current player for placement
        )

        self.settlement_on = False

        self.road_on = False

        self.city_on = False

        self.robber_placement_active = False

    def __get_pieces(self) -> None:
        self.pieces_ref = {
            "sheep": "lime",
            "wood": "green",
            "brick": "brown",
            "wheat": "yellow",
            "ore": "gray",
            "desert": "tan",
        }

        for i in range(4):
            self.pieces.append(self.pieces_ref["sheep"])
            self.pieces.append(self.pieces_ref["wood"])
            self.pieces.append(self.pieces_ref["wheat"])
        for i in range(3):
            self.pieces.append(self.pieces_ref["brick"])
            self.pieces.append(self.pieces_ref["ore"])
        self.pieces.append(self.pieces_ref["desert"])

    def __draw_hexagon(self, x: float, y: float, size: float, fill_color: str) -> None:
        points = []
        for i in range(6):
            angle = math.radians(60 * i - 30)
            x_i = x + size * math.cos(angle)
            y_i = y + size * math.sin(angle)
            points.append((x_i, y_i))
        flat_points = [coord for point in points for coord in point]
        self.canvas.create_polygon(
            flat_points, outline="black", fill=fill_color, width=2
        )
        self.hexagons.append(flat_points)

    def draw_robber_on_piece(self, piece_number: int) -> None:
        # Find the center of the hexagon for the given piece number
        hexagon_points = self.hexagons[piece_number - 1]
        x_coords = hexagon_points[0::2]
        y_coords = hexagon_points[1::2]
        center_x = sum(x_coords) / len(x_coords)
        center_y = sum(y_coords) / len(y_coords)

        # Draw the robber as a black circle at the center
        radius = 15
        self.canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill="black",
            tag="robber",
        )

    def undraw_robber_on_piece(self, piece_number: int) -> None:
        # Remove the robber from the canvas
        self.canvas.delete("robber")

    def draw_number_on_piece(self, piece_number: int, number: int | str) -> None:
        # Find the center of the hexagon for the given piece number
        hexagon_points = self.hexagons[piece_number - 1]
        x_coords = hexagon_points[0::2]
        y_coords = hexagon_points[1::2]
        center_x = sum(x_coords) / len(x_coords)
        center_y = sum(y_coords) / len(y_coords)

        # Draw the number at the center
        self.canvas.create_text(
            center_x, center_y, text=str(number), font=("Arial", 16), fill="black"
        )

    def __draw_board(self) -> None:

        for piece_num, cords in self.piece_coords.items():
            if self.game_struct.get_piece_resource(piece_num) is not None:
                color = self.game_struct.get_piece_resource(piece_num)

            else:
                color = self.__choose_radom_color_from_piece_list()

            self.game_struct.add_image_color_to_piece(piece_num, color)

            number = self.game_struct.get_piece_dice_number(piece_num)

            self.__draw_hexagon(cords[0], cords[1], 50, color)
            self.draw_number_on_piece(piece_num, number)

        # --- Draw Robber if already placed ---
        if not self.game_struct.is_robber_on_board():
            for i in range(1, 20):
                if self.game_struct.get_piece_resource(i) == "tan":
                    self.game_struct.place_robber_on_piece(i)
                    self.draw_robber_on_piece(i)
                    break
        else:
            # Redraw existing robber
            robber_piece = self.game_struct.get_robber_piece()
            self.draw_robber_on_piece(robber_piece)

        # Draw Ports
        selected_areas = self.game_struct.get_all_available_connections_of_ports()
        LENGTH_OF_PORT = 60
        ANGLE_ADD_CONST = 100
        angle_deg = 60

        for house, port in selected_areas:
            colors = ["lime", "brown", "gray", "green", "yellow", "norm"]
            just_col = port[
                :-1
            ].lower()  # gets everything but last element and lowercase everything
            choosen_color: str = ""
            for color in colors:
                if just_col.endswith(color):
                    choosen_color = color
                if choosen_color == "norm":
                    choosen_color = "black"

            top_facing_angles = [30, 1, 3, 4]
            right_facing_angles = [7, 8, 10, 11, 13, 14]
            bottom_facing_angles = [17, 18, 20, 21]
            left_facing_angles = [23, 24, 27, 28]

            house_number = int("".join([char for char in house if char.isdigit()]))
            start_x, start_y = self.corner_coords[house_number]

            if house_number in top_facing_angles:
                angle_deg = ANGLE_ADD_CONST
            elif house_number in right_facing_angles:
                angle_deg = ANGLE_ADD_CONST + 75
            elif house_number in bottom_facing_angles:
                angle_deg = ANGLE_ADD_CONST + ANGLE_ADD_CONST + 45
            elif house_number in left_facing_angles:
                angle_deg = ANGLE_ADD_CONST + ANGLE_ADD_CONST + ANGLE_ADD_CONST + 55
            else:
                raise ValueError(f"House with port not in lists. {house_number}")

            angle_rad = math.radians(angle_deg)

            end_x = start_x - LENGTH_OF_PORT * math.cos(angle_rad)
            end_y = start_y - LENGTH_OF_PORT * math.sin(angle_rad)

            self.canvas.create_line(
                start_x, start_y, end_x, end_y, width=5, fill=choosen_color
            )
            angle_deg = math.degrees(angle_rad)

            angle_deg *= house_number * 4

    def __choose_radom_color_from_piece_list(self) -> str:
        return self.pieces.pop(random.randint(0, len(self.pieces) - 1))

    def __point_in_polygon(self, x: float, y: float, poly: list) -> bool:
        n = len(poly) // 2
        inside = False

        p1x, p1y = poly[0], poly[1]
        for i in range(n + 1):
            p2x, p2y = poly[2 * (i % n)], poly[2 * (i % n) + 1]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def is_corner_hit(self, event, tolerance=10):
        cx, cy = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        for idx, flat_points in enumerate(self.hexagons, start=1):
            for x_i, y_i in zip(flat_points[0::2], flat_points[1::2]):
                dx, dy = cx - x_i, cy - y_i
                if (dx * dx + dy * dy) ** 0.5 <= tolerance:
                    return idx, (x_i, y_i)  # piece number, corner coords
        return None, None

    def is_edge_hit(self, event, tolerance=10):
        cx, cy = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        for idx, flat_points in enumerate(self.hexagons, start=1):
            for i in range(6):
                x1, y1 = flat_points[2 * i], flat_points[2 * i + 1]
                x2, y2 = (
                    flat_points[2 * ((i + 1) % 6)],
                    flat_points[2 * ((i + 1) % 6) + 1],
                )

                # Calculate distance from point to line segment
                A = cx - x1
                B = cy - y1
                C = x2 - x1
                D = y2 - y1

                dot = A * C + B * D
                len_sq = C * C + D * D
                param = dot / len_sq if len_sq != 0 else -1

                if param < 0:
                    xx, yy = x1, y1
                elif param > 1:
                    xx, yy = x2, y2
                else:
                    xx = x1 + param * C
                    yy = y1 + param * D

                dx = cx - xx
                dy = cy - yy
                if (dx * dx + dy * dy) ** 0.5 <= tolerance:
                    return idx, (
                        (x1, y1),
                        (x2, y2),
                    )  # piece number, edge coords of what houses inbetween
        return None, None

    def is_piece_hit(self, event):
        cx, cy = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        for idx, flat_points in enumerate(self.hexagons, start=1):
            if self.__point_in_polygon(cx, cy, flat_points):
                return idx  # piece number
        return None

    def get_corner_num(self, corner, tolerance=0.01):
        """Find corner number by coordinate with tolerance for floating-point errors"""
        for key, (x, y) in self.corner_coords.items():
            try:
                if abs(x - corner[0]) < tolerance and abs(y - corner[1]) < tolerance:
                    return key
            except TypeError as e:
                print(str(e) + " in get_corner_num")
        return None

    def draw_road(self, x1: float, y1: float, x2: float, y2: float, color: str) -> None:
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=6)

    def draw_settlement(self, x: float, y: float, color: str) -> None:
        size = 10
        points = [
            (x - size, y),
            (x, y - size),
            (x + size, y),
            (x + size, y + size),
            (x - size, y + size),
        ]
        flat_points = [coord for point in points for coord in point]
        self.canvas.create_polygon(flat_points, outline="black", fill=color, width=2)

    def draw_city(self, x: float, y: float, color: str) -> None:
        size = 12
        points = [
            (x - size, y + size),
            (x - size, y - size),
            (x + size, y - size),
            (x + size, y + size),
            (x, y + 2 * size),
        ]
        flat_points = [coord for point in points for coord in point]
        self.canvas.create_polygon(flat_points, outline="black", fill=color, width=2)

    def settlement_init(self, current_player):
        self.placement_complete = False

        def on_canvas_click(event):
            if self.placement_complete:
                return  # Ignore clicks if placement is complete

            hit_piece, corner = self.is_corner_hit(event)

            corner_num = self.get_corner_num(corner)
            if hit_piece:
                # Here you would add logic to place settlement/road

                check = self.game_struct.check_house_occupancy_empty(corner_num)
                if check:
                    x_cord = corner[0]
                    y_cord = corner[1]
                    self.draw_settlement(x_cord, y_cord, current_player.color)
                    self.game_struct.add_player_to_house(
                        corner_num, current_player.name, "House"
                    )
                    print(
                        f"{current_player.name} clicked on piece {hit_piece} at {corner}"
                    )
                    self.placement_complete = True  # Mark placement as complete

                elif not check:
                    print(f"Corner {corner_num} is already occupied.")
                    # return

            else:
                print("No corner hit")

        self.canvas.bind("<Button-1>", on_canvas_click)

        # Wait until placement is complete
        while not self.placement_complete:
            self.root.update()

    def road_init(self, current_player):
        self.placement_complete = False

        def on_canvas_click(event):
            if self.placement_complete:
                return

            hit_piece, edge_coords = self.is_edge_hit(event)

            if edge_coords is None:
                print("No edge hit")
                return

            house1_num, house2_num = edge_coords
            house1_corner_num = self.get_corner_num(house1_num)
            house2_corner_num = self.get_corner_num(house2_num)

            if hit_piece:
                print(
                    f"{current_player.name} clicked on edge {hit_piece} at {edge_coords}"
                )
                road_check = self.game_struct.check_road_occupancy(
                    house1_corner_num, house2_corner_num
                )

                # Check if player owns a settlement at either endpoint
                has_settlement_endpoint = self.game_struct.check_house_owner(
                    house1_corner_num, current_player.name
                ) or self.game_struct.check_house_owner(
                    house2_corner_num, current_player.name
                )

                if road_check and has_settlement_endpoint:
                    x1, y1 = house1_num
                    x2, y2 = house2_num
                    self.draw_road(x1, y1, x2, y2, current_player.color)
                    self.game_struct.add_player_to_road(
                        house1_corner_num, house2_corner_num, current_player.name
                    )
                    self.placement_complete = True
                else:
                    if not has_settlement_endpoint:
                        print(f"You must have a settlement at one end of this road.")

        self.canvas.bind("<Button-1>", on_canvas_click)

        while not self.placement_complete:
            self.root.update()

    def get_player(self, player):
        self.current_player = player
        print(f"Current player set to {player.name}")

    def settlement_mode(self):
        self.root.bind(
            "<s>",
            lambda e: (
                setattr(self, "settlement_on", True),
                setattr(self, "road_on", False),
                setattr(self, "city_on", False),
                print("Settlement mode activated"),
            ),
        )

    def city_mode(self):
        self.root.bind(
            "<c>",
            lambda e: (
                setattr(self, "city_on", True),
                setattr(self, "settlement_on", False),
                setattr(self, "road_on", False),
                print("City mode activated"),
            ),
        )

    def road_mode(self):
        self.root.bind(
            "<r>",
            lambda e: (
                setattr(self, "road_on", True),
                setattr(self, "settlement_on", False),
                setattr(self, "city_on", False),
                print("Road mode activated"),
            ),
        )

    def on_canvas_click_game_loop(
        self, event
    ):  # make this method make the player able to buy settlements, roads, and cities

        print(self.current_player.name + " clicked the canvas")

        hit_piece_corner, corner = self.is_corner_hit(event)
        hit_piece_edge, edge_coords = self.is_edge_hit(event)

        if hit_piece_corner:
            if self.settlement_on:

                check = self.game_struct.is_valid_house_placement(
                    self.get_corner_num(corner), self.current_player.name
                )
                if (
                    check
                    and self.current_player.resources["lime"] >= 1
                    and self.current_player.resources["brown"] >= 1
                    and self.current_player.resources["green"] >= 1
                    and self.current_player.resources["yellow"] >= 1
                ):
                    self.current_player.remove_resource("lime", 1)
                    self.current_player.remove_resource("brown", 1)
                    self.current_player.remove_resource("green", 1)
                    self.current_player.remove_resource("yellow", 1)
                    self.current_player.add_victory_point(1)
                    x_cord = corner[0]
                    y_cord = corner[1]
                    self.draw_settlement(x_cord, y_cord, self.current_player.color)
                    self.game_struct.add_player_to_house(
                        self.get_corner_num(corner), self.current_player.name, "House"
                    )
                    print(
                        f"{self.current_player.name} clicked on piece {hit_piece_corner} at {corner}"
                    )
                    self.current_player.actions.add("bought_settlement")
                elif not check:
                    print(f"Corner {self.get_corner_num(corner)} is already occupied.")

                print(
                    f"Clicked on piece {hit_piece_corner} at {corner} for settlement!"
                )
            elif self.city_on:
                check = self.game_struct.is_valid_city_placement(
                    self.get_corner_num(corner), self.current_player.name
                )
                if (
                    check
                    and self.current_player.resources["gray"] >= 3
                    and self.current_player.resources["yellow"] >= 2
                ):
                    self.current_player.remove_resource("gray", 3)
                    self.current_player.remove_resource("yellow", 2)
                    self.current_player.add_victory_point(2)
                    x_cord = corner[0]
                    y_cord = corner[1]

                    self.draw_city(x_cord, y_cord, self.current_player.color)
                    self.game_struct.change_house_to_city(
                        self.get_corner_num(corner), self.current_player.name
                    )
                    print(
                        f"{self.current_player.name} clicked on piece {hit_piece_corner} at {corner} for city!"
                    )
                    self.current_player.actions.add("bought_city")

        elif hit_piece_edge:
            if self.road_on:
                house1_num, house2_num = edge_coords
                house1_num = self.get_corner_num(house1_num)
                house2_num = self.get_corner_num(house2_num)
                check = self.game_struct.is_valid_road_placement(
                    house1_num, house2_num, self.current_player.name
                )
                if (
                    check
                    and self.current_player.resources["brown"] >= 1
                    and self.current_player.resources["green"] >= 1
                ):
                    self.current_player.remove_resource("brown", 1)
                    self.current_player.remove_resource("green", 1)
                    house1_num, house2_num = edge_coords
                    house1_corner_num = self.get_corner_num(house1_num)
                    house2_corner_num = self.get_corner_num(house2_num)
                    x1, y1 = house1_num
                    x2, y2 = house2_num
                    self.draw_road(x1, y1, x2, y2, self.current_player.color)
                    self.game_struct.add_player_to_road(
                        house1_corner_num, house2_corner_num, self.current_player.name
                    )
                    print(
                        f"{self.current_player.name} clicked on edge {hit_piece_edge} at {edge_coords}"
                    )
                elif not check:
                    print(
                        f"Edge between corners {house1_num} and {house2_num} is already occupied or invalid."
                    )
                self.current_player.actions.add("bought_road")

        else:
            print("No corner hit or edge hit")

    def place_two_roads(self, current_player):
        roads_placed = 0
        self.placement_complete = False

        def on_canvas_click(event):
            nonlocal roads_placed

            if self.placement_complete:
                return

            hit_piece, edge_coords = self.is_edge_hit(event)

            if edge_coords is None:
                print("No edge hit")
                return

            house1_num, house2_num = edge_coords
            house1_corner_num = self.get_corner_num(house1_num)
            house2_corner_num = self.get_corner_num(house2_num)

            if hit_piece:
                print(
                    f"{current_player.name} clicked on edge {hit_piece} at {edge_coords}"
                )
                road_check = self.game_struct.check_road_occupancy(
                    house1_corner_num, house2_corner_num
                )

                # Check if player owns a settlement at either endpoint OR has an adjacent road
                has_connection = (
                    self.game_struct.check_house_owner(
                        house1_corner_num, current_player.name
                    )
                    or self.game_struct.check_house_owner(
                        house2_corner_num, current_player.name
                    )
                    or self.game_struct.check_adjacent_road_owner(
                        house1_corner_num, current_player.name
                    )
                    or self.game_struct.check_adjacent_road_owner(
                        house2_corner_num, current_player.name
                    )
                )

                if road_check and has_connection:
                    x1, y1 = house1_num
                    x2, y2 = house2_num
                    self.draw_road(x1, y1, x2, y2, current_player.color)
                    self.game_struct.add_player_to_road(
                        house1_corner_num, house2_corner_num, current_player.name
                    )
                    roads_placed += 1
                    print(f"Road {roads_placed} of 2 placed")

                    if roads_placed >= 2:
                        self.placement_complete = True
                else:
                    if not has_connection:
                        print(
                            f"You must have a settlement or road connected to place this road."
                        )

        self.canvas.bind("<Button-1>", on_canvas_click)

        while not self.placement_complete:
            self.root.update()

        # Rebind to regular game loop click handler
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<Button-1>", self.on_canvas_click_game_loop)
        print("Two roads placed successfully!")

    def place_robber(self, current_player, players: list, button: ttk.Button) -> None:
        button.config(state="disabled")

        current_robber_piece = self.game_struct.get_robber_piece()
        if current_robber_piece:
            self.undraw_robber_on_piece(current_robber_piece)

        self.placement_complete = False
        self.robber_placement_active = True

        def on_canvas_click(event):
            # Early exit if placement already complete
            if self.placement_complete or not self.robber_placement_active:
                return

            hit_piece = self.is_piece_hit(event)

            if hit_piece:
                # IMMEDIATELY disable to prevent re-entry
                self.robber_placement_active = False

                self.game_struct.place_robber_on_piece(hit_piece)
                self.draw_robber_on_piece(hit_piece)

                affected_players = self.game_struct.get_players_adjacent_to_piece(
                    hit_piece
                )

                if affected_players:
                    player_selection = tk.Toplevel(self.root)
                    player_selection.title("Steal Resource")
                    player_selection.geometry("300x200")
                    player_selection.iconbitmap("src/hexagon.ico")
                    player_selection.protocol("WM_DELETE_WINDOW", lambda: None)
                    selection = tk.Label(
                        player_selection, text="Select a player to steal from:"
                    )
                    selection.pack(anchor="center", padx=10, pady=10)
                    for player in affected_players:
                        btn = ttk.Button(
                            player_selection,
                            text=player,
                            command=lambda p=player: self.steal_resource_and_close(
                                current_player, players, p, player_selection
                            ),
                        )
                        btn.pack(anchor="center", padx=5, pady=5)
                else:
                    print("No players to steal from.")
                    self.placement_complete = True

        self.canvas.bind("<Button-1>", on_canvas_click)

        while not self.placement_complete:
            self.root.update()

        # Clean up
        self.robber_placement_active = False
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<Button-1>", self.on_canvas_click_game_loop)
        button.config(state="normal")

    def steal_resource_and_close(
        self, current_player, players, target_name, window: tk.Toplevel
    ) -> None:
        player_to_steal_from = next((p for p in players if p.name == target_name), None)

        if player_to_steal_from:
            try:
                stolen_resource = player_to_steal_from.remove_random_resource()
            except ValueError:
                stolen_resource = None
            if stolen_resource:
                current_player.add_resource(stolen_resource, 1)
                print(
                    f"{current_player.name} stole {stolen_resource} from {player_to_steal_from.name}"
                )
            else:
                print(f"{player_to_steal_from.name} has no resources to steal.")

        window.destroy()
        self.placement_complete = True  # Signal loop to exit

    def draw_board_with_loaded_data(self, players: list) -> None:

        # Draw existing settlements and cities
        for node in self.game_struct.graph.nodes:
            if node.startswith("House"):
                node_data = self.game_struct.graph.nodes[node]
                owner = node_data.get("Player")
                structure_type = node_data.get("Type")

                if owner and structure_type:
                    # Extract house number from "House123" format
                    house_num = int(node.replace("House", ""))
                    x, y = self.corner_coords[house_num]

                    # Get player color
                    color = next((p.color for p in players if p.name == owner), "black")

                    if structure_type == "House":
                        self.draw_settlement(x, y, color)
                    elif structure_type == "City":
                        self.draw_city(x, y, color)

            elif node.startswith("City"):
                # Cities are renamed nodes from House nodes
                node_data = self.game_struct.graph.nodes[node]
                owner = node_data.get("Player")

                if owner:
                    # Extract house number from "City123" format
                    house_num = int(node.replace("City", ""))
                    x, y = self.corner_coords[house_num]

                    # Get player color
                    color = next((p.color for p in players if p.name == owner), "black")
                    self.draw_city(x, y, color)

        # Draw existing roads
        for edge in self.game_struct.graph.edges(data=True):
            u, v, data = edge
            owner = data.get("Player")

            # Only draw roads between House nodes (not Piece nodes)
            if owner and u.startswith("House") and v.startswith("House"):
                # Extract house numbers
                house1_num = int(u.replace("House", ""))
                house2_num = int(v.replace("House", ""))

                x1, y1 = self.corner_coords[house1_num]
                x2, y2 = self.corner_coords[house2_num]

                # Get player color
                color = next((p.color for p in players if p.name == owner), "black")
                self.draw_road(x1, y1, x2, y2, color)
