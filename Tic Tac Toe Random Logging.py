#the current state of played xes and os in the game
import sys
import random
import pandas as pd
from datetime import datetime


current_board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]

pick_coordinate = 0

game_data = {} #keys are the computer's turn number, followed by the gameboard, 
                #the decision, whether playing x or o, and the timestamp
turn_number = 0
winner = ""

winning_combos = [[0,1,2],
                  [3,4,5],
                  [6,7,8],
                  [0,3,6],
                  [1,4,7],
                  [2,5,8],
                  [0,4,8],
                  [2,4,6]]

def display():
    print(current_board[0], current_board[1], current_board[2])
    print(current_board[3], current_board[4], current_board[5])
    print(current_board[6], current_board[7], current_board[8])
    
def human_turn(x_or_o):
    pick = input('Pick a spot to play (ex. "top right") ')
    pick.lower()
    pick_coordinate = (0 if pick.startswith("top") else 3 if 
        pick.startswith("middle" or "center") else 6 if 
        pick.startswith("bottom") else 0)
    pick_coordinate = pick_coordinate + (0 if pick.endswith("left") else 1 if 
        pick.endswith("middle" or "center") else 2 if 
        pick.endswith("right") else 0)
    
    if pick.startswith("end"):
        sys.exit()
    
    if current_board[pick_coordinate] == "-":
        current_board[pick_coordinate] = x_or_o
    
def my_turn_random(x_or_o):
    global turn_number
    while True:
        my_pick = random.randint(0, 8)
        if current_board[my_pick] == "-":
            break #once the computer has picked a valid spot
    timestamp = datetime.now()
    entry = current_board + [my_pick] + [x_or_o] + ["in progress"] + [timestamp]
    game_data[turn_number] = entry
    turn_number = turn_number + 1
    current_board[my_pick] = x_or_o;
    
def my_turn_smart(x_or_o):
    global turn_number
    global current_board
    df = pd.read_csv("tic tac toe insights.csv", index_col=0)
    
    data_dictionary = df.to_dict(orient="index")
    #produces a dictionary with the insights gameboards as keys with an entry that is a
    #dictionary that uses the different choices as keys
    
    generic_current_board = current_board
    for i in range(len(generic_current_board)): #convert to a generic form
        if generic_current_board[i] == x_or_o:
            generic_current_board[i] = "M"
        elif generic_current_board[i] == ("X" if x_or_o=="O" else "O" if x_or_o=="X" else "-"):
            generic_current_board[i] = "Y"
    
    if str(generic_current_board) in data_dictionary:
        situation_study = data_dictionary[str(generic_current_board)]
        print(situation_study)
        my_pick = insightful_decision(situation_study)
    else: #new situation, guess randomly
        while True:
            my_pick = random.randint(0, 8)
            if current_board[my_pick] == "-":
                break #once the computer has picked a valid spot
    
    for i in range(9): #convert back to specific form, not sure why I need to
        if current_board[i] == "M":
            current_board[i] = x_or_o
        elif current_board[i] == "Y":
            current_board[i] = ("X" if x_or_o=="O" else "O" if x_or_o=="X" else "-")
    
    timestamp = datetime.now()
    entry = current_board + [my_pick] + [x_or_o] + ["in progress"] + [timestamp]
    game_data[turn_number] = entry
    turn_number = turn_number + 1
    current_board[my_pick] = x_or_o;
    
    input("Hit Enter ")
   
def insightful_decision(situation_study):
    choice_list = []
    choice_weights = []
    for choice in situation_study:
        if situation_study[choice] != None:
            choice_list = choice_list + [choice]
            print(situation_study[choice])
            weight = situation_study[choice][1] #still don't know what's goint on here
            print(weight)
            #choice_weights = choice_weights + [weight]
            
    print(choice_list, choice_weights)
    input("Hit Enter ")
        
    
            
def check_for_win(): #also checks for a tie
    global winner
    for combo in winning_combos:
        if (current_board[combo[0]] == current_board[combo[1]] == current_board[combo[2]] != "-"):
            print("GAME OVER")
            winner = current_board[combo[0]] #returns the character of who won
            print("Winner: ", winner)
            print("Winning combo: ", combo)
            return True
    if "-" not in current_board:
        winner = "tie"
        print("Winner: ", winner)
        return True
    return False

def log_game():
    for turn in game_data: #this reformats all of the log data to be more generic, so it can be used by either x or o
        player_letter = game_data[turn][10]
        if winner == player_letter:
            game_data[turn][11] = "won"
        elif winner == "tie":
            game_data[turn][11] = "lost" #for now let's teach it to win
        else:
            game_data[turn][11] = "lost"
        del game_data[turn][10]
        for i in range(9):
            j = game_data[turn][i]
            if j == player_letter:
                game_data[turn][i] = "M" # M is mine
            elif j != "-":
                game_data[turn][i] = "Y" # Y is yours
        
    df = pd.DataFrame(game_data).T #creates and inverts the dataframe object to send
    df.to_csv("tic tac toe experience.csv", mode="a", header=False, index=False)
            

def generate_insights():
    
    insights = {}

    df = pd.read_csv("tic tac toe experience.csv")

    data_dictionary = df.to_dict(orient="split")
    data = data_dictionary["data"] #ends up with a list of lists of the actual data

    for turn in data:
        gameboard = str(turn[0:9]) #string of the gameboard
        gameboard_list = turn[0:9]
        decision = turn[9] #the number of the spot that was chosen
        won = "won" in turn #becomes true if it was a "won" log entry
        if gameboard in insights:
            #this gameboard has been seen before
            previous_stats = insights[gameboard][decision] #the previous stats for that decision
            new_number_of_instances = previous_stats[0] + 1
            new_percent_victory = ((((0 if previous_stats[1] == None else previous_stats[1]) * previous_stats[0]) + 
                                    (1 if won else 0)) / new_number_of_instances)
            insights[gameboard][decision] = [new_number_of_instances, new_percent_victory]
        else:
            #conrgrats! this board setup has never been seen before
            #let's study it
            new_insight = {0:[0, None],1:[0, None],2:[0, None],3:[0, None],
                           4:[0, None],5:[0, None],6:[0, None],7:[0, None],
                           8:[0, None]}
            
            for position in range(9): #deletes data entry spaces for choices it can't make
                if gameboard_list[position] != "-":
                    del(new_insight[position])
                    
            new_insight[decision] = [1, 1 if won else 0] #adds that data point
    
            insights[gameboard] = new_insight #publishes the new insight to the insights list

    print("insights generated")
    insights_dataframe = pd.DataFrame(data=insights).T
    insights_dataframe.to_csv("tic tac toe insights.csv")
    
def reset_game():
    global current_board
    global pick_coordinate
    global game_data
    global turn_number
    global winner
    
    current_board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
    pick_coordinate = 0
    game_data = {} #keys are the computer's turn number, followed by the gameboard and each decision
    turn_number = 0
    winner = ""
    

print("WELCOME TO TIC TAC TOE")

input("Ready to start? Hit Enter to begin... ")

display()

for i in range(10):
    while True:
        my_turn_random("X")
        display()
        if check_for_win():
            log_game()
            generate_insights()
            reset_game()
            break
            
        my_turn_random("O")
        display()
        if check_for_win():
            log_game()
            generate_insights()
            reset_game()
            break

sys.exit()
    
    
            
             