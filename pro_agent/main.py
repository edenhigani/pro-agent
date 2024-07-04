import pandas as pd
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

master = Tk()
# declaring string variable
# for storing name and password
first_name_var = StringVar()
last_vame_var = StringVar()
selected_option_var = StringVar()
last_row = 5
master.title("Football Agent")

teams = pd.read_csv('teams.csv', encoding='latin-1', error_bad_lines=False)
players = pd.read_csv('players.csv', encoding='latin-1', error_bad_lines=False)

# Save data for each player
class Player:
    def __init__(self, name, team, player_number, grade):
        self.name = name
        self.team = team
        self.player_number = player_number
        self.grade = grade
        self.level = ""
        self.level_num = 0

# Save data for each team
class Team:
    def __init__(self, name, league, rank, level):
        self.name = name
        self.league = league
        self.rank = rank
        self.level = level


# Percentile
TOP_FIRST_LEAGUE = 90
ALMOST_TOP_FIRST_LEAGUE = 83
MID_FIRST_LEAGUE = 75
ALMOST_MID_FIRST_LEAGUE = 68
LOW_FIRST_LEAGUE = 60

ALMOST_FIRST_LEAGUE = 50

TOP_SECOND_LEAGUE = 30
ALMOST_TOP_SECOND_LEAGUE = 20
LOW_SECOND_LEAGUE = 15

# Calculate percentile and save description for each player in list
def calc_percentile(grades_list, players_list):
    for player in players_list:
        if player.grade >= np.percentile(grades_list, TOP_FIRST_LEAGUE):
            player.level = "Top First League"
            player.level_num = 1
            continue
        if player.grade >= np.percentile(grades_list, ALMOST_TOP_FIRST_LEAGUE):
            player.level = "Almost Top First League"
            player.level_num = 1.5
            continue
        if player.grade >= np.percentile(grades_list, MID_FIRST_LEAGUE):
            player.level = "Mid First League"
            player.level_num = 2
            continue
        if player.grade >= np.percentile(grades_list, ALMOST_MID_FIRST_LEAGUE):
            player.level = "Almost Mid First League"
            player.level_num = 2.5
            continue
        if player.grade >= np.percentile(grades_list, LOW_FIRST_LEAGUE):
            player.level = "Low First League"
            player.level_num = 3
            continue

        if player.grade >= np.percentile(grades_list, ALMOST_FIRST_LEAGUE):
            player.level = "Almost First League"
            player.level_num = 3.5
            continue
        if player.grade >= np.percentile(grades_list, TOP_SECOND_LEAGUE):
            player.level = "Top Second League"
            player.level_num = 4
            continue
        if player.grade >= np.percentile(grades_list, ALMOST_TOP_SECOND_LEAGUE):
            player.level = "Almost Top Second League"
            player.level_num = 4.5
            continue
        if player.grade >= np.percentile(grades_list, LOW_SECOND_LEAGUE):
            player.level = "Low Second League"
            player.level_num = 5
            continue
        player.level = "Check Third League"
        player.level_num = 5.5

# Calculate grade for each player according to his position
def calculate_grades(factor_dict, players_details):
    grades_list = []
    players_position_list = []
    for index, player in players_details.iterrows():
        team_name = player['Team']
        team_details = teams.loc[teams['Name'] == team_name]
        grade = factor_dict['minutes'] * player['Minutes'] \
                + factor_dict['player_goals'] * player['Goals'] \
                + factor_dict['assists'] * player['Assists']  # PLAYER params
        grade += factor_dict['on_target'] * player['On Target'] \
                 + factor_dict['tackles'] * player['Tackles'] \
                 - factor_dict['lost_ball'] * player['Lost Ball']  # PLAYER params
        grade += factor_dict['team_goals'] * team_details['Goals'] \
                 - factor_dict['against'] * team_details['Against']  # TEAM params

        # TEAM BONUS
        league = team_details['League'].values[0]
        rank = team_details['Rank'].values[0]
        bonus = add_team_bonus(league, rank)

        # Calculate Final Grade
        final_grade = bonus * grade.values[0]
        player_details_and_grade = Player(player['Full Name'], player['Team'], player['Number'], final_grade)
        grades_list.append(final_grade)
        players_position_list.append(player_details_and_grade)
    calc_percentile(grades_list, players_position_list)
    return players_position_list


# Split calculation according to positions

# Position--> Defenders
def calc_defenders_grades():
    position = "defenseman"
    defenders_factor_dict = {}
    defenders_factor_dict["minutes"] = 3
    defenders_factor_dict["player_goals"] = 15
    defenders_factor_dict["assists"] = 10
    defenders_factor_dict["on_target"] = 1
    defenders_factor_dict["tackles"] = 3
    defenders_factor_dict["lost_ball"] = 5
    defenders_factor_dict["team_goals"] = 1
    defenders_factor_dict["against"] = 5

    defenders_players_details = players.loc[players["Position"] == position]

    defenders_list = calculate_grades(defenders_factor_dict, defenders_players_details)
    return defenders_list

# Position--> midfielder
def calc_mid_grades():
    position = "mid-fielder"
    mid_factor_dict = {}
    mid_factor_dict["minutes"] = 3
    mid_factor_dict["player_goals"] = 20
    mid_factor_dict["assists"] = 15
    mid_factor_dict["on_target"] = 1
    mid_factor_dict["tackles"] = 3
    mid_factor_dict["lost_ball"] = 3
    mid_factor_dict["team_goals"] = 3
    mid_factor_dict["against"] = 2
    mid_players_details = players.loc[players["Position"] == position]

    mid_list = calculate_grades(mid_factor_dict, mid_players_details)
    return mid_list

# Position--> forward
def calc_forward_grades():
    position = "forward"
    forward_factor_dict = {}
    forward_factor_dict["minutes"] = 3
    forward_factor_dict["player_goals"] = 15
    forward_factor_dict["assists"] = 10
    forward_factor_dict["on_target"] = 1
    forward_factor_dict["tackles"] = 3
    forward_factor_dict["lost_ball"] = 5
    forward_factor_dict["team_goals"] = 10
    forward_factor_dict["against"] = 5
    forward_players_details = players.loc[players["Position"] == position]

    forward_list = calculate_grades(forward_factor_dict, forward_players_details)
    return forward_list

# Position--> goalkeeper
def calc_goalie_grades():
    position = "goalie"
    goalie_factor_dict = {}
    goalie_factor_dict["minutes"] = 3
    goalie_factor_dict["player_goals"] = 5
    goalie_factor_dict["assists"] = 5
    goalie_factor_dict["on_target"] = 1
    goalie_factor_dict["tackles"] = 10
    goalie_factor_dict["lost_ball"] = 10
    goalie_factor_dict["team_goals"] = 5
    goalie_factor_dict["against"] = 15

    goalie_players_details = players.loc[players["Position"] == position]

    goalie_list = calculate_grades(goalie_factor_dict, goalie_players_details)

    return goalie_list


# Get league and rank. Calculate bonus
def add_team_bonus(league, rank):
    league_bonus = 1
    rank_bonus = 16 - rank
    if league == 'First League':
        league_bonus += 12
        rank_bonus += 5

    bonus = 2 * league_bonus + rank_bonus
    return bonus

# Calculate level for each team (according to league and rank in league)
def calc_teams_levels():
    teams_levels_dict = {1: [], 2: [], 3: [], 4: [], 5: []}
    for index, team in teams.iterrows():
        if team['League'] == 'First League':
            rank = team['Rank']
            if rank <= 4:
                level = 1
            else:
                if rank <= 9:
                    level = 2
                else:
                    level = 3
        else:  # Second League
            rank = team['Rank']
            if rank <= 8:
                level = 4
            else:
                level = 5
        team_obj = Team(team['Name'], team['League'], team['Rank'], level)
        teams_levels_dict[level].append(team_obj)

    return teams_levels_dict

# Print relevant teams for player (according to his grade)
def print_relevant_teams(player):
    lst = []
    player_level_num = player.level_num
    if isinstance(player_level_num, int):
        for team in teams_levels_dict[player_level_num]:
            lst.append(team.name)
    else:
        lower_level = player_level_num + 0.5
        higher_level = player_level_num - 0.5
        for team in teams_levels_dict[higher_level]:
            lst.append(team.name)
        teams
        if lower_level < 6:  # There are no teams to offer in level 6
            for team in teams_levels_dict[lower_level]:
                lst.append(team.name)
    return lst


# If there are two players or more with the same name--> Choose the relevant player
def choose_player(players):
    global last_row
    global options
    for widgets in master.winfo_children():
        widgets.destroy()
    image = Image.open("pro agent.png")
    image = image.resize((450, 350), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)

    img_label = Label(master, image=photo, anchor=CENTER)
    img_label.image = photo
    clear_btn = Button(master, text="Clear", command=clear_data, bg='#BD2525', fg='white')
    select_option_input = Entry(master, textvariable=selected_option_var)
    select_option_btn = Button(master, text="Select Option", command=select_option, bg='#BD2525', fg='white')

    # GRID
    img_label.grid(row=1, column=1)
    clear_btn.grid(row=5, column=1, sticky=W, pady=2)
    Label(master, text='Options', fg='red').grid(row=6, column=1, pady=10)
    idx = 1
    options = []
    for index, player in players.iterrows():
        player_option = str(idx) + "\t" + str(player['Full Name']) + "\t" + str(player['Team']) + "\t" + str(player['Number'])
        options.append(player_option)
        idx += 1
    for row in range(len(options)):
        Label(master, text=options[row]).grid(row=7+row, column=1, pady=10)
        last_row = 8 + row
    Label(master, text='Select option').grid(row=last_row)
    select_option_input.grid(row=last_row, column=1, sticky=W, pady=2)
    select_option_btn.grid(row=last_row+1, column=1, sticky=W, pady=2)
    last_row += 2




# If there are two players or more with the same name--> Choose the relevant player
def select_option():
    selected_player_option = selected_option_var.get()
    if(int(selected_player_option) > len(options)) or (int(selected_player_option) < 1):
        return
    selected_player = options[int(selected_player_option)-1].split('\t')
    player_name = selected_player[1]
    team = selected_player[2]
    number = selected_player[3]
    player_details = players.loc[((players['Team'] == team) & (players['Number'] == int(number)))]
    if player_details.Position.values[0] == "goalie":
        goalie_list.sort(key=lambda x: x.grade, reverse=True)
        relevant_list = goalie_list
    else:
        if player_details.Position.values[0] == "forward":
            forward_list.sort(key=lambda x: x.grade, reverse=True)
            relevant_list = forward_list
        else:
            if player_details.Position.values[0] == "mid-fielder":
                mid_list.sort(key=lambda x: x.grade, reverse=True)
                relevant_list = mid_list
            else:
                if player_details.Position.values[0] == "defenseman":
                    defenders_list.sort(key=lambda x: x.grade, reverse=True)
                    relevant_list = defenders_list

    for player in relevant_list:
        if player.name == player_name and (player_details['Number'] == player.player_number).values[0] and \
                (player_details['Team'] == player.team).values[0]:
            save_player = player


    lst = print_relevant_teams(save_player)
    i = 0

    for x in lst:
        Label(master, text=x).grid(row=last_row + i, column=1)
        i += 1


# Decision tree- get name of player and print the relevant teams for this player
def decision_tree(player_name):
    player_details = players.loc[players['Full Name'] == player_name]
    if len(player_details) > 1:
        choose_player(player_details)  # There are two players of more with the same name
        return
    if len(player_details) == 0:  # No player found
        return
    # Check position of player
    if player_details.Position.values[0] == "goalie":
        goalie_list.sort(key=lambda x: x.grade, reverse=True)
        relevant_list = goalie_list
    else:
        if player_details.Position.values[0] == "forward":
            forward_list.sort(key=lambda x: x.grade, reverse=True)
            relevant_list = forward_list
        else:
            if player_details.Position.values[0] == "mid-fielder":
                mid_list.sort(key=lambda x: x.grade, reverse=True)
                relevant_list = mid_list
            else:
                if player_details.Position.values[0] == "defenseman":
                    defenders_list.sort(key=lambda x: x.grade, reverse=True)
                    relevant_list = defenders_list


    for player in relevant_list:
        if player.name == player_name and (player_details['Number'] == player.player_number).values[0] and (player_details['Team'] == player.team).values[0]:
            save_player = player

    # return list of teams
    lst = print_relevant_teams(save_player)
    return lst




# Calculate grades for each player
defenders_list = calc_defenders_grades()
mid_list = calc_mid_grades()
forward_list = calc_forward_grades()
goalie_list = calc_goalie_grades()

# Calculate ranks for each team
teams_levels_dict = calc_teams_levels()


# Display list of teams on screen
def find_teams():
    global teams_list
    first_name = first_name_var.get()
    last_name = last_vame_var.get()

    player_name = first_name + ' ' + last_name
    teams_list = decision_tree(player_name)


    i=0
    if teams_list is None:
        return
    for x in teams_list:
        Label(master, text=x).grid(row=5+i, column=1)
        i += 1

# Clear data in screen (clear button)
def clear_data():
   first_name_var.set('')
   last_vame_var.set('')
   for widgets in master.winfo_children():
      widgets.destroy()
   image = Image.open("pro agent.png")
   image = image.resize((450, 350), Image.ANTIALIAS)
   photo = ImageTk.PhotoImage(image)

   img_label = Label(master, image=photo, anchor=CENTER)
   img_label.image = photo
   first_name_input = Entry(master, textvariable=first_name_var)
   last_name_input = Entry(master, textvariable=last_vame_var)
   find_teams_btn = Button(master, text="Find Teams", command=find_teams, bg='#BD2525', fg='white')
   clear_btn = Button(master, text="Clear", command=clear_data, bg='#BD2525', fg='white')

   # GRID
   Label(master, text='First Name').grid(row=2)
   Label(master, text='Last Name').grid(row=3)
   img_label.grid(row=1, column=1)
   first_name_input.grid(row=2, column=1, sticky=W, pady=2)
   last_name_input.grid(row=3, column=1, sticky=W, pady=2)
   find_teams_btn.grid(row=4, column=1, sticky=W, pady=10)
   clear_btn.grid(row=5, column=1, sticky=W, pady=2)



image = Image.open("pro agent.png")
image = image.resize((450, 350), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)


img_label = Label(master, image=photo, anchor=CENTER)
img_label.image = photo
first_name_input = Entry(master, textvariable=first_name_var)
last_name_input = Entry(master, textvariable=last_vame_var)
find_teams_btn = Button(master, text="Find Teams", command=find_teams, bg='#BD2525', fg='white')
clear_btn = Button(master, text="Clear", command=clear_data, bg='#BD2525', fg='white')
selected_option = Entry(master, textvariable=selected_option_var)

# GRID
Label(master, text='First Name').grid(row=2)
Label(master, text='Last Name').grid(row=3)
img_label.grid(row=1, column=1)
first_name_input.grid(row=2, column=1, sticky=W, pady=2)
last_name_input.grid(row=3, column=1, sticky=W, pady=2)
find_teams_btn.grid(row=4, column=1, sticky=W, pady=10)
clear_btn.grid(row=5, column=1, sticky=W, pady=2)


master.mainloop()
