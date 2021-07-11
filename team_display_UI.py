import PySimpleGUI as sg
from database import *
from main import get_teams_db
from startPageUI import *



def team_display_UI(collection):
    team_list, teams, main_dict = get_teams_db(collection)
    w, h = sg.Window.get_screen_size()
    teams_display = [
        [
            sg.Text(("Teams in " + collection),font=("Helvetica", 25),enable_events=True, key="-SEASON-")
        ],
        [
            sg.Listbox(
                values=team_list,font=("Helvetica", 12), enable_events=True, size=(60, 30), key="-TEAM-"
            )
        ],
    ]
    right_column = [[sg.Text("Players on Selected Team: ",font=("Helvetica", 25))],
                    [sg.Listbox(values=[],font=("Helvetica", 12), visible= True, enable_events=True, size=(60, 30), key="-PLAYERS-")]

    ]
    teams_layout = [ [sg.Button("Back",font=("Helvetica", 12), enable_events=True, key = "-BACK-")],
        [
            sg.Column(teams_display),
            sg.VSeperator(),
            sg.Column(right_column),
        ]
    ]

    team_display = sg.Window("Current Teams", teams_layout, enable_close_attempted_event=True, size=(w,h))
    while True:
        event, values = team_display.read()
        if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no(
                'Do you really want to exit?') == 'Yes':
            break
        if event == "-BACK-":
            team_display.close()

            break



        if event == "-TEAM-":
            players_id = teams[values["-TEAM-"][0]]
            players= []
            for id in players_id:
                player= main_dict[id]
                f_name = player["First_name"]
                l_name = player["Last_name"]
                dob = player["DOB"]
                height = player["Height"]
                shooting = player["Shooting"]
                ball_handling = player["Ball_handling"]
                rebounding = player["Rebounding"]
                defense = player["Defense"]
                total = player["Total"]
                players.append(f_name + " " + l_name)
            choosen_team = values["-TEAM-"][0]
            team_display['-PLAYERS-'].update(values =players)

    # ----Closes Window ---
    team_display.close()

#def player_window(team):
