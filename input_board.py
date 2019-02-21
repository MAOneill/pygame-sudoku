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
        self.guess = None  #blank to start
        self.answer = answer
        self.pencils = {}  #{} will object create this and set here
        self.x_position = 0
        self.y_position = 0
        self.image = 'png'

allcells = []
       
row = 0
for eachrow in rawboard:
    row += 1    #increment the row counter
    rowarray = []   #create a new instance here
    col = 0 
    for eachtuple in eachrow:
        col += 1
        cellname = "r%dc%d" % (row,col)
        # print (cellname)
        newcell = Cell(row,col,eachtuple[0],eachtuple[1]) #all named 'newcell'
        rowarray.append(newcell)   #append my object into the row array
    allcells.append(rowarray)       #append row array of cells into the big one

print(len(allcells))  #should be 9
print(allcells[3][5].answer) # <-- this works
# print(allcells)
print(newcell.answer)


def print_grid2(cube,value):
    #print first line:
    print("----"*9 + "-")      #top border  
    for i in range(9):
        print ("|",end='')  #first left border
        for each in cube[i]:
            print ((" %s |" % (each[value],)), end='') #it is a string right now
        print (" ") #new line
        print("----"*9 + "-") #separator lines and bottom border