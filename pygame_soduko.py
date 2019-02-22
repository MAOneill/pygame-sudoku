import pygame

#this is the functiont that can read in the raw board settings
#raw board is an array of 9 arrays with 9 tuples each
from board1_raw import rawboard

class Tcell():
    def __init__(self,tinycell,x,y):
        self.set = False
        # self.image = None
        self.image = pygame.image.load('numbers/%d_pencil_marks_27.png' % tinycell).convert_alpha()
        #default blank
        # self.image = pygame.image.load('numbers/pencil_marks_27.png' ).convert_alpha()
        self.xpos = x + ((tinycell-1) % 3) * 27
        self.ypos = y + ((tinycell-1) // 3) * 27

class Cell():
    #define the playing cell.  there are 81 of these in an 9x9 soduko board
    def __init__(self,row,col,value,answer=None):
        # self.start = value  #or is this in the subclass...
        # self.anser = 
        self.row = row
        self.col = col
        #  self.inner = 0  #compute thie
        self.pencils = {}  #{} will object create this and set here

        self.guess = None       #blank to start
        self.value = value      #given in start cube
        self.answer = answer    #if loaded in answers, used for hints

        self.name = "r%dc%d" % (row,col)

        rowbox = int((row-1)//3)
        colbox = int((col-1)//3)
        self.inner = (rowbox *3 )+ colbox+ 1

        self.x_position = (col-1) * 81
        self.y_position = (row-1) * 81    

        #you can only change the image for an unknown cell:
    def change_cell_image(self):
        pass

class Known_cell(Cell):
    def __init__(self,row,col,value,answer):
        super().__init__(row,col,value,answer)
        self.answer = answer  
        #known cells don't need pencils or possibles
        self.possibles = {}  #empty    
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
        #changes the display image based on the GUESS value
        #not tested yet
        self.image = pygame.image.load('numbers/%d_guess.png' % self.guess).convert_alpha()
        # self.image = pygame.image.load('numbers/%d_transparent_number.png' % value).convert_alpha()

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

def main():

    # declare the size of the canvas
    width = 850
    height = 790

    blue_color = (97, 159, 182)  #background color
    background_color = (244,237,221)
    background_color = (159,209,204)
    blue_color = (97, 159, 182)  #sky_blue
    red_color = (255,0,0)
    pitch_blue_color = (83,94,126)
    red_color = (255,0,0)
    green_color = (89,162,134)
    orange_color = (224,95,20)
    sea_foam_color = (159,209,204)


    pygame.init()
    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption('Soduko')
    clock = pygame.time.Clock()

    # Game initialization
    grid_image = pygame.image.load('numbers/big_grid_lines.png').convert_alpha()
    pencil_grid_image = pygame.image.load('numbers/litte_grid_lines.png').convert_alpha()
    #buttons
    other_button_image = pygame.image.load('numbers/other_button.png').convert_alpha()
    pencil_button_image = pygame.image.load('numbers/pencil_button.png').convert_alpha()
    solve_button_image = pygame.image.load('numbers/solve_button.png').convert_alpha()
    new_button_image = pygame.image.load('numbers/new_button.png').convert_alpha()
    undo_button_image = pygame.image.load('numbers/undo_button.png').convert_alpha()
    hint_button_image = pygame.image.load('numbers/hint_button.png').convert_alpha()

    #create data
    #do this after you set images, although I guess this could be done inside..
    board = create_board(rawboard)
    
    # for each in board.values():
    #     print(each.answer)
    #these print to the terminalo
    # print_grid(board,"value")
    # print_grid(board,"answer")
    # print_grid(board,"inner")

    #message text
    #this is for when a user does something - the message changes
    font = pygame.font.Font(None, 25)
    message_text = font.render('', True, (orange_color))    
    #set initial values to be used throughout        
    row = 0
    col = 0
    cell = 0

    stop_game = False

    pencil = False  #state at which to enter pencil values
    solving = True   #state at which to enter value.  You havce to click to get to that state   
    screen_clicked = False


    while not stop_game:
        for event in pygame.event.get():
            # Event handling
            if event.type == pygame.QUIT:
                stop_game = True
            
            # print("no event type")
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print('mouse down at %d, %d' % event.pos)  #to terminal
                screen_clicked = True
                x = event.pos[0]
                y = event.pos[1]

                # use math to figure out what square they are in:
                row =  int(y // 81) + 1
                col = int (x // 81) + 1
                cell = 'r%dc%d' % (row,col)
                print(board[cell].answer)
                #change the value of the message text
                if type(board[cell]) == Known_cell:    #if known:
                    message_text = font.render('You cannot change this cell.  Try another', True, (orange_color))
                else:       #Unknown value, changeable
                    message_text = font.render('You are changing the cell at row: %d / column: %d.  Enter a number from 1 t0 9' % (row,col), True, (orange_color))
            
            # Game logic
               
            if event.type == pygame.KEYDOWN:
                print('key down %r' % event.key)
                entry = event.key

                #pressing P toggles between pencil mode or not
                if entry == 112:     #this is for P for pencil
                    pencil = not pencil
                
                #if
                 #we are in the solving state and a key has been pressed
                if screen_clicked == True and pencil == False:     
                    choices = {49:1,50:2,51:3,52:4,53:5,54:6,55:7,56:8,57:9}
                    number = choices.get(entry, None) 
                    if number != None:      #it got a value number
                        #update cell value
                        # print(board['r%dc%d' % (row,col)].inner)
                        board['r%dc%d' % (row,col)].guess = number
                        board['r%dc%d' % (row,col)].change_cell_image()
                        #flip switches:
                        screen_clicked = False
                        #change message
                        message_text = font.render("", True, (orange_color))  

                    else:
                        message_text = font.render('You are editing row: %d / column: %d.  You can only enter numbers' % (row,col), True, (orange_color))  


        # Draw background
        screen.fill(background_color)

        # Game display

        #set the blits for all known numbers
        for cell in board.values():
            if pencil == False:     #fill images based only on values
                if cell.image != None :
                    screen.blit(cell.image, (cell.x_position,cell.y_position))
            else:               #in pencil mode
                if type(cell) == Known_cell:    #use cell value
                    screen.blit(cell.image, (cell.x_position,cell.y_position))
                else:       #unknown cells
                    for z in range(1,10):
                        # screen.blit(cell.pencils[z].image, (cell.x_position, cell.y_position))
                        screen.blit(cell.pencils[z].image, (cell.pencils[z].xpos,cell.pencils[z].ypos))
                        screen.blit(pencil_grid_image, (cell.x_position,cell.y_position))
                    

        #while we are in pencil mode,
        # the cells that are blank (guess = None and value = None)  
        # have their image updated with their possible values
        # this requires 9 blit values and a grid
        #       
        # while pencil == True:
        #     pass


        screen.blit(grid_image, (0,0))
        # screen.blit(image6, (250, 250))
        # screen.blit(pencil_image9, (600,600))


        # update the message_text
        screen.blit(message_text, (3,731))
           

        #general message...add press P for pencil??
        font = pygame.font.Font(None, 25)
        gen_text = font.render('Click on a blank square to enter value', True, (pitch_blue_color))
        gen_text2 = font.render('Press P to toggle between pencil values or Solving', True, (pitch_blue_color))
        screen.blit(gen_text, (3, 750))
        screen.blit(gen_text2, (3, 765))

        #display menu buttons
        screen.blit(new_button_image, (795,20))
        screen.blit(hint_button_image, (795,70))
        screen.blit(pencil_button_image, (795,120))
        screen.blit(undo_button_image, (795,170))
        screen.blit(other_button_image, (795,220))
        screen.blit(solve_button_image, (795,270))

        pygame.display.update()     #internal function

        clock.tick(60)  #600 makes the fan go crazy

    pygame.quit()

if __name__ == '__main__':
    main()
