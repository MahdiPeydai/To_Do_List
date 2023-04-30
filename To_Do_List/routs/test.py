import json
with open('../To_Do_List/To_Do_List/data/users_information.json', 'r') as f:
    g = json.load(f)
print(g)
