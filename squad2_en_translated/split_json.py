import json

dev_dict = {
    "version": "v2.0",
    "data": []
}

train_dict = {
    "version": "v2.0",
    "data": []
}

with open("squad2_en_translated/squad2_en_translated.json", "r") as in_file:
    squad_fi = json.loads(in_file.read())
    count = 0
    for line in squad_fi["data"]:
        if count < 442:
            train_dict["data"].append(line)
        if count >= 442:
            dev_dict["data"].append(line)
        count += 1

with open("squad2_en_translated/dev-v2.0.json", "w") as dev_file:
    json.dump(dev_dict, dev_file)
 
with open("squad2_en_translated/train-v2.0.json", "w") as train_file:
    json.dump(train_dict, train_file)
              
