# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings
from OpenFile import *
from sorter import *
from printer import *
from trader import *
import copy
from database import *


def main() -> None:
    main_loop = True
    while main_loop:
        user = input("What do you want to do?\n L)Load exisitng database\n O)Open using csv file \n")
        if user.upper().strip() == "L":
            main_loop =False
            season = input("Which season (Enter the year)")
            collection_name = "Season_" + season
            mycol = db[collection_name]
            main_dict = get_players_dict(mycol)
            teams = get_teams_dict(mycol)
            print_teams_db(teams, mycol)
            trade(main_dict, teams)
            delete_players_printer(main_dict, teams, mycol)
            print_teams_db(teams, mycol)
            generate_database(main_dict, teams)
            print("done")

        elif user.upper().strip() == "O":
            create = False
            main_loop = False
            override = False
            update = False
            season = get_season()
            current_season = "Season_"+season
            season_list = db.list_collection_names()
            if current_season in season_list:
                print("Selected Season Already Exists!")
                update_or_override = input("Do you want to: \nU)pdate \nO)verride \n")
                while not (override or update):
                    if update_or_override.strip().upper() == "O":
                        print("Selected season:",season, " will be deleted and new season will be created")
                        override = True
                    elif update_or_override.strip().upper() == "U":
                        print("Selected season:",season, " will be updated with the mew players from the file")
                        update = True
                    else:
                        print("Invalid Selection, Try Again")
            else:
                create =True

            # Asks User for CSV file
            valid_file = False
            while not valid_file:
                try:
                    file = input("Enter CSV file name: ")
                    # calls the generator_print program to generate more entries
                    generator_print(file)
                    # Opens File
                    main_dict = csvOpener(file)
                    valid_file = True
                except FileNotFoundError:
                    print("The ", file, " file does not exist")

            if override:
                mycol = db[current_season]
                #deleting season from database and recreating a new one
                mycol.drop()
                create = True

            if create:
                new_season = db[current_season]
                # Calculate number of players based on dictionary inputs
                num_players = len(main_dict.keys())
                # Make Deepcopy of main_dict
                temp_dict = copy.deepcopy(main_dict)
                print("Number of players in the League: ", num_players)
                # Ask User for number of teams
                num_teams = int(input("How many teams do you want to make: "))
                teams = {}
                # Find tallest players
                height_list = sorting_height(main_dict, num_teams)
                # Add players to teams
                add_player_to_team(height_list, teams)
                # Remove players that were added from the temp_dict (deepcopy of main_dict)
                remove_players(height_list, temp_dict)
                # Find shortest players, height list is reversed and top players are selected based on shooting
                height_list = sorting_height(main_dict, num_teams, False)
                # Add players to teams
                add_player_to_team(height_list, teams, True)
                remove_players(height_list, temp_dict)
                score_list = sorting_score(temp_dict)
                adding_alg(score_list, teams, num_teams)
                print_teams(main_dict,teams)
                trade(main_dict, teams)
                delete_players_printer(main_dict, teams,current_season)
                print_teams( main_dict,teams )
                generate_database(main_dict, teams, season)
            # Add the csv file to main dict and compare with dict that you get from the database, add any new entries and update the database
            if update:
                new_season = db[current_season]
                database_dict= get_players_dict(new_season)
                teams_database_dict = get_teams_dict(new_season)
                database_list= database_dict.keys()
                main_dict_list = main_dict.keys()
                new_ids = []
                for id in main_dict_list:
                    if id not in database_list:
                        new_ids.append(id)
                        players_stats = main_dict.get(id)
                        database_dict[id] = players_stats
                print(new_ids)
                num_teams = len(teams_database_dict.keys())
                #Get list of teams and there stats (Average score, Average height, Average Total Score)
                team_stats = get_team_total(database_dict, teams_database_dict)
                sorted_teams = sort_teams(team_stats,teams_database_dict )
                print("Sorted Teams: ",sorted_teams)
                #Sort the new players in descending order (best to worst)
                updated_players_ranked_list = sorting_updated_players(new_ids, database_dict)
                updating_alg(updated_players_ranked_list, sorted_teams, teams_database_dict, num_teams)
                print_teams(database_dict, teams_database_dict)
                trade(database_dict, teams_database_dict)
                delete_players_printer(database_dict, teams_database_dict, current_season)
                print_teams_db(teams, current_season)
                generate_database(database_dict, teams_database_dict, season)
        else:
            print("Invalid Input! Input either L,O or U")


def remove_players(players: list, temp_dict: dict) -> None:
    #Iterates through players list and deletes all the players from the temp_dict
    for player in players:
        del temp_dict[player]


def add_player_to_team(players: list, teams: dict, r=False) -> None:
    if r:
        players.reverse()
    for index in range(len(players)):
        try:
            teams[index].append(players[index])
        except KeyError:
            teams[index] = [players[index]]


def adding_alg(players: list, teams: dict, num_teams: int):
    lenght= len(players)
    max = num_teams
    loops= round(lenght/max)
    for index in range(loops):
        for i in range(max):
            try:
                teams[i].append(players[i])
            except IndexError:
                pass
        del players[0:num_teams]
        players.reverse()

def get_season():
    season_valid = False
    while not season_valid:
        season = input("Which season (Enter the year)")
        try:
            val = int(season)
            if val >= 2015:
                season_valid = True
        except ValueError:
            print("That's not a valid or supported season")
    return season

def updating_alg(players :list, teams_list:list, teams:dict, num_teams):
    lenght = len(players)
    max = num_teams
    loops = round(max/lenght)
    for index in range(loops):
        if len(players)!= 0:
            for i in range(max):
                try:
                    team = teams_list[i]
                    teams[team].append(players[i])
                except IndexError:
                    break
            del players[0:num_teams]
            players.reverse()
        else:
            break



def update_teams(num_teams: int, team_stats : dict, teams :dict, main: dict):
    sorted_teams = {}

def get_teams_db(collection_name):
    mycol = db[collection_name]
    main_dict = get_players_dict(mycol)
    teams = get_teams_dict(mycol)
    team_list = []
    for team in teams:
        team_list.append(team)
    return (team_list,teams, main_dict)




if __name__ == '__main__':
    main()
