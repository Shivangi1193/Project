import json
import sqlite3
import pandas as pd
from pathlib import Path

DB_NAME = "cricket.db"
JSON_FOLDER = "c:/Users/LENOVO/Downloads/guvi/crizbuzz/data"  # folder containing json files

conn = sqlite3.connect(DB_NAME)

for json_file in Path("c:/Users/LENOVO/Downloads/guvi/crizbuzz/data").glob("*.json"):
    print(f"Reading {json_file}")

    df = pd.read_json(json_file)
    table_name = json_file.stem
    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    print(f"Created table: {table_name}")

conn.commit()
conn.close()