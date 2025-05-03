"""
Generate questions for LLMs and save it as a task
"""
import argparse
import os,re
import sys
import json
from pathlib import Path
import pandas as pd
import logging
from tqdm import tqdm
# 设置基本配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_question_section(text):
    # Use regex to find the content starting from /* Answer the following: and ending at the newline
    matches = re.findall(r'/\* Answer the following:(.*?)\*/', text,re.DOTALL)
    return [match.strip(' */') for match in matches]  
    
def generate_questions_and_estimates(db_root_directory, DAIL_SQL):
    dev_json = os.path.join(db_root_directory, 'data_preprocess', 'dev.json')   
    dailsql_json = DAIL_SQL

    # Load JSON data
    with open(dailsql_json, 'r') as f:
        dailsql_content = json.load(f)
    with open(dev_json, 'r') as f:
        dev_infos = json.load(f)

    # Prompt headers
    prompt_head = '/* Some SQL examples are provided based on similar problems: */'
    extract_head = "/* Some extract examples are provided based on similar problems: */"

    questions = []
    extracts = []

    for query_info, dev_info in tqdm(zip(dailsql_content['questions'], dev_infos), total=len(dev_infos), desc="Processing"):
        # Directly use existing prompt from DAIL_SQL
        dail_prompt = query_info['prompt']
        # Prepare entries
        new_entry = {
            "question": dev_info['question'],
            "evidence": "",
            "raw_question": dev_info['question'],
            "prompt": dail_prompt,
            "n_examples": query_info['n_examples'],
            "db_id": query_info['db_id']
        }
        # Extract entry uses same prompt but cuts to max 6 examples if possible
        # Here, we assume prompt contains multiple '/* Answer the following:'
        split_prompt = dail_prompt.split("/* Answer the following:")
        if len(split_prompt) > 7:
            # Keep only first 6 few-shot + 1 question
            head = split_prompt[0]
            body = split_prompt[1:7]
            rest = split_prompt[-1]
            trimmed_prompt = head + ''.join([f'/* Answer the following:{x}' for x in body]) + f'/* Answer the following:{rest}'
        else:
            trimmed_prompt = dail_prompt

        ext_entry = {
            "question": dev_info['question'],
            "evidence": "",
            "raw_question": dev_info['question'],
            "prompt": trimmed_prompt.replace(prompt_head, extract_head, 1),
            "n_examples": 6,
            "db_id": query_info['db_id']
        }

        questions.append(new_entry)
        extracts.append(ext_entry)

    # Save result
    task = {
        "args": {},
        "costs": dailsql_content.get('costs', []),
        "questions": questions,
        "extract": extracts
    }

    generate_path = Path(db_root_directory) / "fewshot"
    generate_path.mkdir(exist_ok=True)

    with open(os.path.join(generate_path, "questions.json"), "w") as f:
        json.dump(task, f, indent=4)

    print(f"✅ Saved to {generate_path / 'questions.json'}")
# def generate_questions_and_estimates(db_root_directory, DAIL_SQL):
#     fewshot_parse_json=Path(db_root_directory,'llm_train_parse.json')
#     dev_json = os.path.join(args.db_root_directory, 'data_preprocess', 'dev.json')   
#     dailsql_json=DAIL_SQL
#     prompt_head='/* Some SQL examples are provided based on similar problems: */'
#     extract_head="/* Some extract examples are provided based on similar problems: */"
#     question_head='/* Answer the following: '

#     # Load JSON data into DataFrames
#     with open(dailsql_json,'r') as f:
#         dailsql_content=json.load(f)
#     fewshot_parse_content=pd.read_json(fewshot_parse_json)
#     with open(dev_json,'r') as f:
#         dev_infos=json.load(f)

#     # Extract similar questions from the DAIL SQL DataFrame
#     all_questions = dailsql_content['questions']

#     # Initialize a new variable to accumulate new fewshot entries
#     questions = []
#     extracts = []
#     # Iterate over the rows of the fewshot_parse DataFrame
#     for query_info,dev_info in tqdm(zip(all_questions,dev_infos), total=len(all_questions), desc="Processing Queries"):
#         new_fewshot = ''
#         ext_fewshot=''
#         cnt=0
#         similar_questions=extract_question_section(query_info['prompt'])
#         # print(similar_questions)
#         # break
#         try:
#             for q in similar_questions[:-1]:
#                 q_trian=fewshot_parse_content[fewshot_parse_content["question"]==q]
#                 # print(q_trian)
#                 cnt+=1
#                 parse_section =q_trian['parse'].iloc[0]
#                 ext_section=q_trian['extract'].iloc[0]
#                 new_fewshot += f'\n{question_head}{q_trian["question"].iloc[0]} */\n{parse_section}\n'
#                 if cnt<=6:
#                     ext_fewshot +=f'\n{question_head}{q_trian["question"].iloc[0]} */\n{ext_section}\n'
#         except Exception as e:
#             print(e,q,q_trian)
#         # print(new_fewshot)
#         # break
#         new_fewshot=prompt_head+new_fewshot[:-1]
#         ext_fewshot=extract_head+ext_fewshot[:-1]
#         new_entry = {
#                 "question": dev_info['question'],
#                 "evidence": "",
#                 "raw_question": dev_info['question'],
#                 'prompt':new_fewshot,
#                 # "response": query_info['response'],
#                 "n_examples": query_info['n_examples'],
#                 "db_id": query_info['db_id']
#                 }
#         ext_entry = {
#                 "question": dev_info['question'],
#                 "evidence": "",
#                 "raw_question": dev_info['question'],
#                 'prompt':ext_fewshot,
#                 # "response": query_info['response'],
#                 "n_examples": 6,
#                 "db_id": query_info['db_id']
#                 }

#         questions.append(new_entry)
#         extracts.append(ext_entry)

#     # Save questions and estimates
#     task = {
#         "args": vars(args),
#         "costs": dailsql_content['costs'],
#         "questions": questions,
#         "extract": extracts
#     }
#     generate_path = Path(args.db_root_directory) / "fewshot"

#     # if generate_path.exists():
#     #     os.system(f"rm -r {generate_path}")

#     generate_path.mkdir(exist_ok=True)

#     with open(os.path.join(generate_path,"questions.json"), "w") as f:
#         json.dump(task, f, indent=4)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate New Fewshot")
    parser.add_argument('--db_root_directory', type=str, help='Root directory for the database')
    parser.add_argument('--DAIL_SQL', type=str, help='Path to the DAIL SQL JSON file')

    # Parse the arguments
    args = parser.parse_args()

    logging.info(f"Start generate_fewshot_step_2,the output_file is {args.db_root_directory}/fewshot")
    generate_questions_and_estimates(args.db_root_directory, args.DAIL_SQL)