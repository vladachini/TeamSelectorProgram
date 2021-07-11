import PySimpleGUI as sg
from main import *


def start_page():
    active_seasons = db.list_collection_names()
    season_list_column = [
        [
            sg.Text("Search Season"),
            sg.In(size=(25, 1), enable_events=True, key="-SEASONS-"),
            sg.Button("Search", enable_events=True, key="-SEARCH-")
        ],
        [
            sg.Listbox(
                values=active_seasons, enable_events=True, size=(40, 20), key="-SEASON LIST-"
            )
        ],
    ]

    select_csv_window = [
        [sg.Text('Please Select CSV File:')],
        [sg.Input(), sg.FileBrowse()],
        [sg.OK(), sg.Cancel()]
    ]

    # For now will only show the name of the file that was chosen
    create_season_column = [
        [sg.Text("Can't Find Your Season on The Left? ")],
        [sg.Text(size=(25, 1), key="-NAME-")],
        [sg.Button('Create Season', size=(20, 2), key="-CREATE-")],
    ]

    # ----- Full layout -----
    layout = [
        [
            sg.Column(season_list_column),
            sg.VSeperator(),
            sg.Column(create_season_column),
        ]
    ]

    start_page = sg.Window("Team Creator", layout, enable_close_attempted_event=True)
    csv_selector = sg.Window("Select CSV File", select_csv_window)

    while True:
        event, values = start_page.read()
        start_page.refresh()
        if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no(
                'Do you really want to exit?') == 'Yes':
            start_page.close()
            break

        if event == "-SEARCH-" and values["-SEASONS-"] != None:

            if values["-SEASONS-"] in active_seasons:
                start_page["-SEASON LIST-"].update(values=[values["-SEASONS-"]])
            else:
                start_page["-SEASON LIST-"].update(values=["No Results Found"])

        if event == "-SEARCH-" and values["-SEASONS-"] == "":
            start_page["-SEASON LIST-"].update(values=active_seasons)

        if event == "-CREATE-":
            # csv_selector.read()
            isInvalid = True
            while isInvalid:
                csv_file = sg.popup_get_file('Please enter CSV file name')
                print(csv_file)
                if csv_file != None:
                    try:
                        main_dict = csvOpener(csv_file)
                        isInvalid = False
                        for id in main_dict:
                            player = main_dict[id]
                            shooting = int(player.get("Shooting"))
                            ball_handling = int(player.get("Ball_handling"))
                            rebounding = int(player.get("Rebounding"))
                            defense = int(player.get("Defense"))
                            total = shooting + ball_handling + rebounding + defense
                            player["Total"] = total

                        current_season, num_teams = select_year_team()
                        if current_season == None:
                            sg.popup('No Season Year was Selected')
                        elif current_season in active_seasons:
                            choice = sg.popup_yes_no("Selected Season Already Exists! \n Do you want to Update the existing season?", modal=True)
                            same_num_teams = True
                            skip = False
                            if choice == "Yes":
                                new_season = db[current_season]
                                database_dict = get_players_dict(new_season)
                                teams = get_teams_dict(new_season)
                                num_teams_dict =len(teams.keys())
                                if num_teams != num_teams_dict:
                                    choice = sg.popup_yes_no(
                                        "Different Number of Teams Selected! \nDo you want to keep the same number of teams that are already in the season?",
                                        modal=True)
                                    if choice == "No":
                                        choice = sg.popup_yes_no(
                                            "Do you want to use your selected number of teams? \n You selected to make:" + str(num_teams),
                                            modal=True)
                                        if choice =="Yes":
                                            same_num_teams = False
                                        else:
                                            skip =True
                                    else:
                                        skip =True
                                if same_num_teams and not skip:
                                    database_list = database_dict.keys()
                                    main_dict_list = main_dict.keys()
                                    new_ids = []
                                    for id in main_dict_list:
                                        if id not in database_list:
                                            new_ids.append(id)
                                            players_stats = main_dict.get(id)
                                            database_dict[id] = players_stats
                                    print(new_ids)
                                    num_teams = num_teams_dict
                                    # Get list of teams and there stats (Average score, Average height, Average Total Score)
                                    team_stats = get_team_total(database_dict, teams)
                                    sorted_teams = sort_teams(team_stats, teams)
                                    # Sort the new players in descending order (best to worst)
                                    updated_players_ranked_list = sorting_updated_players(new_ids, database_dict)
                                    updating_alg(updated_players_ranked_list, sorted_teams, teams, num_teams)
                                    team_display_UI(current_season, True, database_dict, teams, None)
                                elif not same_num_teams and not skip:
                                    create_teams(main_dict, num_teams, current_season)
                            else:
                                break
                        else:
                            sg.popup("Creating New ", current_season, " from the selected CSV")
                            new_season = db[current_season]
                            # Calculate number of players based on dictionary inputs
                            num_players = len(main_dict.keys())
                            start_page.close()
                            create_teams(main_dict, num_teams, current_season)
                            break

                    except UnicodeDecodeError:
                        sg.popup_ok("Invalid File Type!\n Please Input CSV")
                        isInvalid = True

                else:
                    sg.popup('No File was Selected')
                    isInvalid = False

        if event == "-SEASON LIST-" and values["-SEASON LIST-"][0] != "No Results Found":

            loaded = True
            for i in range(1, 1000):
                completed = sg.one_line_progress_meter('Loading Database ', i + 1, 1000, 'Loading:', orientation="h")
                if i == 999:
                    completed = True
                    break
                if completed == False:
                    break

            if completed:
                start_page.close()
                team_display_UI(values['-SEASON LIST-'][0])
                break

    # ----Closes Window ---
    start_page.close()


def select_year_team():
    choose_year = [
        [sg.Text("Please Select Season Year:")],
        [sg.Slider(range=(2010, 2050),
                   default_value=2020,
                   size=(20, 15),
                   orientation='horizontal',
                   font=('Helvetica', 12), key="-YEAR-")],
        [sg.Text("Please Select Number of Teams:")],
        [sg.Slider(range=(2, 50),
                   default_value=2,
                   size=(20, 15),
                   orientation='horizontal',
                   font=('Helvetica', 12), key="-NUM TEAMS-")],
        [sg.Text("Please Select Division:"),
         sg.Combo(["Novice", "Atom", "Bantam", "Midget", "Juvenile"], key="-DIVISION-", size=(20, 5),
                  enable_events=True)
         ],
        [sg.Text("Please Select Category:"),
         sg.Combo(["Boys", "Girls"], key="-GENDER-", size=(20, 5),
                  enable_events=True)],
        [sg.Button("OK", enable_events=True, key="-OK YEAR-"),
         sg.Button("Cancel", enable_events=True, key="-CANCEL YEAR-")]
    ]
    year_select = sg.Window("Select Season", choose_year, modal=True)
    choosing_year = True
    while choosing_year:
        event, values = year_select.read()
        if event == "-CANCEL YEAR-" or event == sg.WINDOW_CLOSED:
            choosing_year = False
            year_select.close()
            return (None, None)
        if event == "-OK YEAR-" and values["-GENDER-"] != "" and values["-DIVISION-"] != "":
            year = values["-YEAR-"]
            gender = values["-GENDER-"]
            div = values["-DIVISION-"]
            num_teams = int(values["-NUM TEAMS-"])
            choosing_year = False
            year_select.close()
        if event == "-OK YEAR-" and values["-GENDER-"] == "" and values["-DIVISION-"] == "":
            sg.popup("Please Fill All Requirements")

    current_season = "Season " + div + " " + gender + " " + str(int(year))

    return (current_season, num_teams)


def create_teams(main_dict, num_teams, collection):
    teams = {}
    temp_dict = copy.deepcopy(main_dict)
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
    team_list = []
    for team in teams:
        team_list.append(team)
    team_display_UI(collection, True, main_dict, teams, team_list)


def team_display_UI(collection, csv=False, main_dict=None, teams=None, team_list=None):
    changed_players = []
    if csv == False:
        team_list, teams, main_dict = get_teams_db(collection)
    w, h = sg.Window.get_screen_size()
    team_total_dict = get_team_total(main_dict, teams)
    team_total_list = []

    selected_player = ''

    for team in team_total_dict:
        team_stats = team_total_dict[team]
        team_total_list += [
            [team, team_stats["Total Score"], team_stats["Average Score"], team_stats["Average Height"]]]

    data = team_total_list
    print(data)
    teams_display = [
        [sg.Text(("Teams in " + collection + ":"), font=("Helvetica", 18), enable_events=True, size=(50, 1))],
        [sg.Table(values=data, size=(100, 100),
                  headings=['Team', 'Total Score', 'Average Score'],
                  def_col_width=20,
                  auto_size_columns=False,
                  row_height=35,
                  text_color='black', background_color='white', header_font=("Helvetica", 14),
                  header_background_color='white', font=("Helvetica", 12),
                  justification='center',
                  enable_events=True, change_submits=True, bind_return_key=True, key="-TEAM-",
                  num_rows=10)]]

    player_display = [[sg.Text("Players on Selected Team: ", font=("Helvetica", 18))],
                      [sg.Table(values=[], size=(30, 30),
                                headings=['First Name', 'Last Name', 'DOB', 'Height', 'Shooting', 'Ball Handling',
                                          'Rebounding', 'Defense', 'Total'],
                                def_col_width=10, font=("Helvetica", 12),
                                auto_size_columns=False,
                                display_row_numbers=True,
                                row_height=35,
                                text_color='black', background_color='white', header_font=("Helvetica", 12),
                                header_background_color='white',
                                justification='center',
                                enable_events=True, change_submits=True, bind_return_key=True, key="-PLAYERS TABLE-",
                                num_rows=10)]]

    selected_player_name = [[sg.Text(size=(18, 1), font=("Helvetica", 30), key="-PLAYER NAME-"),
                             sg.Text("Team: ", size=(5, 1), font=("Helvetica", 30)),
                             sg.Text(size=(5, 1), font=("Helvetica", 30), key="-PLAYER TEAM-")],
                            [
                                sg.Text("Player DOB: ", size=(12, 1), font=("Helvetica", 18)),
                                sg.Text(size=(10, 1), font=("Helvetica", 18), key="-PLAYER DOB-"),
                                sg.Text("Player Height: ", size=(12, 1), font=("Helvetica", 18)),
                                sg.Text(size=(10, 1), font=("Helvetica", 18), key="-PLAYER HEIGHT-")
                            ],
                            [
                                sg.Text("Shooting: ", size=(10, 1), font=("Helvetica", 18)),
                                sg.Text(size=(12, 1), font=("Helvetica", 18), key="-PLAYER SHOOTING-"),
                                sg.Text("Ball Handling: ", size=(12, 1), font=("Helvetica", 18)),
                                sg.Text(size=(10, 1), font=("Helvetica", 18), key="-PLAYER BALL HANDLING-")],
                            [
                                sg.Text("Rebounding: ", size=(10, 1), font=("Helvetica", 18)),
                                sg.Text(size=(12, 1), font=("Helvetica", 18), key="-PLAYER REBOUNDING-"),
                                sg.Text("Defense: ", size=(12, 1), font=("Helvetica", 18)),
                                sg.Text(size=(10, 1), font=("Helvetica", 18), key="-PLAYER DEFENSE-")
                            ],
                            [
                                sg.Text("Total: ", size=(10, 1), font=("Helvetica", 18)),
                                sg.Text(size=(10, 1), font=("Helvetica", 18), key="-PLAYER TOTAL-")
                            ]
                            ]
    finding_trades = [
        [sg.Text(("Best Trades for  " + selected_player + ":"), font=("Helvetica", 18),
                 enable_events=True, size=(30, 1), key='-BEST OPTIONS TEXT-', visible=True),
         sg.Button("Trade", font=("Helvetica", 11), enable_events=True, size=(5, 1), key="-TRADE BEST-", visible=True)],
        [sg.Table(values=[], size=(100, 100),
                  headings=['First Name', 'Last Name', 'DOB', 'Height', 'Shooting', 'Ball Handling',
                            'Rebounding', 'Defense', 'Total', 'Team'],
                  def_col_width=10,
                  auto_size_columns=False,
                  row_height=35,
                  text_color='black', background_color='white', header_font=("Helvetica", 14),
                  header_background_color='white', font=("Helvetica", 12),
                  justification='center',
                  enable_events=True, change_submits=True, bind_return_key=True, key="-BEST TRADES-",
                  num_rows=5, visible=True)],
        [sg.Text(("Other Trades for  " + selected_player + ":"), font=("Helvetica", 18),
                 enable_events=True, size=(30, 1), key='-OTHER OPTIONS TEXT-', visible=True),
         sg.Button("Trade", font=("Helvetica", 11), enable_events=True, size=(5, 1), key="-TRADE OTHER-",
                   visible=True)],
        [sg.Table(values=[], size=(100, 100),
                  headings=['First Name', 'Last Name', 'DOB', 'Height', 'Shooting', 'Ball Handling',
                            'Rebounding', 'Defense', 'Total', 'Team'],
                  def_col_width=10,
                  auto_size_columns=False,
                  row_height=35,
                  text_color='black', background_color='white', header_font=("Helvetica", 14),
                  header_background_color='white', font=("Helvetica", 12),
                  justification='center',
                  enable_events=True, change_submits=True, bind_return_key=True, key="-OTHER TRADES-",
                  num_rows=5, visible=True)],

    ]
    options_column = [
        [sg.Button("Find \nTrades", font=("Helvetica", 11), enable_events=True, size=(30, 5), key="-LOOK-",
                   visible=False)],
        [sg.Button("Manual \nTrade", enable_events=True, font=("Helvetica", 11), size=(30, 5), key="-TRADE-")],
        [sg.Button("Save \nChanges", font=("Helvetica", 11), enable_events=True, size=(30, 5), key="-SAVE-")],
        [sg.Button("Remove \nPlayer", font=("Helvetica", 11), enable_events=True, size=(30, 5), key="-REMOVE-")]]

    teams_layout = [[sg.Button("Back", font=("Helvetica", 12), enable_events=True, key="-BACK-")],
                    [
                        sg.Column(teams_display),
                        sg.VSeperator(),
                        sg.Column(player_display),
                        sg.VSeperator(),
                        sg.Column(options_column)
                    ],
                    [sg.Text("-" * 1000)], [sg.Column(selected_player_name), sg.VSeperator(),
                                            sg.Column(finding_trades, key="-FINDING TRADES-", visible=False)]
                    ]

    team_window = sg.Window("Current Teams", teams_layout, enable_close_attempted_event=True, size=(w, h))
    while True:
        event, values = team_window.read(timeout=100)


        if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no(
                'Do you really want to exit?') == 'Yes':
            team_window.close()
            break
        if event == "-BACK-":
            team_window.close()
            start_page()
            break

        if event == "-TEAM-":

            players_id = teams[values["-TEAM-"][0]]
            players = []
            players_stats = []
            num_players = 0
            for id in players_id:
                player = main_dict[id]
                f_name = player["First_name"]
                l_name = player["Last_name"]
                dob = player["DOB"]
                height = player["Height"]
                shooting = player["Shooting"]
                ball_handling = player["Ball_handling"]
                rebounding = player["Rebounding"]
                defense = player["Defense"]
                total = player["Total"]
                players.append(f_name + "," + l_name)
                players_stats += [[f_name, l_name, dob, height, shooting, ball_handling, rebounding, defense, total]]
                num_players += 1

            chosen_team = values["-TEAM-"][0]
            team_window['-PLAYERS TABLE-'].update(values=players_stats)

        if event == "-PLAYERS TABLE-":
            selected_team = teams.get(values["-TEAM-"][0])
            selected_player_id = selected_team[values["-PLAYERS TABLE-"][0]]
            selected_player_stats = main_dict.get(selected_player_id)
            f_name = selected_player_stats["First_name"]
            l_name = selected_player_stats["Last_name"]
            dob = selected_player_stats["DOB"]
            height = selected_player_stats["Height"]
            shooting = selected_player_stats["Shooting"]
            ball_handling = selected_player_stats["Ball_handling"]
            rebounding = selected_player_stats["Rebounding"]
            defense = selected_player_stats["Defense"]
            total = selected_player_stats["Total"]
            display = f_name + ", " + l_name
            team_window["-PLAYER NAME-"].update(display)
            team_window["-PLAYER TEAM-"].update(values["-TEAM-"][0])
            team_window["-PLAYER HEIGHT-"].update(height)
            team_window["-PLAYER DOB-"].update(dob)
            team_window["-PLAYER SHOOTING-"].update(shooting)
            team_window["-PLAYER BALL HANDLING-"].update(ball_handling)
            team_window["-PLAYER REBOUNDING-"].update(rebounding)
            team_window["-PLAYER DEFENSE-"].update(defense)
            team_window["-PLAYER TOTAL-"].update(total)
            team_window["-LOOK-"].update(visible=True)

        if event == "-SAVE-":
            choice = sg.popup_yes_no("Are you sure you want to  save to the Database?", modal=True)
            if choice == "Yes":
                # add_to_database(main_dict, teams, collection)
                add_to_database_cache(changed_players, collection, main_dict, teams)
                changed_players = []
                sg.popup("Uploaded Sucessfully")

            else:
                pass
        if event == "-REMOVE-":
            selected_team = teams.get(values["-TEAM-"][0])
            selected_player_id = selected_team[values["-PLAYERS TABLE-"][0]]
            selected_player_stats = main_dict.get(selected_player_id)
            f_name = selected_player_stats["First_name"]
            l_name = selected_player_stats["Last_name"]
            choice = sg.popup_yes_no("Are you sure you want to  delete "+str(f_name)+" "+str(l_name), modal=True)
            if choice == "Yes":
                print(f_name)
                print(l_name)
                print(selected_player_id)
                print(collection)
                delete_player(selected_player_id, main_dict, teams, collection)
                sg.popup(str(f_name)+" "+str(l_name)+ " was deleted from the Team")
            refresh_teams(team_window, main_dict,teams)


        if event == "-TRADE-":
            manual_trading_window(teams, main_dict, team_list, collection, changed_players)
            refresh_teams(team_window, main_dict, teams)
            team_window.refresh()
        if event == "-LOOK-" and selected_player_id != None and selected_team != None:
            selected_team_number = values["-TEAM-"][0]
            get_trades_dict = get_trades(f_name, l_name, selected_team_number, main_dict, teams)
            best_options_id = get_trades_dict.get("Best Options")
            other_options_id = get_trades_dict.get("Other Options")
            best_options_list = []
            other_options_list = []
            for player1 in best_options_id:
                stats1 = main_dict[player1]
                f_name1 = stats1.get('First_name')
                l_name1 = stats1.get("Last_name")
                dob1 = stats1.get("DOB")
                height1 = int(stats1["Height"])
                shooting1 = int(stats1["Shooting"])
                ball_handling1 = int(stats1["Ball_handling"])
                rebounding1 = int(stats1["Rebounding"])
                defense1 = int(stats1["Defense"])
                total1 = shooting + ball_handling + rebounding + defense
                team1 = get_team(player1, teams)
                best_options_list += [
                    [f_name1, l_name1, dob1, height1, shooting1, ball_handling1, rebounding1, defense1, total1, team1]]
            for player2 in other_options_id:
                stats2 = main_dict[player2]
                f_name2 = stats2.get('First_name')
                l_name2 = stats2.get("Last_name")
                dob2 = stats2.get("DOB")
                height2 = int(stats2["Height"])
                shooting2 = int(stats2["Shooting"])
                ball_handling2 = int(stats2["Ball_handling"])
                rebounding2 = int(stats2["Rebounding"])
                defense2 = int(stats2["Defense"])
                total2 = shooting2 + ball_handling2 + rebounding2 + defense2
                team2 = get_team(player2, teams)
                other_options_list += [
                    [f_name2, l_name2, dob2, height2, shooting2, ball_handling2, rebounding2, defense2, total2, team2]]
            selected_player = display
            team_window["-BEST TRADES-"].update(values=best_options_list)
            team_window["-OTHER TRADES-"].update(values=other_options_list)
            team_window["-BEST OPTIONS TEXT-"].update("Best Trades for  " + selected_player + ":", visible=True)
            team_window["-OTHER OPTIONS TEXT-"].update("Other Trades for  " + selected_player + ":", visible=True)
            team_window["-FINDING TRADES-"].update(visible=True)
        if event == "-TRADE BEST-" and (values["-BEST TRADES-"][0]) != None:
            selected_player_trade_team = best_options_list[values["-BEST TRADES-"][0]][9]
            selected_player_trade_id = best_options_id[values["-BEST TRADES-"][0]]
            teams[selected_player_trade_team].remove(selected_player_trade_id)
            teams[selected_team_number].remove(selected_player_id)
            teams[selected_player_trade_team].append(selected_player_id)
            teams[selected_team_number].append(selected_player_trade_id)
            if selected_player_id not in changed_players:
                changed_players.append((selected_player_id, selected_player_trade_team))
            if selected_player_trade_id not in changed_players:
                changed_players.append((selected_player_trade_id, selected_team_number))
            sg.popup("Trade Complete")
            team_window["-BEST OPTIONS TEXT-"].update("Best Trades for  " + selected_player + ":", visible=False)
            team_window["-OTHER OPTIONS TEXT-"].update("Other Trades for  " + selected_player + ":", visible=False)
            team_window["-FINDING TRADES-"].update(visible=False)
            refresh_teams(team_window, main_dict, teams)
            team_window.refresh()

        if event == "-TRADE OTHER-" and (values["-OTHER TRADES-"][0]) != None:
            selected_player_trade_team = other_options_list[values["-OTHER TRADES-"][0]][9]
            selected_player_trade_id = other_options_id[values["-OTHER TRADES-"][0]]
            teams[selected_player_trade_team].remove(selected_player_trade_id)
            teams[selected_team_number].remove(selected_player_id)
            teams[selected_player_trade_team].append(selected_player_id)
            teams[selected_team_number].append(selected_player_trade_id)
            if selected_player_id not in changed_players:
                changed_players.append((selected_player_id, selected_player_trade_team))
            if selected_player_trade_id not in changed_players:
                changed_players.append((selected_player_trade_id, selected_team_number))
            sg.popup("Trade Complete")
            team_window["-BEST OPTIONS TEXT-"].update("Best Trades for  " + selected_player + ":", visible=False)
            team_window["-OTHER OPTIONS TEXT-"].update("Other Trades for  " + selected_player + ":", visible=False)
            team_window["-FINDING TRADES-"].update(visible=False)
            refresh_teams(team_window, main_dict, teams)
            team_window.refresh()


    # ----Closes Window ---
    team_window.close()

def refresh_teams(team_window, main_dict ,teams):
    team_total_dict = get_team_total(main_dict, teams)
    team_total_list = []

    for team in team_total_dict:
        team_stats = team_total_dict[team]
        team_total_list += [
            [team, team_stats["Total Score"], team_stats["Average Score"], team_stats["Average Height"]]]
    team_window["-TEAM-"].update(values=team_total_list)

def manual_trading_window(teams, main_dict, teams_list, collection, changed_players):
    # players_list =[teams[0]]
    new_team_list = []
    for team in teams_list:
        new_team_list.append(team)

    layout = [
        [
            sg.Text(" Player 1 Team:", font=("Helvetica", 11)),
            sg.Combo(teams_list, key="-CHOSEN TEAM1-", size=(30, 5), enable_events=True),
            sg.Text("Player 1:", font=("Helvetica", 11)),
            sg.Combo(values=[], key="-CHOSEN PLAYER1-", size=(30, 5), enable_events=True)
        ],
        [
            sg.Text("Player 2 Team:", font=("Helvetica", 11)),
            sg.Combo(teams_list, key="-CHOSEN TEAM2-", size=(30, 5), enable_events=True),
            sg.Text("Player 2:", font=("Helvetica", 11)),
            sg.Combo(values=[], key="-CHOSEN PLAYER2-", size=(30, 5), enable_events=True)
        ],
        [
            sg.Button("OK", key="-OK TRADE-")
        ]

    ]
    manual_trade_window = sg.Window("Trading", layout, enable_close_attempted_event=True)
    team1 = 0
    team2 = 0
    player1 = ""
    player2 = ""
    player_list_names = []
    player_list_names2 = []
    while True:
        event, values = manual_trade_window.read()
        if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no(
                'Do you really want to exit?') == 'Yes':
            break
        if event == "-CHOSEN TEAM1-":
            team1 = teams.get(values['-CHOSEN TEAM1-'])
            player_list_names = []
            for id in team1:
                player = main_dict[id]
                f_name = player["First_name"]
                l_name = player["Last_name"]
                player_list_names.append(f_name + "," + l_name)
            manual_trade_window['-CHOSEN PLAYER1-'].update(values=player_list_names)
        if event == "-CHOSEN TEAM2-":
            team2 = teams.get(values['-CHOSEN TEAM2-'])
            player_list_names2 = []
            for id in team2:
                player = main_dict[id]
                f_name = player["First_name"]
                l_name = player["Last_name"]
                player_list_names2.append(f_name + "," + l_name)
            manual_trade_window['-CHOSEN PLAYER2-'].update(values=player_list_names2)
        if event == "-CHOSEN PLAYER1-":
            chosen1 = values["-CHOSEN PLAYER1-"]
            index = player_list_names.index(chosen1)
            player1 = team1[index]
        if event == "-CHOSEN PLAYER2-":
            chosen2 = values["-CHOSEN PLAYER2-"]
            index = player_list_names2.index(chosen2)
            player2 = team2[index]
        if event == "-OK TRADE-" and team1 != None and team2 != None and player1 != None and player2 != None and team1 != team2:
            print(player1, values['-CHOSEN TEAM1-'])
            print(player2, values['-CHOSEN TEAM2-'])
            teams[values['-CHOSEN TEAM1-']].remove(player1)
            teams[values['-CHOSEN TEAM2-']].remove(player2)
            teams[values['-CHOSEN TEAM1-']].append(player2)
            teams[values['-CHOSEN TEAM2-']].append(player1)
            if player1 not in changed_players:
                changed_players.append((player1, values['-CHOSEN TEAM2-']))
            if player2 not in changed_players:
                changed_players.append((player2, values['-CHOSEN TEAM1-']))

            # update_player_col(player1, "Team", values['-CHOSEN TEAM1-'],collection)
            # update_player_col(player2, "Team", values['-CHOSEN TEAM2-'],collection)

            sg.popup("Trade Completed")
            break
        if team1 == None or team2 == None or player1 == None or player2 == None or team1 == team2 and event == "-OK TRADE-":
            sg.popup_ok("Invalid Input!\nMake sure Teams are not the same")
    manual_trade_window.close()


# Main
start_page()
