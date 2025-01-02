#the current state of played xes and os in the game
import sys
import random

current_board = [[" ", " ", " "], 
                 [" ", " ", " "], 
                 [" ", " ", " "]]

pick_coordinate = [0, 0]

winning_combos = [[[0,0],[0,1],[0,2]], #rows
                  [[1,0],[1,1],[1,2]],
                  [[2,0],[2,1],[2,2]],
                  [[0,0],[1,0],[2,0]], #columns
                  [[0,1],[0,1],[0,1]],
                  [[0,2],[0,2],[0,2]],
                  [[0,0],[1,1],[2,2]], #diagonals
                  [[0,2],[1,1],[2,0]]]


def display():
    for line in current_board:
        print(line)
    
def get_pick_new():
    pick = input('Pick a spot to play (ex. "top right") ')
    pick.lower()
    pick_coordinate[0] = (0 if pick.startswith("top") else 1 if 
        pick.startswith("middle" or "center") else 2 if 
        pick.startswith("bottom") else 0)
    pick_coordinate[1] = (0 if pick.endswith("left") else 1 if 
        pick.endswith("middle" or "center") else 2 if 
        pick.endswith("right") else 0)
    
    if pick.startswith("end"):
        sys.exit()
    
    current_board[pick_coordinate[0]][pick_coordinate[1]] = "X";
    
def my_turn():
    while True:
        my_pick = [random.randint(0, 2), random.randint(0, 2)]
        if current_board[my_pick[0]][my_pick[1]] == " ":
            current_board[my_pick[0]][my_pick[1]] = "O";
            break #only leave the loop once the computer has played
            
def check_for_win(): #also checks for a tie
    for combo in winning_combos:
        if (current_board[combo[0][0]][combo[0][1]] == current_board[combo[1][0]][combo[1][1]] and
            current_board[combo[0][0]][combo[0][1]] == current_board[combo[2][0]][combo[2][1]] and
            current_board[combo[0][0]][combo[0][1]] != " "):
            print("GAME OVER")
            print(combo)
            sys.exit()
            
            #to do figure out why this is getting tripped when it shouldn't be
    

print("WELCOME TO TIC TAC TOE")

input("Ready to start? Hit Enter to begin... ")

display()

while True:
    get_pick_new()
    my_turn()
    check_for_win()
    display()
    
            
             