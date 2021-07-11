from pymongo import *


client = MongoClient("mongodb+srv://vladachini:kovacina2002@cluster0.5c4te.mongodb.net/Team_Selector?retryWrites=true&w=majority")
db= client["Team_Selector"]


def get_db():
    return db


def get_collection():
    return collection


def generate_database(players:dict, teams:dict, season = None):
    user = input("Do you want to upload to database? (Y/N)")
    if user.upper().strip() == "Y":
        if season == None:
            season = input("Please enter the season year (YYYY)")
        collection_name = "Season_"+ season
        mycol = db[collection_name]

        entries = []
        for id in players:
            #gives id, the key in the players dict
            player = {}
            player["_id"] = id
            stats = players.get(id)
            f_name = stats.get('First_name')
            player["First_name"]= f_name
            l_name = stats.get('Last_name')
            player["Last_name"] = l_name
            dob = stats.get('DOB')
            player["DOB"] = dob
            height = int(stats["Height"])
            player["Height"] = height
            shooting = int(stats["Shooting"])
            player["Shooting"] = shooting
            ball_handling = int(stats["Ball_handling"])
            player["Ball_handling"] = ball_handling
            rebounding = int(stats["Rebounding"])
            player["Rebounding"] = rebounding
            defense = int(stats["Defense"])
            player["Defense"] = defense
            total = shooting + ball_handling + rebounding + defense
            player["Total"] = total
            team = get_team(id, teams)
            player["Team"] = team
            query_all = mycol.find_one(player)
            #query_team = mycol.find_one({"_id":id, "Team": team})
            query_id = mycol.find_one({"_id":id})
            if query_all == None and query_id == None:
                print("Adding: ", player)
                mycol.insert_one(player)
                entries.append(player)
            elif query_all == None and query_id != None:
                # update the Team
                print("Updating :", player)
                mycol.update_one({"_id":id}, { "$set": {"Team": team}})

    #x = mycol.insert_many(entries)

def add_to_database(players:dict, teams:dict, collection_name):
    mycol = db[collection_name]
    entries = []
    for id in players:
        # gives id, the key in the players dict
        player = {}
        player["_id"] = id
        stats = players.get(id)
        f_name = stats.get('First_name')
        player["First_name"] = f_name
        l_name = stats.get('Last_name')
        player["Last_name"] = l_name
        dob = stats.get('DOB')
        player["DOB"] = dob
        height = int(stats["Height"])
        player["Height"] = height
        shooting = int(stats["Shooting"])
        player["Shooting"] = shooting
        ball_handling = int(stats["Ball_handling"])
        player["Ball_handling"] = ball_handling
        rebounding = int(stats["Rebounding"])
        player["Rebounding"] = rebounding
        defense = int(stats["Defense"])
        player["Defense"] = defense
        total = shooting + ball_handling + rebounding + defense
        player["Total"] = total
        team = get_team(id, teams)
        player["Team"] = team
        query_all = mycol.find_one(player)
        # query_team = mycol.find_one({"_id":id, "Team": team})
        query_id = mycol.find_one({"_id": id})
        if query_all == None and query_id == None:
            print("Adding: ", player)
            mycol.insert_one(player)
            entries.append(player)
        elif query_all == None and query_id != None:
            # update the Team
            print("Updating :", player)
            mycol.update_one({"_id": id}, {"$set": {"Team": team}})

def add_to_database_cache(changed_players, collection_name, players, teams):
    #changed_players is a list [(id,team),(id,team)]
    mycol = db[collection_name]
    for player in changed_players:
        _id, team = player
        query_id = mycol.find_one({"_id": _id})
        if query_id == None:
            player = {}
            player["_id"] = _id
            stats = players.get(_id)
            f_name = stats.get('First_name')
            player["First_name"] = f_name
            l_name = stats.get('Last_name')
            player["Last_name"] = l_name
            dob = stats.get('DOB')
            player["DOB"] = dob
            height = int(stats["Height"])
            player["Height"] = height
            shooting = int(stats["Shooting"])
            player["Shooting"] = shooting
            ball_handling = int(stats["Ball_handling"])
            player["Ball_handling"] = ball_handling
            rebounding = int(stats["Rebounding"])
            player["Rebounding"] = rebounding
            defense = int(stats["Defense"])
            player["Defense"] = defense
            total = shooting + ball_handling + rebounding + defense
            player["Total"] = total
            player_team = get_team(_id, teams)
            player["Team"] = player_team
            print("Adding: ", player)
            mycol.insert_one(player)
        else:
            print("Updating :", _id)
            mycol.update_one({"_id": _id}, {"$set": {"Team": team}})







def get_players_dict(collection):
    list_players = []
    main = {}
    cursor = collection.find()
    for players in cursor:
        list_players.append(players)
    for player in list_players:
        id = player["_id"]
        f_name = player["First_name"]
        l_name = player["Last_name"]
        dob = player["DOB"]
        height = player["Height"]
        shooting = player["Shooting"]
        ball_handling = player["Ball_handling"]
        rebounding = player["Rebounding"]
        defense = player["Defense"]
        total = player["Total"]
        main[id] = {"First_name":f_name, "Last_name":l_name,"DOB":dob, "Height": height,
                    "Shooting": shooting,"Ball_handling": ball_handling,"Rebounding":rebounding,
                    "Defense": defense, "Total":total}
    return main


def get_teams_dict(collection):
    teams = {}
    i = 0
    cursor = collection.find({"Team": i})
    while cursor.count() != 0 :
        list_players = []
        temp_team =[]
        for players in cursor:
            list_players.append(players)
        for player in list_players:
            id = player["_id"]
            temp_team.append(id)
        teams[i] = temp_team
        i += 1
        cursor = collection.find({"Team": i})
    return teams


def update_player(_id, category, new_data) -> None:
    myquery = {"_id": _id}
    newvalues = {"$set": {category: new_data}}
    collection.update_one(myquery,newvalues)

def update_player_col(_id, category, new_data, collection_name) -> None:
    mycol = db[collection_name]
    myquery = {"_id": _id}
    newvalues = {"$set": {category: new_data}}
    mycol.update_one(myquery,newvalues)


def get_team(id,teams:dict):
    player_team = 0
    for team in range(len(teams.keys())):
        for player in teams[team]:
            if player == id:
                player_team = team
    return player_team


def delete_player(id, players: dict,teams, collection):
    mycol = db[collection]
    myquery = {"_id": id}
    mycol.delete_one(myquery)
    for team in teams:
        player = teams.get(team)
        if id in player:
            player.remove(id)
    del players[id]










