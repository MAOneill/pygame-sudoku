import pygame
import random 

#note - I started prefixing all function scoped variables with an 'f'

#this includes the strings to draw a custom cursor that kind of looks like a pencil
from pencil_strings import pencil_strings

#this is the functiont that can read in the raw board settings
#raw board is an array of 9 arrays with 9 tuples each

myrandom = random.randint(1, 5)   
#this works...but some of the documentation says not to use it....
exec('from board%d_raw import rawboard' % myrandom)

class Tcell():
    def __init__(self,tinycell,x,y):
        self.set = False
        self.image = pygame.image.load('numbers/pencil_blank_diff.png' ).convert_alpha()
        self.xpos = x + ((tinycell-1) % 3) * 27
        self.ypos = y + ((tinycell-1) // 3) * 27
        self.number = tinycell
    def update_pencil_image(self):
        if self.set == True:
            # print("the pencil cell is %d" % self.number)
            self.image = pygame.image.load('numbers/%d_pencil_diff.png' % self.number).convert_alpha()
        else:  #use blank
            self.image = pygame.image.load('numbers/pencil_blank_diff.png' ).convert_alpha()

class Cell():
    #define the playing cell.  there are 81 of these in an 9x9 soduko board
    def __init__(self,row,col,value,answer=None):
        # self.start = value  #or is this in the subclass...
        self.row = row
        self.col = col
        #  self.inner = 0  #compute thie
        # self.pencils = {}  #{} will object create this and set here

        self.guess = None       #blank to start
        self.value = value      #given in start cube
        self.answer = answer    #if loaded in answers, used for hints

        self.name = "r%dc%d" % (row,col)

        rowbox = int((row-1)//3)
        colbox = int((col-1)//3)
        self.inner = (rowbox *3 )+ colbox+ 1

        self.x_position = (col-1) * 81
        self.y_position = (row-1) * 81    

        #you can only change the image for an unknown cell or blank:
    def change_cell_image(self):
        pass

class Known_cell(Cell):
    def __init__(self,row,col,value,answer):
        super().__init__(row,col,value,answer)
        self.answer = answer  
        #known cells don't need pencils or possibles
        # self.possibles = {}  #empty    
        self.image = pygame.image.load('numbers/%d_background_transparent.png' % answer).convert_alpha()
        # self.image = pygame.image.load('numbers/%d_transparent_number.png' % value).convert_alpha()
    
class Unknown_cell(Cell):
    def __init__(self,row,col,value,answer=None):
        super().__init__(row,col,value,answer)
        self.answer = answer
        self.value = 0
        self.pencils ={}
        for tinycell in range(1,10):
            self.pencils[tinycell] = Tcell(tinycell,self.x_position,self.y_position)
        #change this to a null image
        self.image = None
    def change_cell_image(self):
        # print(self.guess)
        #changes the display image based on the GUESS value
        if self.guess == None or self.guess == 0:
            self.image = None       #undo can set it back to zero
        else:
            self.image = pygame.image.load('numbers/%d_guess.png' % self.guess).convert_alpha()

class Blank_cell(Cell):
    #used in the SOLVING part of the program, not the game play
    #.value is the STARTING value.  .guess is the computed answer
    #.answer - holds BOTH - either starting and/or value
    def __init__(self,row,col,value=None,answer=None):
        super().__init__(row,col,value,answer)
        self.guess = None
        self.possibles = {1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9}
        # self.possibles = {}
        self.image = None
    def change_cell_image(self):
    #changes the display image based on the "value"
    # if answer not none, use that.  otherwise, use value:
        if self.value == None and self.guess == None:
            self.image = None       #undo can set it back to zero
        elif self.guess != 0 and self.guess != None:
            self.image = pygame.image.load('numbers/%d_guess.png' % self.guess).convert_alpha()
        else:  #value is not none
            self.image = pygame.image.load('numbers/%d_background_transparent.png' % self.value).convert_alpha()
    def solve_clear_possibles(self):
    # based on the known values/guesses (which are both stored in answers)
    # remove the appropriate key in possibles
    # every cell begins with all 9 possibles.
        if self.answer != None:
            self.possibles ={}  #there are no possibles if known
        
def create_cell(row,col,tuple,known):
    #process to create all 81 objects AND load them into an array
    #I didn't not put this inside a function because I need the individual
    #objects accessable by their name

    newcell = {}
    if known:       #known is true
        newcell = Known_cell(row,col,tuple[0],tuple[1]) #all named 'newcell'
    else:
        newcell = Unknown_cell(row,col,tuple[0],tuple[1]) #all named 'newcell'
    return newcell     #this points to entirely new spot each time

def create_board(input_board):
    # returns an array of all 81 cells, NOT IN ROWS
    allcells = {}  #dictionary not array
    cell = {}    
    row = 0
    for eachrow in input_board:
        row += 1    #increment the row counter
        rowarray = []   #create a new instance here
        col = 0 
        for eachtuple in eachrow:
            col += 1
            
            #if the first value is KNOWN, then create a Known_cell class
            #otherwise create an Unknown_cell class        
            if eachtuple[0] == 0:  #unknown
                known = False  
            else:
                known = True
            
            cellname = "r%dc%d" % (row,col)
            # print(cellname)
            allcells[cellname] = create_cell(row,col,eachtuple,known)
            # print(cell['data'].value)
            # allcells.append(cell)   #append my object into the row array
    return allcells

def create_blank_board():
    #this is used for the solving side of the game
    # returns an array of all 81 cells, NOT IN ROWS
    allcells = {}  #dictionary not array
    cell = {}    
    for r in range(1,10) : 
        for c in range(1,10):
            cellname = "r%dc%d" % (r,c)
            allcells[cellname] = Blank_cell(r,c)
    return allcells

row1 = '061007003'
row2 = '092003000'
row3 = '000000000'
row4 = '008530000'
row5 = '000000504'
row6 = '500008000'
row7 = '040000001'
row8 = '000160800'
row9 = '600000000'

# row1 = '000000680'
# row2 = '000073009'
# row3 = '309000045'
# row4 = '490000000'
# row5 = '803050902'
# row6 = '000000036'
# row7 = '960000308'
# row8 = '700680000'
# row9 = '028000000'

dummyboard = []

dummyboard.append(list(row1))
dummyboard.append(list(row2))
dummyboard.append(list(row3))
dummyboard.append(list(row4))
dummyboard.append(list(row5))
dummyboard.append(list(row6))
dummyboard.append(list(row7))
dummyboard.append(list(row8))
dummyboard.append(list(row9))
# print(dummyboard)


def fill_blank_board(theboard,inputdata):
    #this is used for testing the SOLVE portion of the game
    #i don't want to have to type in a new playing board everytime for 
    #testing.
    
    #easy solve in 11 iterations of sole
    for r in range(9):
        for c in range(9):
            curr_cell = "r%dc%d" % (r+1,c+1)
            theboard[curr_cell].value = int(inputdata[r][c])
            if theboard[curr_cell].value == 0:
                theboard[curr_cell].value = None
            theboard[curr_cell].answer = theboard[curr_cell].value
            theboard[curr_cell].change_cell_image()
            #initialize possibles
            theboard[curr_cell].solve_clear_possibles()

def solve_remove_possibles(f_board):
    print("setting initial possibles")

    for f_cell in f_board.values():      #cycle through each cell
        if f_cell.answer != None:    #if an answer known
            f_cell.solve_clear_possibles()
            for f_cell2 in f_board.values():  
                #cycle through each cell again and clear out the row, col, and inner possibles for that value
                if (f_cell2.row == f_cell.row) or (f_cell2.col == f_cell.col) or (f_cell2.inner == f_cell.inner):  
                    if f_cell.answer in f_cell2.possibles.keys():
                        del f_cell2.possibles[f_cell.answer]
        print(f_cell.row,f_cell.col,f_cell.answer,f_cell.possibles)

def solve_update_possibles(f_r,f_c,f_inn,f_value,f_board):
    print("updating possibles")

    for f_cell in f_board.values():
        if (f_r == f_cell.row) or (f_c == f_cell.col) or (f_inn == f_cell.inner):
            if f_value in f_cell.possibles.keys():
                del f_cell.possibles[f_value]
        print(f_cell.row,f_cell.col,f_cell.answer,f_cell.possibles)

def solve_only(f_board):
    f_changed = False
    #if a cell only has ONE possible value, then that must be the answer
    for f_cell in f_board.values():
        if len(f_cell.possibles) == 1:  #there is only one value
            for f_thekey in f_cell.possibles.keys():  #there will only be one
                f_cell.guess = f_thekey
                f_cell.answer = f_thekey
                
                print("changing %s to %d" % (f_cell.name,f_thekey))

                f_cell.change_cell_image()
                f_cell.solve_clear_possibles()
                solve_update_possibles(f_cell.row,f_cell.col,f_cell.inner,f_thekey,f_board)
                f_changed = True
    return f_changed

def solve_unique(f_board):
    f_change = False
    #if a cell within a row, or column, or inner cube is the only cell that can
    #be of a certain value, then that is the answer
    f_unique_byrow = True
    f_unique_bycol = True
    f_unique_byinn = True
    for f_cell in f_board.values():
        #look at each possible value.  Is it a possible value in any other cell in that row?  is it a possible in any other cell in that column?  Finally, is it a possibile value in any other cell in the inner cube?
        for f_each_poss in f_cell.possibles.keys():
            f_unique_byrow = True #reset for each possible in each cell
            f_unique_bycol = True #reset for each possible in each cell
            f_unique_byinn = True #reset for each possible in each cell
            for f_cell2 in f_board.values() :  #cycle through each 81 again
                if f_cell.row == f_cell2.row and f_cell != f_cell2 :       #same row, but exclude same cell
                    if f_each_poss in f_cell2.possibles.keys():
                        f_unique_byrow = False
                if f_cell.col == f_cell2.col and f_cell != f_cell2 :       #same column, but exclude same cell
                    if f_each_poss in f_cell2.possibles.keys():
                        f_unique_bycol = False
                if f_cell.inner == f_cell2.inner and f_cell != f_cell2 :       #same row, but exclude same cell
                    if f_each_poss in f_cell2.possibles.keys():
                        f_unique_byinn = False
            if f_unique_byrow or f_unique_bycol or f_unique_byinn:      #if any true:
                #set the value of the cell equal to the possible value
                f_cell.guess = f_each_poss
                f_cell.answer = f_each_poss
                f_cell.change_cell_image()            #update image
                #clear the possibles in the current cell
                f_cell.solve_clear_possibles()
                # print("cell r%d c%d got value %d because row unique: %r or col unique %r or inner unique %r" % (f_cell.row,f_cell.col,f_each_poss,f_unique_byrow,f_unique_bycol,f_unique_byinn))
                #update the Possible in related cells
                solve_update_possibles(f_cell.row,f_cell.col,f_cell.inner,f_each_poss,f_board)
                f_change = True
                return f_change
    return f_change

def remove_possible(f_value,f_special_board,fi,f_name1,f_name2):
    f_change = False
    for f_each_cell in f_special_board[fi].values():
        if f_each_cell.name != f_name1 and f_each_cell.name != f_name2:
            if f_value in f_each_cell.possibles.keys():
                del f_each_cell.possibles[f_value]
                f_change = True     #only set this to true if a possible was deleted
                print("possibles for %s are %s" % (f_each_cell.name,f_each_cell.possibles.values()))
    return f_change

def solve_naked_subset(f_group_board):
    #this finds cells where there are only 2 possibles
    #for instance if 2 cells ONLY have two possible values, then those values can't be possibles in any other cells in that row /column/inner
    f_change = False
    # this uses
    # rowboard[i] = {}
    # colboard[i] = {}
    # innboard[i] = {}

    #for rows
    for fi in range(1,10):
        for f_each_cell in f_group_board[fi].values():
            if len(f_each_cell.possibles) == 2: #only 2 possible values
                    for f_each_cell2 in f_group_board[fi].values():
                        if f_each_cell != f_each_cell2 and f_each_cell.possibles == f_each_cell2.possibles:
                            #different cell, but the possible pairs are equal
                            #then remove the possible values from all other cells in tht row
                            for f_poss in f_each_cell.possibles.values():  #this will run twice
                                print("removing %d because pair in %s and %s" %(f_poss, f_each_cell.name,f_each_cell2.name))
                                f_change = f_change or remove_possible(f_poss,f_group_board,fi,f_each_cell.name,f_each_cell2.name)  #this could be true on one and false on another.  so if it is ever true, return true
                            if f_change == True:
                                return f_change     # as soon as there is a change, go back to top
    return f_change

def is_it_solved(f_board):
    for f_each_cell in f_board.values():
        if f_each_cell.answer == None or f_each_cell.answer == 0:
            return False
    return True

def print_grid(cube,what):  
    #function for printing my grid in python terminal
    #used for testing
    #default print is the initial values, unless you specifically ask for "answer"
    #can all print the inner cube values with "inner"
    #print first line:
    print("----"*9 + "-")      #top border  
    for i in range(1,10):
        print ("|",end='')  #first left border
        for j in range(1,10):
            if what == "answer":
                
                # print ((" %s |" % (each['data'].answer,)), end='') 
                print ((" %s |" % (cube['r%dc%d' % (i,j)].answer,)), end='') 
            elif what == "inner":
                # print ((" %s |" % (each['data'].inner,)), end='') 
                print ((" %s |" % (cube['r%dc%d' % (i,j)].inner,)), end='') 
            else:
                # print ((" %s |" % (each['data'].value,)), end='') 
                print ((" %s |" % (cube['r%dc%d' % (i,j)].value,)), end='') 

        print (" ") #new line
        print("----"*9 + "-") #separator lines and bottom border

def output_data(cube,newfile):
    #if a user uses the solve method, and enters a new board...then this can be used to save the output to a file
    #this function will be used to save a user input board, and its computed solution.  this data set can then be used in the game play side of the program.
    randomfilenum = random.randint(1, 3000)   
    print(randomfilenum)
    newfile = newfile + str(randomfilenum) + ".py"
    f = open(newfile,"w+")
    answerstring = "rawboard=["

    for i in range(1,10):
        answerstring = answerstring + "["
        for j in range(1,10):
            location = ('r%dc%d' % (i,j))
            aa =  (cube[location].value)    #user entered starting point
            if aa == " " or aa == None:
                aa = '0'
            bb =  (cube[location].answer)    #computer generated answer
            if bb == " " or bb == None:
                bb = '0'

            if j == 9:
                answerstring = answerstring +  ("(%s,%s)" % (aa,bb))
            else:
                answerstring = answerstring +  ("(%s,%s)," % (aa,bb))
        if i == 9:
            answerstring = answerstring + ("]")
        else:
            answerstring = answerstring + ("],\n")
    answerstring = answerstring + ("]")
    f.write(answerstring)

def set_coordinates_from_click(event):
    x = event.pos[0]
    y = event.pos[1]
    if y in range(730) and x in range(730):
        board_clicked = True
        # use math to figure out what square they are in:
        row =  int(y // 81) + 1
        col = int (x // 81) + 1
        cell = 'r%dc%d' % (row,col)
        # calculate the pencil_cell
        tempcol = (x % 81) // 27
        temprow = (y % 81) // 27
        pencilplacement = temprow * 3 + tempcol + 1
        # print("the pencil cell is %d" % pencilplacement)
    else:
        board_clicked = False
        row = 0
        col = 0
        cell = ""
        pencilplacement = 0
    return row,col,cell,board_clicked,pencilplacement

def clear_coordinates():
    r = 0
    c = 0
    cl = ""
    penc = 0
    board_clicked = False
    # entry = 0   #should this be here??
    return r,c,cl,board_clicked,penc

def sanity_check(f_special_board):
    for fi in range(1,10):
        f_dict = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
        for f_cell in f_special_board[fi].values():
            if f_cell.answer in range (1,10):
                f_dict[f_cell.answer] += 1  #add one to the counter
                if f_dict[f_cell.answer] > 1:
                    return False
    return True  
        
def main_menu():
    width = 400
    height = 400

    #set some colores
    background_color = (159,209,204)   #blue
    pitch_blue_color = (83,94,126)

    main_answer = False

    pygame.init()       #should this be in each module??

    #try to change cursor
    
    font = pygame.font.Font('fonts/cmtt10.ttf', 22)    #must be after init                        
    #default cursor
    # pygame.mouse.set_cursor(*pygame.cursors.arrow)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Sudoku - Choose game play mode')
    clock = pygame.time.Clock()

    while not main_answer:
        for event in pygame.event.get():
            # Event handling
            if event.type == pygame.QUIT:
                main_answer = True

            if event.type == pygame.KEYDOWN:   
                # myentry = event.key
                choices = {97:"Play",98:"Solve",27:"Esc"}
                game_state = choices.get(event.key,None)  #don't change the state unless a valid state
                print ("game state is %s" % game_state)
                if game_state == "Esc":  #this will end the game
                    main_answer = True
                elif game_state == "Play":
                    main_answer = True
                elif game_state == "Solve":
                    main_answer = True
                


        screen.fill(background_color)

        window_text = font.render('Enter A for Play mode.', True, (pitch_blue_color))
        window_text2 = font.render('Or B for solving mode.', True, (pitch_blue_color))
        
        screen.blit(window_text, (75,100))
        screen.blit(window_text2, (75,250))

        pygame.display.update()     #internal function

        clock.tick(60)  #600 makes the fan go crazy
    
    print(__name__)
    return game_state

    # pygame.quit()   #change to return  #quit when you are out of while loop

def solve():
    board = create_blank_board()
    
    # create 3 different dictionaries that have sub dictionaries by row, column, and inner  
    # but they point to the exact same cell references

    rowboard = {}
    colboard = {}
    innboard = {}
    for i in range (1,10):
        # initialze dictionaries
        rowboard[i] = {}
        colboard[i] = {}
        innboard[i] = {}

    for each_cell in board.values():
        rowboard[each_cell.row]["r%dc%d" % (each_cell.row,each_cell.col)] = each_cell
        colboard[each_cell.col]["r%dc%d" % (each_cell.row,each_cell.col)] = each_cell
        innboard[each_cell.inner]["r%dc%d" % (each_cell.row,each_cell.col)] = each_cell

    #this is only used when testing my solve logic
    #otherwise the user will manually enter the board

    # fill_blank_board(board,dummyboard)
    
    # print_grid(board,"answer")


    def solve_input():
        solve_remove_possibles(board)
        
        changed = True

        while changed :     
            print("%r - running solve only" % changed)
            changed = solve_only(board)

            if changed == False:
                print("%r - running unique" % changed)
                changed = solve_unique(board)
        
            if changed == False:
                print("%r - running solvd nakeed row" % changed )
                changed = solve_naked_subset(rowboard)

            if changed == False:
                print("%r - running solvd nakeed col" % changed)
                changed = solve_naked_subset(colboard)

            if changed == False:
                print("%r - running solved naked inner" % changed)
                changed = solve_naked_subset(innboard)

    # declare the size of the canvas
    width = 730
    height = 780

    row,col,cell,pencil_box,board_clicked = clear_coordinates()      

    #set some colores
    blue_color = (97, 159, 182)  
    background_color = (244,237,221)  #cream
    orange_color = (192, 83, 64)

    #initalize pygame and playing window
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Sudoku Solver')
    clock = pygame.time.Clock()

    #set some fonts - do AFTER pygame.init
    # font = pygame.font.Font(None, 25)                 
    # #set sytem font.  (filename, size)
    font = pygame.font.Font('fonts/cmtt10.ttf', 48)                           

    #default images used throughout
    grid_image = pygame.image.load('numbers/big_grid_lines.png').convert_alpha()
    outline_image = pygame.image.load('numbers/outline.png').convert_alpha()

    # Draw background
    screen.fill(background_color)
    stop_game = False
    solved_text = font.render("" , True, (orange_color))

    while not stop_game:

        for event in pygame.event.get():
            # Event handling
            if event.type == pygame.QUIT:
                stop_game = True

        #get events from user - clicks, keyboard
        if event.type == pygame.KEYDOWN:   
            # myentry = event.key
            choices = {27:"Esc",115:"Solve",9:"Tab"}
            game_state = choices.get(event.key,None)  #don't change the state unless a valid state
            print ("game state is %s" % game_state)
            if game_state == "Esc":  #this will end the game
                stop_game = True
            elif game_state == "Solve":
                if sanity_check(rowboard) and sanity_check(colboard) and sanity_check(innboard):
                    solve_input()
                    # print_grid(board,"answers")
                    screen.fill(background_color)  # you need this to overwrite

                    game_state = None  #so solve only runs once
                    solved = is_it_solved(board)
                    # print("the puzzle is %r" % solved)
                    if solved == False:
                        solved_text = font.render("unable to solve puzzle" , True, (orange_color))
                    elif solved == True:
                        solved_text = font.render("Puzzle Solved!!" , True, (orange_color))
                else:
                    print("can not solve this board - does not pass the mustard")

            elif game_state == "Tab" and cell != 0:
                #increase row by 1

                if col == 9 and row == 9:
                    row = 1
                    col = 1
                elif col == 9:
                    col = 1
                    row += 1
                else:
                    col += 1
                cell = "r%dc%d" % (row,col)


        #get user input
        #get mouse coordinates and 
        if event.type == pygame.MOUSEBUTTONDOWN:            #get board_coordinates
                # if in game board return coordinates. 
                # a click outside of the soduko board does NOTHING
            row,col,cell,board_clicked,pencil_box = set_coordinates_from_click(event)
            # entry = 0


        #get number entered
        if board_clicked == True :
            if event.type == pygame.KEYDOWN:            #get game_state
            # print('key down %r. game state is %s' % (event.key,game_state))
                entry = event.key
                choices = {49:1,50:2,51:3,52:4,53:5,54:6,55:7,56:8,57:9,48:0,8:0}

                number = choices.get(entry, None) 
                if number != None:      #it got a value number
                    #update cell value
                    screen.fill(background_color)  # you need this to overwrite

                    #if user enters 0, blank out the value
                    if number == 0:
                        board[cell].value = None
                    else:
                        board[cell].value = number
                    board[cell].answer = board[cell].value
                    board[cell].change_cell_image()
                    # board[cell].solve_update_possibles()
                    # board[cell].possibles = {}  #probably won't need this
        
        screen.fill(background_color)  # you need this to overwrite

        # update the display
        # should only be done if there were changes....add this
        for thecell in board.values():
            if thecell.image != None :
                screen.blit(thecell.image, (thecell.x_position,thecell.y_position))

    

        
     
        instruction_text = font.render("press S to solve", True ,(orange_color))
        

        screen.blit(instruction_text, (2,731))
        screen.blit(grid_image, (0,0))
        screen.blit(solved_text, (50,50))
        if cell != 0:
            screen.blit(outline_image, (((col-1)*81),((row-1)*81)))

        pygame.display.update()     #internal function
        #i turned the fps down to 10 from 60...i don't need 
        #fast graphics AND this slowed my tabbing function
        #to a reasonable speed so that it is useable.
        clock.tick(10)  #this is frames per second, i think


    if solved != False:
        output_data(board,"newrawboard")

    pygame.quit()

def play():     #or rename this "Play"

    # declare the size of the canvas
    width = 900
    height = 810

    #set some colores
    blue_color = (97, 159, 182)  #background color
    background_color = (244,237,221)  #cream
    background_color = (216,212,182)
    # background_color = (159,209,204)   #blue
    blue_color = (97, 159, 182)  #sky_blue
    red_color = (255,0,0)
    pitch_blue_color = (83,94,126)
    red_color = (255,0,0)
    green_color = (89,162,134)
    orange_color = (224,95,20)
    sea_foam_color = (159,209,204)


    #initalize pygame and playing window
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Sudoku')
    clock = pygame.time.Clock()

    #set some fonts - do AFTER pygame.init
    # font = pygame.font.Font(None, 25)                 
    # #set sytem font.  (filename, size)
    font = pygame.font.Font('fonts/cmtt10.ttf', 22)                           
    # font = pygame.font.Font('fonts/futurachapro-Regular.ttf', 25)                           

    #default images used throughout
    grid_image = pygame.image.load('numbers/big_grid_lines.png').convert_alpha()
    pencil_grid_image = pygame.image.load('numbers/litte_grid_lines.png').convert_alpha()
    # big_x_image = pygame.image.load('numbers/x.png').convert_alpha()
    big_x_image = pygame.image.load('numbers/x_diffuse.png').convert_alpha()
    


    ##################################################################################################
    ###everything below here is for the game play mode. ##############################################
    ##################################################################################################

    # Game initialization

    #create data
    board = create_board(rawboard)

    #this is a test
    #this will be moved to the solve portion
    output_data(board,"newrawboard")  

    # for each in board.values():
    #     print(each.answer)
    #these print to the terminalo
    # print_grid(board,"value")
    # print_grid(board,"answer")
    # print_grid(board,"inner")


    #message text
    message_text = font.render('', True, (orange_color))        
    
    #set initial values to be used throughout  
    row,col,cell,pencil_box,board_clicked = clear_coordinates()      

    undo_array = []     #this holds the cells that have had value changed.  in order.  it can hold duplicates
    stop_game = False
    game_state = "Normal"  #default mode
    entry = 0       #where and why do I need this????
    any_change = True

    while not stop_game:
        for event in pygame.event.get():
            # Event handling
            if event.type == pygame.QUIT:
                stop_game = True

            # GET USER INPUT VALUES FROM KEYBOARD AND MOUSE
            if event.type == pygame.MOUSEBUTTONDOWN:            #get board_coordinates

                # if in game board return coordinates. 
                # a click outside of the soduko board does NOTHING
                row,col,cell,board_clicked,pencil_box = set_coordinates_from_click(event)
                entry = 0
                any_change = True
            
            if event.type == pygame.KEYDOWN:            #get game_state
                # print('key down %r. game state is %s' % (event.key,game_state))
                entry = event.key
                print(entry)
                # letter_choices = {121:"Y",115:"Solved",98:"Blank",103:"Newgame"}
                letter_choices = {110:"Normal",112:"Pencil",27:"Esc",117:"Undo",104:"Hint",101:"Error"}
                game_state = letter_choices.get(entry,game_state)  #don't change the state unless a valid state
                any_change = True
                if game_state == "Esc":  #this will end the game
                    stop_game = True
                print("game state is %s" % game_state)

                # if game_state not "Normal", a key press should reset board_clicked to false
                if game_state != "Normal":
                    board_clicked = False

            if game_state == "Pencil":
                datatuple, masktuple = pygame.cursors.compile( pencil_strings,black='.', white='X', xor='o' )
                pygame.mouse.set_cursor( (24,24), (0,0), datatuple, masktuple )
            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)


            #state evaluations and GAME LOGIC
            if game_state == "Normal":
                message_text =  font.render('Click on a blank square to enter value', True, (orange_color))
            if game_state == "Error":
                message_text =  font.render('These are your mistakes', True, (orange_color))


            #we are in the "Normal" state and a key has been pressed
            #added delete key (8) to be set to zero
            if board_clicked == True and game_state == "Normal":  
                # print (entry)
                choices = {49:1,50:2,51:3,52:4,53:5,54:6,55:7,56:8,57:9,48:0,8:0}
                number = choices.get(entry, None) 
                if number != None:      #it got a value number
                    #update cell value
                    #add the current cell and its CURRENT vaue to the undo_array
                    
                    undo_pair = (cell,board[cell].guess)
                    undo_array.append(undo_pair)

                    #if user enters 0, blank out the value
                    if number == 0:
                        board[cell].guess = None
                    else:
                        board[cell].guess = number
                    print(undo_array)
                    board[cell].change_cell_image()
                    # board['r%dc%d' % (row,col)].change_cell_image()
                    #flip switches:
                    board_clicked = False
                    entry = 0  #reset entry
                    #change message
                    message_text = font.render("", True, (orange_color))  

                else:
                    message_text = font.render('You are editing row: %d / column: %d.  You can only enter numbers' % (row,col), True, (orange_color))  
            
            if game_state == "Pencil":

                message_text = font.render("click on the tiny cell to toggle-in your possible options" , True, (orange_color))

                if board_clicked == True and type(board[cell]) == Unknown_cell: 
                        #update  pencil cell value (true/false) - flip its value
                        board[cell].pencils[pencil_box].set = not board[cell].pencils[pencil_box].set
                        #updae pencil cell image
                        board[cell].pencils[pencil_box].update_pencil_image()  #self.value work?
                        #board_clicked goes back to false till a new click happens
                        board_clicked = False

            if game_state == "Undo":
                message_text = font.render("Press Undo again to revert your changes one by one." , True, (orange_color))
                
                if len(undo_array) > 0:
                    to_remove = undo_array.pop()
                    # print (to_remove)
                    #the cell is changed back to its old value
                    board[to_remove[0]].guess = to_remove[1]
                    #update the image for the cell
                    board[to_remove[0]].change_cell_image()
                

                else:
                    game_state = "Normal"
                    message_text = font.render("There are no more changes to Undo." , True, (orange_color))
                #revert screen display to Normal
                game_state = "Normal"
 
            if game_state == "Hint":
                message_text = font.render('Select the cell you want the answer to', True, (orange_color))
                
                if board_clicked == True:
                    print("my cell is within hint")
                    print(cell)
                    if board[cell].answer == 0:
                        message_text = font.render("No Hint available", True, (orange_color))
                    else :
                        
                        board[cell].guess = board[cell].answer
                        board[cell].change_cell_image()
                
                    entry = 0        
                    game_state = "Normal"  #set back to "Normal"
                    print(game_state)
                    board_clicked = False

        # Draw background
        screen.fill(background_color)   # this does not overlay everything!!

        # Game display 
        #only do this if there has been a change (any_change)

        if any_change == True:
            #set the blits for all known numbers
            for thecell in board.values():
                # if game_state == "Normal" or game_state == "Hint" or game_state == "Error":
                if thecell.image != None :
                    screen.blit(thecell.image, (thecell.x_position,thecell.y_position))
                if game_state == "Error":  #overlay the x if guess is wrong
                    if type(thecell) == Unknown_cell and thecell.guess != thecell.answer and thecell.guess != None:
                        screen.blit(big_x_image, (thecell.x_position,thecell.y_position))

                elif game_state == "Pencil":               #in pencil mode
                            # this is OVERLAYED over the guesses
                            #while we are in pencil mode,the cells that are blank (guess = None and value = None)  
                            # have their image updated with their possible values
                    if type(thecell) == Unknown_cell:
                        for z in range(1,10):
                            # this requires 9 blit values and a grid
                            screen.blit(thecell.pencils[z].image, (thecell.pencils[z].xpos,thecell.pencils[z].ypos))
                            screen.blit(pencil_grid_image, (thecell.x_position,thecell.y_position))
                    
                    # if type(thecell) == Known_cell:    #use cell value
                    #     screen.blit(thecell.image, (thecell.x_position,thecell.y_position))
                    # else:       #unknown cells
                        


            screen.blit(grid_image, (0,0))

            # update the message_text based on state values
                    
            if board_clicked == True and game_state == 'Normal':
                if type(board[cell]) == Known_cell:    #if known:
                    message_text = font.render('You cannot change this cell.  Try another', True, (orange_color))
                    row,col,cell,board_clicked,pencil_box = clear_coordinates()
                    # board_clicked = False  #change this b/c its not a valid square
                    entry = 0   #need???
                else:       #Unknown value, changeable
                    entry = 0  #clear out entry values
                    message_text = font.render('You are changing the cell at row: %d / column: %d.  Enter a number from 1 t0 9' % (row,col), True, (orange_color))
            
            if game_state == "Undo":
                message_text = font.render("Press Undo again to revert your changes one by one." , True, (orange_color))

            gen_text = font.render('Press N, then Click on a blank square to enter value', True, (pitch_blue_color))
            gen_text2 = font.render('Press P to add Pencil Values -- U to Undo your guesses -- ESC to quit', True, (pitch_blue_color))
            gen_text3 = font.render('enter 1-9 for values.  0/delete clear guesses ...', True, (pitch_blue_color))
        
            screen.blit(message_text, (3,731))
            screen.blit(gen_text, (3, 750))
            screen.blit(gen_text2, (3, 765))
            screen.blit(gen_text3, (3,780))


            
            side_text1 = font.render('N - Normal', True, (pitch_blue_color))
            screen.blit(side_text1, (730,0))
            side_text2 = font.render('P - Pencil', True, (pitch_blue_color))
            screen.blit(side_text2, (730,40))
            side_text3 = font.render('H - Hint', True, (pitch_blue_color))
            screen.blit(side_text3, (730,80))
            side_text4 = font.render('E - Errors', True, (pitch_blue_color))
            screen.blit(side_text4, (730,120))
            side_text5 = font.render('U - Undo', True, (pitch_blue_color))
            screen.blit(side_text5, (730,160))
            side_text6 = font.render('ESC - Quit', True, (pitch_blue_color))
            screen.blit(side_text6, (730,200))

            any_change = False  #after update, flip back

            pygame.display.update()     #internal function

        clock.tick(60)  #600 makes the fan go crazy

    pygame.quit()

main_state = None
print(__name__)

if __name__ == '__main__':
    # main()
    main_state = main_menu()
    print (main_state)
    if main_state == "Play":
        play()
    else:
        solve()
