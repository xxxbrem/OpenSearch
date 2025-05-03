import json
with open("spider2-lite.jsonl") as f:
    data = [json.loads(i) for i in f]
dic = []
count = 0
for i in data:
    if i["instance_id"].startswith("local"):
        dic.append({"question_id": count, "instance_id": i["instance_id"], "db_id": i["db"], "question": i["question"]})
        count += 1

with open("sqlite.json", "w") as f:
    json.dump(dic, f, indent=4)