import json
riven_name=[]
riven_list=json.load(open("static/WM物品表.json", "r", encoding="utf-8"))
for name in riven_list['payload']['items']:
    riven_name.append(name['item_name'])

#把riven_name保存为json
with open('static/tradable_parts_name.json', 'w', encoding='utf-8') as f:
    json.dump(riven_name, f, ensure_ascii=False)

