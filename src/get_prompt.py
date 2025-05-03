import os
import json
from pipeline.utils import make_newprompt
fewshot_path = "Bird/fewshot/questions.json"
result_path = "results/dev/generate_db_schema+extract_col_value+extract_query_noun+column_retrieve_and_other_info/Bird/2025-04-22-20-34-38"
question_path = "Bird/dev/dev.json"
with open(fewshot_path) as f:## fewshot
    df_fewshot = json.load(f)

with open(question_path) as f:## fewshot
    question_json = json.load(f)

new_prompt_O="""{fewshot}

/* Database schema */
{db_info}
{key_col_des}

# Based on the database schema and the examples above, pay attention to the following:
1. For parts involving division that contain integer types, CAST them to REAL.
2. "#Values in Database" display part values from the database. Please ignore the unnecessary values.
```

/* Answer the following: {question} */
{q_order}"""

new_prompt_dict_list = []
for example in os.listdir(result_path):
    if "_" in example:
        new_prompt_dict = {}
        question_id = int(example.split("_")[0])
        with open(os.path.join(result_path, example)) as f:
            ex_json_all = json.load(f)
        ex_json = ex_json_all[-1]
        # print(ex_json.keys())
        column = ex_json["column"]
        foreign_keys= ex_json["foreign_keys"]
        L_values = ex_json["L_values"]
        # if not L_values:
        #     os.remove(os.path.join(result_path, example))
        #     continue
        q_order = ex_json["q_order"]
        values = [f"{x[0]}: '{x[1]}'" for x in L_values]
        db="_".join(example.replace(".json", "").split("_")[1:])
        assert db == question_json[question_id]["db_id"], db

        key_col_des = "#Values in Database:\n" + '\n'.join(values)
        # key_col_des = ""

        new_db_info = f"Database Management System: SQLite\n#Database name: {db} \n{column}\n\n#Forigen keys:\n{foreign_keys}\n"
        # new_db_info=get_last_node_result(execution_history, "generate_db_schema")["db_list"]

        # question=rewrite_question(task.question)
        question=question_json[question_id]["question"]
        fewshot=df_fewshot["questions"][question_id]['prompt']
        # fewshot=""
        # fewshot=fewshot.split("\n/* Given the following database schema: */")[0]
        new_prompt = make_newprompt(new_prompt_O, fewshot,
                                key_col_des, new_db_info, question,
                                question_json[question_id]["evidence"],q_order)
        new_prompt_dict["question_id"] = question_id
        # new_prompt_dict["prompt"] = new_prompt


        columns = column.split("\n")
        # new_prompt_dict["sl_columns"] = [x[:x.find(":")] for x in columns]
        new_prompt_dict["L_values"] = L_values
        new_prompt_dict["column"] = column
        new_prompt_dict["db_cols"] = list(ex_json_all[0]["db_col_dic"].keys())
        new_prompt_dict_list.append(new_prompt_dict)

with open("new_prompt.jsonl", "w") as f:
    for row in new_prompt_dict_list:
        f.write(json.dumps(row)+"\n")