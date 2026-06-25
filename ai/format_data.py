import pandas as pd
from pathlib import Path
import sqlite3

def sql_to_csv():
    path = Path("database/Tinkinan.db")
    path = path.absolute().resolve()
    connection = sqlite3.connect(path)

    data = pd.read_sql("SELECT * FROM Catan", connection)
    data = data.dropna()
    connection.close()
    data.to_csv("ai/data.csv", index=False)

if __name__ == "__main__":
    sql_to_csv()