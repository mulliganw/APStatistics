import pandas, requests

all_players = ["WANTED-22351", "GoodBoyZak-2715", "RhinoThunder-11647", "Majestic-22728", "popsimoke-2753", "goop-11970", "Jojoba-11695", "MrXd-1422", "KiWi-23601", "edamame-31488", "delune-21239", "Sulyvaint-2327", "Mariarchi23-2792", "Fami-21157", "MVP-13667", "MonkeyDLuffy-22733", "evilbronbron-1771", "GRiNNZi-1940", "bingo-11130", "lvolve-2785", "Duhti52-2819", "Youseff-21470", "Gamez-11845", "Ariancool-2630", "ROMZiLLA-21954", "License2chil-1626", "NUTZFROMBERK-1121", "YEAHRIGHT-21548", "SPEED-22410", "Ethanfun11-1602", "MISTER-31729", "PlzSanWichME-3722", "kizu-21247", "Zow-11392", "bataocanbo-1919", "Zycko-21516", "Swiss-11457", "Mew-22202", "GPP-11863", "peyon-1117", "Vieira-12142", "Deji-21825", "Turo-11702", "Pocky-11824", "Spy-21749", "Aquil3on-2806", "Endmaker-21432", "Viikinki-21909", "lambchops-11620", "iMazt-1712"]

def exportPlayerStats(username) :
    try:
        json = requests.get(f"https://overfast-api.tekrop.fr/players/{username}/stats?gamemode=quickplay").json()
        rank_json = requests.get(f"https://overfast-api.tekrop.fr/players/{username}/summary").json()
    except: 
        print("404 not found")
        return 
    results_dict = {}
    stat_dict = {}
    column_list = []

    try:
        stat_dict["Tank"] = [f"{rank_json["competitive"]["pc"]["tank"]["division"]} {rank_json["competitive"]["pc"]["tank"]["tier"]}" for x in json.keys()]
    except: 
        stat_dict["Tank"] = [None for x in json.keys()]
    try: 
        stat_dict["Damage"] = [f"{rank_json["competitive"]["pc"]["damage"]["division"]} {rank_json["competitive"]["pc"]["damage"]["tier"]}" for x in json.keys()]
    except: 
        stat_dict["Damage"] = [None for x in json.keys()]
    try:
        stat_dict["Support"] = [f"{rank_json["competitive"]["pc"]["support"]["division"]} {rank_json["competitive"]["pc"]["support"]["tier"]}" for x in json.keys()]
    except:
        stat_dict["Support"] = [None for x in json.keys()]
    try:
        stat_dict["Open"] = [f"{rank_json["competitive"]["pc"]["open"]["division"]} {rank_json["competitive"]["pc"]["open"]["tier"]}" for x in json.keys()]
    except: 
        stat_dict["Open"] = [None for x in json.keys()]

    for key in json.keys() :
        for i in range(0, len(json[key])) :
            if not type(json[key]) == list :
                return
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
    df.to_csv(f"src/Stats/{username} Stats.csv")
