#this is the functiont that can read in the raw board settings
from board1_raw import rawboard
#raw board is an array of 9 arrays with 9 tuples each

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
        self.answer = answer    #if loaded in answers

        self.name = "r%dc%d" % (row,col)


class Known_cell(Cell):
    def __init__(self,row,col,value,answer):
        super().__init__(row,col,value,answer)
        self.answer = answer                    

class Unknown_cell(Cell):
    def __init__(self,row,col,value,answer=None):
        super().__init__(row,col,value,answer)
        self.answer = answer
        self.value = None



#process to create all 81 objects AND load them into an array
#I didn't not put this inside a function because I need the individual
#objects accessable by their name

allcells = []
cell = {}    
row = 0
for eachrow in rawboard:
    row += 1    #increment the row counter
    rowarray = []   #create a new instance here
    col = 0 
    for eachtuple in eachrow:
        col += 1
        
        #if the first value is KNOWN, then create a Known_cell class
        #otherwise create an Unknown_cell class
        if eachtuple[0] == 0:  #unknown
            newcell = Unknown_cell(row,col,eachtuple[0],eachtuple[1]) #all named 'newcell'
        else:
            newcell = Known_cell(row,col,eachtuple[0],eachtuple[1]) #all named 'newcell'
        cellname = "r%dc%d" % (row,col)
        cell['name'] = cellname
        cell['data'] = newcell      #'data' dictionary key pair has the object

        # exec('r%dc%d = newcell'% (row,col)) #create unique name for each object
        # print(cell['data'].value)
        rowarray.append(cell)   #append my object into the row array
    print(rowarray)
    allcells.append(rowarray)       #append row array of cells into the big one
    #need to delete newcell at sometime

# print(len(allcells))  #should be 9
# print(allcells[3][5].answer) # <-- this works
# print(allcells)


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

print_grid(allcells,"value")
print_grid(allcells,"answer")