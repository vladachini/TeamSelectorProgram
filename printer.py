from trader import *
from OpenFile import *
from database import *


def print_teams (main:dict, teams :dict) -> None:
    """
    Function used to print teams and players
    :param main: main dictionary with {id:{stats},...}
    :param teams: team dictionary with {team_id: [player1_id, player2_id...],...}
    :return: Nothing its prints teams with player names, height and overall score
    """
    total_team = 0
    team_height = 0
    num_players=0
    average_team = 0
    for key in teams:
        print("Team: ", key)
        for player in teams.get(key):
            num_players +=1
            stats = main.get(player)
            f_name= stats.get('First_name')
            l_name= stats.get("Last_name")
            height = int(stats["Height"])
            shooting = int(stats["Shooting"])
            ball_handling = int(stats["Ball_handling"])
            rebounding = int(stats["Rebounding"])
            defense = int(stats["Defense"])
            total = shooting + ball_handling + rebounding + defense
            team_height += height
            print(f_name, l_name, "Total Score: ", total, " Height: ", height)
            average_team += round(total / num_players)
            total_team += total
        print("Team: ", key, "Total Score: ", total_team," Average Score: ", average_team, "Average Height: ", (round(team_height/num_players)),"\n")
        #Resets total_team, num_players, and team_height for the next team
        total_team = 0
        num_players = 0
        team_height = 0
        average_team = 0
    print("--------------------------------------------")


def print_teams_db (teams :dict, collection) -> None:
    """
    Function used to print teams and players from the database
    :param main: main dictionary with {id:{stats},...}
    :param teams: team dictionary with {team_id: [player1_id, player2_id...],...}
    :return: Nothing its prints teams with player names, height and overall score
    """
    average_team = 0
    team_height = 0
    num_players=0
    total_team = 0
    for key in teams:
        print("Team: ", key)
        for player in teams.get(key):
            num_players +=1
            list_player = []
            query = collection.find({"_id": player})
            for i in query:
                list_player.append(i)
            for item in list_player:
                f_name = item.get('First_name')
                l_name = item.get("Last_name")
                height = int(item["Height"])
                shooting = int(item["Shooting"])
                ball_handling = int(item["Ball_handling"])
                rebounding = int(item["Rebounding"])
                defense = int(item["Defense"])
                total = shooting + ball_handling + rebounding + defense
                team_height += height
                print(f_name, l_name, "Total Score: ", total, " Height: ", height)
                average_team += round(total / num_players)
                total_team += total
        print("Team: ", key," Total Score: ", total_team, " Average Score: ", average_team, "Average Height: ", (round(team_height/num_players)),"\n")
        #Resets total_team, num_players, and team_height for the next team
        total_team = 0
        average_team = 0
        num_players = 0
        team_height = 0
    print("--------------------------------------------")


def trade_printer(p1_f, p1_l, p1_t,p2_f,p2_l, p2_t, main:dict, teams:dict):
    print(p1_f, " ",p1_l, "from Team: ",p1_t, "Traded to Team: ",p2_t," for: ",p2_f, " ",p2_l )
    manual_trade(p1_f, p1_l, p1_t,p2_f,p2_l, p2_t, main, teams)
    print_teams(main, teams)


def trade_avail_printer(p1_f, p1_l, p1_t, main:dict, teams:dict):
    players = get_trades(p1_f, p1_l, p1_t, main, teams)
    print("\n BEST TRADE OPTIONS FOR: ", p1_f," ", p1_l, " from Team ", p1_t,":")
    print("----------------------")
    best_list= players["Best Options"]
    for player in best_list:
        stats= main[player]
        f_name = stats.get('First_name')
        l_name = stats.get("Last_name")
        height = int(stats["Height"])
        shooting = int(stats["Shooting"])
        ball_handling = int(stats["Ball_handling"])
        rebounding = int(stats["Rebounding"])
        defense = int(stats["Defense"])
        total = shooting + ball_handling + rebounding + defense
        team =  get_team(player,teams)
        print(f_name, " ", l_name," Height: ", height, " Total Score: ", total, " From Team: ", team)

    print("\nOTHER TRADE OPTIONS FOR:  ", p1_f, " ", p1_l, " from Team ", p1_t, ":")
    print("--------------------------")
    other_list = players["Other Options"]
    for player2 in other_list:
        stats2= main[player2]
        f_name2 = stats2.get('First_name')
        l_name2 = stats2.get("Last_name")
        height2 = int(stats2["Height"])
        shooting2 = int(stats2["Shooting"])
        ball_handling2 = int(stats2["Ball_handling"])
        rebounding2 = int(stats2["Rebounding"])
        defense2 = int(stats2["Defense"])
        total2 = shooting2 + ball_handling2 + rebounding2 + defense2
        team2 = get_team(player2, teams)
        print(f_name2, " ", l_name2," Height: ", height2, " Total Score: ", total2," From Team: ", team2)


def trade(main_dict, teams):
    loop = True
    while loop:
        trade = input("Do you want to Trade any players?(Y/N): ")
        if trade.upper()== "Y" or trade.upper() == "YES":
            loop2 = True
            while loop2:
                trade_type= input("Do you want to Manual Trade (M/m) or look for tradable players (L/l)? ")
                if trade_type.upper() == "M":
                    player1_firstname =  input("Enter Player 1 first name: ").strip()
                    player1_lastname = input("Enter Player 1 last name: ").strip()
                    player1_team = int(input("Enter Player 1 Team Number: "))
                    player2_firstname = input("Enter Player 2 first name: ").strip()
                    player2_lastname = input("Enter Player 2 last name: ").strip()
                    player2_team = int(input("Enter Player 2 Team Number: "))
                    trade_printer(player1_firstname, player1_lastname, player1_team, player2_firstname, player2_lastname,
                                  player2_team, main_dict, teams)
                    loop2= False
                elif trade_type.upper() == "L":
                    player1_firstname = input("Enter Player 1 first name: ").strip()
                    player1_lastname = input("Enter Player 1 last name: ").strip()
                    player1_team = int(input("Enter Player 1 Team Number: "))
                    trade_avail_printer(player1_firstname,player1_lastname,player1_team,main_dict, teams)

                    player2_firstname = input("Enter First Name of Player you wish to trade for: ").strip()
                    player2_lastname = input("Enter Last Name of Player you wish to trade for: ").strip()
                    player2_team = int(input("Enter Team Number of Player you wish to trade for: "))
                    trade_printer(player1_firstname, player1_lastname, player1_team, player2_firstname,
                                    player2_lastname,
                                    player2_team, main_dict, teams)
                    loop2=False
                else:
                    print("Invalid input")
        elif trade.upper() == "N" or trade.upper() == "NO":
            loop = False
        else:
            print("Invalid Input")


def generator_print(filename):
    loop = True
    while loop:
        gen = input("Do you want to Update/Generate any players?(Y/N): ")
        if gen.upper() == "Y" or gen.upper() == "YES":
            type_of_gen = input("Generate stats out of 10? (Y/N)")
            if type_of_gen.upper() == "Y":
                entries = int(input("How many  random entries: "))
                generate10(filename, entries)
            else:
                print("Generating stats out of 5")
                entries = int(input("How many  random entries: "))
                generate(filename, entries)

            loop = False
        elif gen.upper() == "N" or gen.upper() == "NO":
            loop = False
        else:
            print("Invalid Input")


def get_team(id,teams:dict):
    player_team = 0
    for team in range(len(teams.keys())):
        for player in teams[team]:
            if player == id:
                player_team = team
    return player_team


def get_team_total(main:dict, teams:dict) ->dict:
    total_team = 0
    team_height = 0
    num_players = 0
    average_team = 0
    team_stats = {}
    for key in teams:
        for player in teams.get(key):
            num_players += 1
            stats = main.get(player)
            f_name = stats.get('First_name')
            l_name = stats.get("Last_name")
            height = int(stats["Height"])
            shooting = int(stats["Shooting"])
            ball_handling = int(stats["Ball_handling"])
            rebounding = int(stats["Rebounding"])
            defense = int(stats["Defense"])
            total = shooting + ball_handling + rebounding + defense
            team_height += height
            average_team += round(total / num_players)
            total_team += total
            average_height = (round(team_height / num_players))
        team_scores = {"Total Score": total_team, "Average Score": average_team, "Average Height": average_height}
        team_stats[key] = team_scores
        # Resets total_team, num_players, and team_height for the next team
        total_team = 0
        num_players = 0
        team_height = 0
        average_team = 0
    return team_stats


def delete_players_printer(main: dict, teams:dict, collection):
    loop = True
    while loop:
        to_delete = input("Do you want to delete any players? (Y/N)\n")
        if to_delete.upper()== "Y":
            f_name =  input("Enter player First Name: \n")
            l_name = input("Enter player Last Name: \n")
            player_team = int(input("Enter player team number: \n"))
            players_in_team = teams[player_team]
            for id in players_in_team:
                player_stats = main[id]
                check_first =  player_stats.get("First_name")
                check_last = player_stats.get("Last_name")
                if check_first.upper() == f_name.upper() and check_last.upper() == l_name.upper():
                    print(id)
                    delete_player(id, main,teams, collection)
                    print(f_name,l_name," from team ", player_team, " was deleted")
        elif to_delete.upper() == "N":
            loop= False
        else:
            print("Invalid Input, type 'Y' for YES or 'N' for NO \n")







