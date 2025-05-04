import os
import json

result_path = "results/dev/generate_db_schema+extract_col_value+extract_query_noun+column_retrieve_and_other_info/Spider2-sqlite/2025-05-03-19-46-07"
sqlite_pth = "Spider2-sqlite/sqlite.json"

with open(sqlite_pth) as f:
    data = json.load(f)

new_prompt_dict_list = []
for example in os.listdir(result_path):
    if "_" in example:
        for ori in data:
            question_id = int(example.split("_")[0])
            if ori['question_id'] == question_id:
                
                with open(os.path.join(result_path, example)) as f:
                    ex_json_all = json.load(f)
                ex_json = ex_json_all[-1]

                column = ex_json["column"]
                foreign_keys= ex_json["foreign_keys"]
                L_values = ex_json["L_values"]
                q_order = ex_json["q_order"]

                ori["question_id"] = question_id
                columns = column.split("\n")
                ori["L_values"] = L_values
                ori["column"] = column
                ori["q_order"] = q_order

with open("sqlite_sl_result.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

with open("sqlite_sl_result.json", encoding="utf-8") as f:
    json.load(f)