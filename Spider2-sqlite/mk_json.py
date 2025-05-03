import sqlite3
import json

def export_spider_style_schema(db_path, db_id="my_database"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]

    column_names = [[-1, "*"]]
    column_types = ["TEXT"]
    table_name_to_index = {table: idx for idx, table in enumerate(tables)}
    primary_keys = []
    foreign_keys = []

    for table_idx, table in enumerate(tables):
        cursor.execute(f"PRAGMA table_info('{table}')")
        cols = cursor.fetchall()
        for col in cols:
            col_id, col_name, col_type, notnull, default_val, pk = col
            column_names.append([table_idx, col_name])
            column_types.append(col_type.lower())
            if pk > 0:
                primary_keys.append(len(column_names) - 1)

        cursor.execute(f"PRAGMA foreign_key_list('{table}')")
        fks = cursor.fetchall()
        for fk in fks:
            # fk: (id, seq, table, from, to, on_update, on_delete, match)
            from_col = fk[3]
            to_table = fk[2]
            to_col = fk[4]

            from_idx = None
            to_idx = None
            for i, (t_idx, col_name) in enumerate(column_names):
                if t_idx == table_idx and col_name == from_col:
                    from_idx = i
                if t_idx == table_name_to_index.get(to_table) and col_name == to_col:
                    to_idx = i
            if from_idx is not None and to_idx is not None:
                foreign_keys.append([from_idx, to_idx])

    schema = {
        "db_id": db_id,
        "table_names_original": tables,
        "column_names_original": column_names,
        "column_types": column_types,
        "primary_keys": primary_keys,
        "foreign_keys": foreign_keys
    }

    conn.close()
    return schema

import os
schema_all = []
for db_id in os.listdir("test_database"):
    sqlite_path = os.path.join("test_database", db_id, db_id+".sqlite")
    if os.path.exists(sqlite_path) and not db_id.startswith("_"):
        schema_all.append(export_spider_style_schema(sqlite_path, db_id))


with open("test_tables.json", "w") as f:
    json.dump(schema_all, f, indent=4)