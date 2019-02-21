## all of this code was moved into "pygame_soduko"


#this is the functiont that can read in the raw board settings
from board1_raw import rawboard
#raw board is an array of 9 arrays with 9 tuples each

#define the playing cell.  there are 81 of these in an 9x9 soduko board
class Cell():
    def __init__(self,row,col,value,answer=None):
        # self.start = value  #or is this in the subclass...
        # self.anser = 
        self.row = row
        self.col = col
        self.inner = 0  #compute thie
        self.pencils = {}  #{} will object create this and set here
        self.x_position = 0
        self.y_position = 0
        self.image = 'png'

        self.guess = None       #blank to start
        self.value = value      #given in start cube
        self.answer = answer    #if loaded in answers, used for hints

        self.name = "r%dc%d" % (row,col)
        

class Known_cell(Cell):
    def __init__(self,row,col,value,answer):
        super().__init__(row,col,value,answer)
        self.answer = answer  
        #known cells don't need pencils or possibles
        self.possibles = {}  #empty                 

class Unknown_cell(Cell):
    def __init__(self,row,col,value,answer=None):
        super().__init__(row,col,value,answer)
        self.answer = answer
        self.value = 0
        self.pencil = {1:False,2:False,3:False,4:False,5:False,6:False,7:False,8:False,9:False}
        self.possibles = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}



#process to create all 81 objects AND load them into an array
#I didn't not put this inside a function because I need the individual
#objects accessable by their name

def create_cell(row,col,tuple,known):
    cell = {}
    cellname = "r%dc%d" % (row,col)
    if known:       #known is true
        newcell = Known_cell(row,col,tuple[0],tuple[1]) #all named 'newcell'
    else:
        newcell = Unknown_cell(row,col,tuple[0],tuple[1]) #all named 'newcell'
        
    cell['name'] = cellname
    cell['data'] = newcell  
    # print(cell['data'].answer)
    return cell     #this points to entirely new spot each time

# returns an array of all 81 cells, organized in 9 rows (arrays)
def create_board(input_board):
    allcells = []
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
            cell = create_cell(row,col,eachtuple,known)

            # print(cell['data'].value)
            rowarray.append(cell)   #append my object into the row array
        allcells.append(rowarray)       #append row array of cells into the big one
    return allcells

#function for printing my grid in python terminal
#used for testing
#default print is the initial values, unless you specifically ask for "answer"
def print_grid(cube,what):  
    #print first line:
    print("----"*9 + "-")      #top border  
    for i in range(9):
        print ("|",end='')  #first left border
        for each in cube[i]:
            if what == "answer":
                print ((" %s |" % (each['data'].answer,)), end='') #it is a string right now
            else:
                print ((" %s |" % (each['data'].value,)), end='') #it is a string right now

        print (" ") #new line
        print("----"*9 + "-") #separator lines and bottom border



board = create_board(rawboard)

print_grid(board,"value")
print_grid(board,"answer")