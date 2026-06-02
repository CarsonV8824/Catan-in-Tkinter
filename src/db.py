import sqlite3
import json
from pathlib import Path

class Database:

    def __init__(self, file="database/Tinkinan.db"):
        path = Path(file)
        abs_path = path.resolve()
        self.connection = sqlite3.connect(abs_path)
        self.cursor = self.connection.cursor()
        self.__make_table()

    def __make_table(self):
        self.cursor.execute(
        """CREATE TABLE IF NOT EXISTS Catan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        node_list TEXT,
        edge_list TEXT,
        PlayerData TEXT,
        player_count INTEGER,
        player_turn INTEGER
        );""")
        self.connection.commit()

    def add_data(self, node_list, edge_list, PlayerData, player_count, player_turn):
        """Adds game data to the database in a JSON string format."""
        
        
        
        self.cursor.execute("""
        INSERT INTO Catan (node_list, edge_list, PlayerData, player_count, player_turn)
        Values (?, ?, ?, ?, ?)

        """, (json.dumps(node_list), json.dumps(edge_list), json.dumps(PlayerData), player_count, player_turn))
        self.connection.commit()

    def get_data(self):
        """Retrieves the most recent game data from the database and returns it as a list of tuples."""
        
        self.cursor.execute("""SELECT * FROM Catan WHERE id = (SELECT MAX(id) FROM Catan)""")
        data = self.cursor.fetchall()
        return [ (row[0], json.loads(row[1]), json.loads(row[2]), json.loads(row[3]), row[4], row[5]) for row in data ]

    def clear_data(self):
        self.cursor.execute("""DELETE FROM Catan""")
        self.connection.commit()

    def __del__(self):
        self.connection.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()