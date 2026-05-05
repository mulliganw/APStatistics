import pandas
import requests

json = requests.get("https://overfast-api.tekrop.fr/players/TBB-11125/stats?gamemode=quickplay").json()
rank_json = requests.get("https://overfast-api.tekrop.fr/players/TBB-11125/summary").json()
results_dict = {}
stat_dict = {}
column_list = []

try:
    stat_dict["Tank"] = [f"{rank_json["competitive"]["pc"]["tank"]["division"]} {rank_json["competitive"]["pc"]["tank"]["tier"]}" for x in range(0,46)]
except: 
    stat_dict["Tank"] = [None for x in range(0,46)]
try: 
    stat_dict["Damage"] = [f"{rank_json["competitive"]["pc"]["damage"]["division"]} {rank_json["competitive"]["pc"]["damage"]["tier"]}" for x in range(0,46)]
except: 
    stat_dict["Damage"] = [None for x in range(0,46)]
try:
    stat_dict["Support"] = [f"{rank_json["competitive"]["pc"]["support"]["division"]} {rank_json["competitive"]["pc"]["support"]["tier"]}" for x in range(0,46)]
except:
    stat_dict["Support"] = [None for x in range(0,46)]
try:
    stat_dict["Open"] = [f"{rank_json["competitive"]["pc"]["open"]["division"]} {rank_json["competitive"]["pc"]["open"]["tier"]}" for x in range(0,46)]
except: 
    stat_dict["Open"] = [None for x in range(0,46)]

for key in json.keys() :
    for i in range(0, len(json[key])) :
        for stat in json[key][i]["stats"] :
            stat_dict[stat["label"]] = [None for x in json.keys()]

for index, key in enumerate(json.keys()) :
    column_list.append(key)
    for i in range(0, len(json[key])) :
        games_won_count = 0
        for stat in json[key][i]["stats"] :
            row_name = stat["label"]
            value = stat["value"]
            if row_name == "Games Won" :
                games_won_count += 1                
            if games_won_count <= 1 or row_name != "Games Won":
                stat_dict[row_name][index] = value

df = pandas.DataFrame.from_dict(stat_dict, orient='index', columns=column_list)
df.to_csv("TestDataframe.csv")
