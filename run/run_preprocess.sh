db_root_directory=Spider2-sqlite #root directory
dev_json=sqlite.json
dev_table=test_tables.json
dev_database=test_database
fewshot_llm=gpt-4o-rag-research
bert_model=BAAI/bge-large-en-v1.5

python -u src/database_process/data_preprocess.py \
    --db_root_directory "${db_root_directory}" \
    --dev_json "${dev_json}" \
    --dev_table "${dev_table}" \

python -u src/database_process/make_emb.py \
    --db_root_directory "${db_root_directory}" \
    --dev_database "${dev_database}" \
    --bert_model "${bert_model}"
