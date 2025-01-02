import time
import glob
import keyboard
import random
#from intertools import groupby

animation = []
projectile_index = []
bullet_index = []
character_frame = 0
distance = 0
current_jump_height = 0
distance_from_top = 0
lives = 5

character = "Character Art\\Guy.txt"

jump_counter = 0

def intro():
    f = open("Intro_Sequence.txt")
    f_contents = f.read()
    f.close()
    sequence = f_contents.splitlines()
    print("\n\n\n\n")
    for line in sequence:
        print(line)
        print("\n")
        time.sleep(3)

def select_character():
    global character
    print('\nChoose your warrior...\n')
    options = glob.glob('Character Art/*.txt')
    for option in options:
        option = option.replace('.txt', '')
        option = option.replace('Character Art\\', '')
        print(option)
    character = 'Character Art\\' + input('\nEnter character name: ') + '.txt'
    

def fetch_animation_pane():
    f = open("Mountains.txt")
    f_contents = f.read()
    f.close()
    return f_contents.splitlines()

def fetch_character_animation():
    f = open(character)               #fetch the file with the character animation
    f_contents = f.read()
    f.close()
    by_frames = f_contents.split('+')    #turn it into a list of strings, each string being a frame
    guy_animation = []
    for element in by_frames:             #turn each frame string into a list, each list being a list of the rows in the frame
        if element.startswith("\n"):
            element = element[1:]
        guy_animation.append(element.splitlines())
    return guy_animation
    
def fetch_dragon():
    f = open("Dragon.txt")               #fetch the file with the character animation
    f_contents = f.read()
    f.close()
    by_frames = f_contents.split('+')    #turn it into a list of strings, each string being a frame
    dragon_animation = []
    for element in by_frames:             #turn each frame string into a list, each list being a list of the rows in the frame
        if element.startswith("\n"):
            element = element[1:]
        dragon_animation.append(element.splitlines())
    return dragon_animation

def print_animation():
    for line in animation:
        print(line)
    print("")

def add_character():
    global animation
    global character_frame
    global distance_from_top
    
    guy_animation = list(character_animation)
    
    if character_frame < (len(guy_animation) - 1):
        character_frame = character_frame + 1
    else:
        character_frame = 0
        
    frame_lists = guy_animation[character_frame]      #extract the list of rows in the current frame
    
    character_height = len(frame_lists)
    pane_height = len(animation) - 1
    airspace = pane_height - character_height
    
    distance_from_top = airspace - current_jump_height #modifies global variable for use in projectile sensing
    
    add_image(frame_lists, 0, distance_from_top)

def update_character_height():  
    global jump_counter
    global current_jump_height
    
    if jump_counter > 0:     #ascending
        if distance_from_top > 0:
            current_jump_height = current_jump_height + 1
        jump_counter = jump_counter - 1  
        
    elif jump_counter == 0 and current_jump_height == 0:   #on the ground
        current_jump_height = current_jump_height
    elif jump_counter == 0 and current_jump_height > 0:   #descending
        current_jump_height = current_jump_height - 1


def print_heading():
    print("Distance: " + str(distance) + "       " + "Lives: " + str(lives) + "       " + "Dragon: " + str(dragon_states[0]))


def jump():
    global jump_counter
    jump_counter = 5
    
def add_projectiles():
    global projectile_index
    global animation
    global lives
    global dragonstates
    seed = random.randint(1,6)
    if seed == 5:                          #creates a new arrow if the seed is 5
        projectile_index.append([random.randint(0,(len(animation)-4))   ,   len(animation[1])   ,  '<'])
        
    if dragon_states[3] == 'blowing':
        for x in range(41):
            projectile_index.append([dragon_states[0]+7, x, 'C'])
    else:
        for projectile in projectile_index:
            if projectile[2] == 'C':
                projectile_index.remove(projectile)
        
    temp = []                                 #removes duplicates
    for projectile in projectile_index:
        if projectile not in temp:
            temp.append(projectile)
    projectile_index = temp
    
    bullet_index = []                        #creates new index for where the bullets are
    for projectile in projectile_index:
        if projectile[2] == '=':
            new_entry = [projectile[0], projectile[1]]
            bullet_index.append(new_entry)
    
    for projectile in projectile_index:
        row = projectile[0]
        column = projectile[1]
        if projectile[2] == '<':           #for arrows   
            if column <= 2:                 #deletes them at the end of the screen
                projectile_index.remove(projectile)
            if column <= len(character_animation[0][0]):  #checks the arrow for contact
                if (row >= distance_from_top) and (row < (distance_from_top + len(character_animation[0]))):
                    lives = lives - 1
                    try:
                        projectile_index.remove(projectile)
                    except:
                        print("that thing happened")
            for bullet in bullet_index:   #checks the arrow for a collision
                if row == bullet[0] and column <= bullet[1] + 1:
                    try:
                        projectile_index.remove(projectile)
                    except:
                        print("that thing happened")
                    for possible_same_line_bullet in projectile_index:
                        if possible_same_line_bullet[0] == row and possible_same_line_bullet[2] == "=":
                            projectile_index.remove(possible_same_line_bullet)
                            break
            projectile[1] = projectile[1] - 1    #advances the arrow one space
        
        if projectile[2] == '=':   #for bullets
            projectile[1] = projectile[1] + 1
            if column >= len(animation[0]):                 #deletes them at the end of the screen
                projectile_index.remove(projectile)
        
        if projectile[2] == 'C':   #for fire
            if column <= len(character_animation[0][0]):  #checks fire for contact
                if (row >= distance_from_top) and (row < (distance_from_top + len(character_animation[0]))):
                    lives = lives - 1  
              
        #generic printing of each projetile
        animation[row] = animation[row][0:(column-1)] + projectile[2] + animation[row][column:len(animation[1])]

                
def shoot():
    global projectile_index
    possible_bullet = [distance_from_top, 5, '=']
    projectile_index.append(possible_bullet)
    
    

def starting_art():
    f = open("Starting art.txt")               #fetch the file with the character animation
    f_contents = f.read()
    f.close()
    print(f_contents)

def end_game():
    input("\n Press enter to play again ")
    reset_game()


def reset_game():
    global distance
    global lives
    global current_jump_height
    global projectile_index
    global dragon_states
    distance = 0
    lives = 5
    current_jump_height = 0
    projectile_index.clear()
    dragon_states = [-15, 'falling', 5, 'flying', 10]

def create_frame():
    global distance
    scene = list(background)
    frame = []
    start = distance / 10
    end = start + 80
    for line in scene:
        needed_portion = line[int(start):int(end)]
        frame.append(needed_portion)
    return frame

def add_dragon():
    global animation
    global dragon_animation
    ycoord = update_dragon_height()
    dragon_frames = list(dragon_animation)
    if dragon_states[3] == 'flying':
        frame = (distance % 4)
        add_image(dragon_frames[frame], 30, ycoord)
    elif dragon_states[3] == 'blowing':
        add_image(dragon_frames[4], 30, ycoord)
    
def update_dragon_height():
    global dragon_height
    global distance
    global dragon_states
    
    if distance < 10:
        return 0
    elif(distance < 25):
        return -(distance - 10)
    elif(dragon_states[3] == 'flying'):
        if(dragon_states[1] == 'falling'):
            dragon_states[0] += 1
            if dragon_states[0] >= dragon_states[2]:
                dragon_states[1] = 'rising'
                dragon_states[3] = 'blowing'
        if(dragon_states[1] == 'rising'):
            dragon_states[0] += -1
            if dragon_states[0] == -len(dragon_animation[1]):
                dragon_states[1] = 'falling'
                dragon_states[2] = random.randint(0, int(len(dragon_animation[1]) / 2))
        return dragon_states[0]
    elif(dragon_states[3] == 'blowing'):
        dragon_states[4] -= 1
        if dragon_states[4] == 0:
            dragon_states[4] = 10
            dragon_states[3] = 'flying'
        return dragon_states[0]
        
    

def add_image(image, xcoord, ycoord):
    global animation
    for line in image:
        if ((ycoord + image.index(line)) >= 0) and ((ycoord + image.index(line)) <= (len(animation) - 1)):
            animation_line = animation[ycoord + image.index(line)]
            line_length = len(line)
            leading_space = len(line) - len(line.lstrip())
            trailing_space = len(line) - len(line.rstrip())
            addition_length = len(line.strip())
            addition = line.strip()
            addition_start_point = xcoord + leading_space
            addition_end_point = xcoord + leading_space + addition_length
            animation[ycoord + image.index(line)] = animation_line[0:addition_start_point] + addition + animation_line[addition_end_point:]

    
        
        
dragon_states = [-15, 'falling', 5, 'flying', 10] 
#dragon's y coordinate, whether rising or falling, target y coordinate, flying or blowing, stagnation counter

intro()
starting_art()

select_character()

background = tuple(fetch_animation_pane())
character_animation = tuple(fetch_character_animation())
dragon_animation = tuple(fetch_dragon())

keyboard.add_hotkey('space', jump)   #set up the spacebar as a jumping hotkey
keyboard.add_hotkey('ctrl', shoot)

while True:
    animation = create_frame()
    update_character_height()
    
    add_character()
    add_projectiles()
    add_dragon()
    
    print_heading()
    print_animation()
    
    if lives <= 0:
        end_game()
    
    time.sleep(0.25)
    distance = distance + 2


