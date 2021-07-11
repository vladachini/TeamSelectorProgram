
def sort_stat(players:list)->list:
    """
    :param players: [('5557b69b', 199, 2, 9), ('d3ecc964', 195, 3, 11), ('a34b1d8b', 191, 5, 17), ('578bafa9', 191, 5, 14)]
    :return: list sorted by a certain stat that is in index [2]
    """
    new_list = players
    new_list.sort(key=getStat, reverse=True)
    return new_list


def getStat(element) -> int:
    return element[2]


def getHeight(element) ->int:
    return element[1]


def getScore(element) -> int:
    return element[3]


def sorting_height(players: dict, num_teams, reverse_list=True) -> list:
    h_lst = []
    for id in players:
        stats = players.get(id)
        height = int(stats["Height"])
        shooting = int(stats["Shooting"])
        ball_handling = int(stats["Ball_handling"])
        rebounding = int(stats["Rebounding"])
        defense = int(stats["Defense"])
        total = shooting+ball_handling+rebounding+defense
        h_lst.append((id, height, shooting, total))
    h_lst.sort(key=getHeight, reverse=reverse_list)
    twenty_tall = []
    for index in range(0,num_teams):
        twenty_tall.append(h_lst[index])
    twenty_tall.sort(key=getScore, reverse=True)
    final_lst=[]
    for item in twenty_tall:
        id, h, shooting, score = item
        final_lst.append(id)
    return final_lst


def sorting_score(players: dict) ->list:
    s_list= []
    for id in players:
        stats = players.get(id)
        height = int(stats["Height"])
        shooting = int(stats["Shooting"])
        ball_handling = int(stats["Ball_handling"])
        rebounding = int(stats["Rebounding"])
        defense = int(stats["Defense"])
        total = shooting+ball_handling+rebounding+defense
        s_list.append((id, height, shooting, total))
        s_list.sort(key=getScore, reverse=True)
    final_lst = []
    for item in s_list:
        id, h, shooting, score = item
        final_lst.append(id)
    return final_lst


def sort_teams(team_stats : dict, teams:dict) -> dict:
    sorted_list = []
    sorted_dict = {}
    sorted_teams_list =[]
    for team in team_stats:
        stats = team_stats.get(team)
        total = stats["Total Score"]
        average_score = stats["Average Score"]
        height= stats["Average Height"]
        total_weighted = int(total) + int(average_score) + int(height)
        sorted_list.append((team,height, total_weighted, average_score))
    sorted_list.sort(key=getStat, reverse=False)
    for entry in sorted_list:
        team,height, total, average_score = entry
        players= teams[team]
        sorted_dict[team] = players
        sorted_teams_list.append(team)
    return sorted_teams_list


def sorting_updated_players (new_players :list, database_dict:dict):
    sorted_list = []
    for id in new_players:
        stats = database_dict.get(id)
        height = int(stats["Height"])
        shooting = int(stats["Shooting"])
        ball_handling = int(stats["Ball_handling"])
        rebounding = int(stats["Rebounding"])
        defense = int(stats["Defense"])
        total_weighted = shooting + ball_handling + rebounding + defense + height
        sorted_list.append((id, height, shooting, total_weighted))
        sorted_list.sort(key=getScore, reverse=True)
    final_lst = []
    for item in sorted_list:
        id, h, shooting, score = item
        final_lst.append(id)
    return final_lst


















