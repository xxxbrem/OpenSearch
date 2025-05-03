import json
with open("spider2-lite.jsonl") as f:
    data = [json.loads(i) for i in f]

sqlite = []
for i in data:
    if i["instance_id"].startswith("local"):
        # print(i["instance_id"])
        sqlite.append({"question_id": i["instance_id"], "db_id": i["db"], "question": i["question"]})

with open("sqlite.json", "w") as f:
    json.dump(sqlite, f) 