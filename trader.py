import copy
from sorter import *
from database import *

def manual_trade(p1_f, p1_l, p1_t,p2_f,p2_l, p2_t, main:dict, teams:dict) -> dict:
    """
    Trades player1 and player2; they switch teams, the teams are not rebalanced
    :param player1: First Player
    :param player2: Second Player
    :param main: Main dictionary with all the players
    :param teams: Teams dictionary
    :return: returns the new team dictionary
    """
    player_list1 = teams[p1_t]
    player_list2 = teams[p2_t]
    player1_id = ""
    player2_id = ""
    for item in player_list1:
        player1= main.get(item)
        player1_fname = player1.get('First_name').strip()
        player1_lname = player1.get("Last_name").strip()
        if player1_fname == p1_f and player1_lname == p1_l:
            player1_id = item
            teams[p1_t].remove(player1_id)
    for item in player_list2:
        player2 = main.get(item)
        player2_fname = player2.get('First_name').strip()
        player2_lname = player2.get("Last_name").strip()
        if player2_fname == p2_f and player2_lname == p2_l:
            player2_id = item
            teams[p2_t].remove(player2_id)
    teams[p1_t].append(player2_id)
    teams[p2_t].append(player1_id)
    print(player1_id)
    print(player2_id)
    #trade_db(player1_id, p1_t, player2_id, p2_t)

def get_trades(p1_f, p1_l, p1_t,main:dict, teams:dict)->dict:
    """

    :param p1_f:
    :param p1_l:
    :param p1_t:
    :param main:
    :param teams:
    :return:

    """
    best_options = []
    other_options = []
    copy_teams = copy.deepcopy(teams)
    del copy_teams[p1_t]
    stat_diff = 2
    height_diff = 10
    total_diff = 3
    player_list = teams[p1_t]
    player_id = ""
    for item in player_list:
        player= main.get(item)
        player_fname= player.get('First_name').strip()
        player_lname = player.get("Last_name").strip()
        if player_fname == p1_f and player_lname == p1_l:
            player_id = item
    stats = main[player_id]
    height_main = int(stats["Height"])
    shooting_main = int(stats["Shooting"])
    ball_handling_main = int(stats["Ball_handling"])
    rebounding_main = int(stats["Rebounding"])
    defense_main = int(stats["Defense"])
    total_main = shooting_main + ball_handling_main + rebounding_main + defense_main
    for team_number in range(len(copy_teams.keys())):
        for id in teams[team_number]:
            stats2 =  main[id]
            height_temp = int(stats2["Height"])
            shooting_temp = int(stats2["Shooting"])
            ball_handling_temp = int(stats2["Ball_handling"])
            rebounding_temp = int(stats2["Rebounding"])
            defense_temp = int(stats2["Defense"])
            total_temp = shooting_temp + ball_handling_temp + rebounding_temp + defense_temp
            team = get_team(id,teams)
            sameTeam1 = is_in_same_team(team,best_options,teams)
            sameTeam2 = is_in_same_team(team,other_options,teams)
            if abs(height_temp-height_main)<=height_diff and abs(total_temp-total_main) <= total_diff \
                and abs(shooting_temp-shooting_main)<= stat_diff and abs(ball_handling_temp-ball_handling_main)<= stat_diff \
                and abs(rebounding_temp - rebounding_main) <=stat_diff and abs( defense_temp- defense_main) <=stat_diff and \
                    sameTeam1 == False and p1_t != team_number:
                best_options.append(id)
            elif abs(height_temp-height_main)<=height_diff and abs(total_temp-total_main) <= total_diff \
                and abs(shooting_temp-shooting_main)<= stat_diff and item not in best_options and sameTeam2 == False \
                    and p1_t != team_number:
                other_options.append(id)
    options = {}
    num_teams = len(teams.keys())
    if len(best_options) <= num_teams:
        options["Best Options"] = best_options
    else:
        options["Best Options"] = best_options[:num_teams]

    if len(other_options) <= num_teams:
        options["Other Options"] = other_options
    else:
        options["Other Options"] = other_options[:num_teams]
    return options


def get_team(id,teams:dict):
    player_team = 0
    for team in range(len(teams.keys())):
        for player in teams[team]:
            if player == id:
                player_team = team
    return player_team


def is_in_same_team(team,players:list, teams:dict):

    team_list = []
    if len(players)> 0:
        for player in players:
            player_team = get_team(player,teams)
            team_list.append(player_team)
        if team in team_list:

            return True
        return False
    else:
        return False


def trade_db(id1, team1, id2, team2, collection):
    temp_team = team1
    myquery = {"_id": id1}
    newvalues = {"$set": {"Team": team2}}
    collection.update_one(myquery,newvalues)
    myquery2 = {"_id": id2}
    newvalues2 = {"$set": {"Team": temp_team}}
    collection.update_one(myquery2, newvalues2)






