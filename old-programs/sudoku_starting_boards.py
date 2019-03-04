import pprint
import copy

#note this will not solve very difficult sodukos.  only those that do
#not require 'recursive backtracking' - i.e., guessing when there are not
#obvious answers and then trying to complete...
#http://apollon.issp.u-tokyo.ac.jp/~watanabe/sample/sudoku/index.html
#this explains the multiple techniques to solve:
# https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php

'''
#easy solve in 11 iterations of sole
row1 = '530070000'
row2 = '600195000'
row3 = '098000060'
row4 = '800060003'
row5 = '400803001'
row6 = '700020006'
row7 = '060000280'
row8 = '000419005'
row9 = '000080079'
'''

'''
#solves in 8 iterations of sole
row1 = '340826071'
row2 = '008000900'
row3 = '760090043'
row4 = '080102030'
row5 = '030000090'
row6 = '070904010'
row7 = '820040059'
row8 = '007000300'
row9 = '410389062'
'''

'''
#can't be solved without other methods:
#i have the solution to this
row1 = '907800060'
row2 = '006700180'
row3 = '010000000'
row4 = '008004000'
row5 = '100050003'
row6 = '000090078'
row7 = '000010000'
row8 = '600400005'
row9 = '500009001'
'''
'''
#supposed to be very hard:
#from http://apollon.issp.u-tokyo.ac.jp/~watanabe/sample/sudoku/index.html  (1)
#the first two methods get you no where with this one...
#will be good to test the other methods
#first nake pair method won't solve this either - its gets you one value
row1 = '046005700'
row2 = '000900000'
row3 = '090001006'
row4 = '000000900'
row5 = '030000000'
row6 = '400520008'
row7 = '080000070'
row8 = '570300082'
row9 = '200000300'
'''

#supposedly the hardes that the apollon site has found:
#my program solved this with only sole and unique...
'''
row1 = '061007003'
row2 = '092003000'
row3 = '000000000'
row4 = '008530000'
row5 = '000000504'
row6 = '500008000'
row7 = '040000001'
row8 = '000160800'
row9 = '600000000'
'''

#another one to test:
#not solvable with sole and unique:
# from https://www.websudoku.com/images/example-steps.html
# i get furher with sole,unique and naked pair, but still not solvable
row1 = '000000680'
row2 = '000073009'
row3 = '309000045'
row4 = '490000000'
row5 = '803050902'
row6 = '000000036'
row7 = '960000308'
row8 = '700680000'
row9 = '028000000'

starting_cube = []

starting_cube.append(list(row1))
starting_cube.append(list(row2))
starting_cube.append(list(row3))
starting_cube.append(list(row4))
starting_cube.append(list(row5))
starting_cube.append(list(row6))
starting_cube.append(list(row7))
starting_cube.append(list(row8))
starting_cube.append(list(row9))

'''
starting_cube = []

# this would be done with a function and input
def input_rows():
    for i in range(9):
        raw = input("enter the 9 digits for row %d " % (i,))
        #test the input...
        #need to change 0 to blank (they could input blank)
        row = list(raw)
        starting_cube.append(row)

input_rows()
'''

#covert zeros to blanks, and digits to numbers
for i in range(0,9):
    for j in range(0,9):
        if starting_cube[i][j] == '0':
            starting_cube[i][j] = " "
        else:
            starting_cube[i][j] = int(starting_cube[i][j])

cell = {
    'row' : None,
    'col' : None,
    'inner_cube': None,
    'final_value': None,
    'possibles' : {}
}

#print_grid can be deleted.  print_grid2 is better
def print_grid(cube):       
    #print first line:
    print("----"*9 + "-")      #top border  
    for i in range(9):
        print ("|",end='')  #first left border
        for each in cube[i]:
            print ((" %s |" % (each,)), end='') #it is a string right now
        print (" ") #new line
        print("----"*9 + "-") #separator lines and bottom border

#you can this to print
def print_grid2(cube,value):
    #print first line:
    print("----"*9 + "-")      #top border  
    for i in range(9):
        print ("|",end='')  #first left border
        for each in cube[i]:
            print ((" %s |" % (each[value],)), end='') #it is a string right now
        print (" ") #new line
        print("----"*9 + "-") #separator lines and bottom border

def print_raw_input_array(startcube,finalcube):
    #this crude, but it helps to get input for the pygame_soduko.  cut, paste and clean up
    zz = []
    print ("answer = [", end='')
    for i in range(9):
        rr = []
        print ("[", end = '')
        for j in range(9):
            # print ("inside new function")
            aa =  (startcube[i][j])
            if aa == " ":
                aa = '0'
            bb =  (finalcube[i][j]['final_value'])
            yy = '(%s,%s)' % (aa,bb)
            # print(yy)
            rr.append(yy)
            if j == 8:
                print ("(%s,%s)" % (aa,bb), end = "")
            else:
                print ("(%s,%s)," % (aa,bb), end = "")
        # print(j)
        if i == 8:
            print("]")
        else:
            print("],")
        # print (rr)
        zz.append(rr)
    print("]")
    # print (zz)


def print_details():
    for i in range(9) :
        for j in range(9):
            print("i: %d j: %d INNER:" % (i,j), end =  ' ')
            print(grid[i][j]['inner_cube'], end=" ")
            print(grid[i][j]['possibles'])

#create 81 objects - one for each cell

def create_all_objects():
    objects = []
    for i in range(9):  #rows
        rows = []
        box = int(i//3) * 3 #rows 0,1,2 = 0; 3,4,5 = 3; 6,7,8 = 6
        for j in range(9):
            box2 = int(j//3)   #cols 0,1,2 = 0; 3,4,5= 1; 6,7,8 = 2
            inner_cube = box + box2   #results in 0 - 8 for the 9 inside 3x3 cubes
            if starting_cube[i][j] in {1,2,3,4,5,6,7,8,9}:
                square = {'inner_cube':inner_cube,
                        'final_value':starting_cube[i][j],
                        'possibles':{}      #final value then no possibles
                }
            else:   #final value is " ""
                square = {'inner_cube':inner_cube,
                            'final_value':starting_cube[i][j],
                            'possibles':{1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9}
                }
            rows.append(square)
        objects.append(rows)
    return objects

grid = create_all_objects()

# print_grid(starting_cube)
# print_grid2(grid,'inner_cube')
# print_grid2(grid,'final_value')

#create 3 objects to hold the known values for rows, columns, and cubes
#changed this to hold key pairs!
check = {
    0:{},
    1:{},
    2:{},
    3:{},
    4:{},
    5:{},
    6:{},
    7:{},
    8:{}
}
#deepcopy creates an entire new object.  not just a pointer to the original object
#these tables how arrays with the TAKEN values for the row/column/cube
#so or blank cells can't have these values.

#these start blank...
#they get filled up as we find KNOWN values

checkrows=copy.deepcopy(check)
checkcols=copy.deepcopy(check)
checkinner=copy.deepcopy(check)

def set_possibles(grid):
    
    #create 3 tables to be used in the next step
    for i in range(9):
        #for each row
        for j in range(9):
            #for each cell...
            if grid[i][j]['final_value'] != " ":
                    value = grid[i][j]['final_value']   #known and set squares
                    inner = grid[i][j]['inner_cube']    #cell lives in cube x
                    # you have to check if it exists before you add it
                    # if the value was found and is KNOWN, add to checks
                    if value not in checkrows[i].keys():
                        checkrows[i][value]=value
                    if value not in checkcols[j].keys():
                        checkcols[j][value]=value
                    if value not in checkinner[inner].keys():
                        checkinner[inner][value]=value

def remove_possibles():
    for i in range(9):
        for j in range(9):
            inner = grid[i][j]['inner_cube']
            # you have to check if it exists before you delete it
            # if the value was found and is KNOWN, remove from possibles
            for each in checkrows[i].keys():
                if each in grid[i][j]['possibles'].keys():
                    del grid[i][j]['possibles'][each]
            for each in checkcols[j].keys():
                if each in grid[i][j]['possibles'].keys():
                    del grid[i][j]['possibles'][each]
            for each in checkinner[inner].keys():
                if each in grid[i][j]['possibles'].keys():
                    del grid[i][j]['possibles'][each]



def find_finals():
    #if only one possible left - that is the KNOWN
    solved = True
    changed = False
    for i in range(9):
        for j in range(9):
            if len(grid[i][j]['possibles']) == 1:    #only on possible left
                error = 0
                changed = True
                for thekey in grid[i][j]['possibles']:
                    grid[i][j]['final_value'] = thekey
                    grid[i][j]['possibles']={}  #clear it out
                    print("ONLY row: %d col: %d was changed to %d" % (i,j,thekey))

                    error += 1
                if error > 1:
                    print ("houston, we have a problem")
            elif len(grid[i][j]['possibles']) > 1:
                #the puzzle is NOT SOLVED YET
                solved = False
    return changed,solved

def unique_candidate():
    #set changed to true in here somewhere, so it will repeat the sole part
    changed = False
    for num in range(1,10):  #1-9
        
        #check each row:
        for row in range(9):   #each row   
            counter = 0 
            thecell = ''    #clear it out
            for cell in range(9):
                if num in grid[row][cell]['possibles'].keys():
                    counter +=1
                    thecell = cell   #remember where it is
            if counter == 1 : #only one value found in all 9 cells of row
                #set final
                grid[row][thecell]['final_value']=num
                grid[row][thecell]['possibles']={}  #all possibles are gone. it is solved
                changed = True
                print("ROW row: %d col: %d was changed to %d" % (row,thecell,num))
                return changed

        #check each column:
        
        for row in range(9):  
            thecell = ''    #clear it out
            counter = 0  
            for cell in range(9):
                if num in grid[cell][row]['possibles'].keys():
                    counter += 1
                    thecell = cell   #remeber where it is
            if counter == 1:
                #set final
                grid[thecell][row]['final_value']=num
                grid[thecell][row]['possibles']={}
                changed = True
                print("COL row: %d col: %d was changed to %d" % (thecell,row,num))
                return changed
        
        #check each inner cube:
        for inner in range(9):
            therow =''
            thecol =''
            counter = 0

            for row in range(9):
                for cell in range(9):
                    if inner == grid[row][cell]['inner_cube']:
                        if num in grid[row][cell]['possibles'].keys():
                            counter += 1
                            therow = row
                            thecol = cell
            if counter == 1:
                #set final
                grid[therow][thecol]['final_value']=num
                grid[therow][thecol]['possibles']={}
                changed = True
                print(grid[therow][thecol], end='')
                print("INNER row: %d col: %d was changed to %d" % (therow,thecol,num))
                return changed
    return changed            



    #as soon as it finds ONE number this way - return 



changed = True
# solved = False
count = 1

#this tests for the SOLE CANDIDATE
while changed:
    
    #based on the known 'final_values' figure out the possibles
    set_possibles(grid)
    # print ("initial")
    # pprint.pprint(grid[1])

    remove_possibles()
    # print ("After removing first round of possibles")
    # pprint.pprint(grid[1])

    changed,solved = find_finals() #will return True if a change is made
    # print ("after finding some finals")
    # pprint.pprint(grid[1])
    #can change solved to True, if no more possibles

    print("%d iteration.  changed = %r" % (count,changed))
    # print_details()
    # print ("----------------------")

    count +=1

    #solved = True or False...if all possibles are zero!
    if changed == False and solved == True:
        print("the puzzle is solved")
    elif changed == False and solved == False:
        print("calling unique_candidate")
        #sole method failed to solve
        changed = unique_candidate()
    
    #if unique didn't find anyting - end
    if changed == False and solved == False:
        print ("Not currently solveable")
    elif changed == False and solved == True:
        print ("PUZZLE SOLVED")
            




# print_grid(starting_cube)

# pprint.pprint(grid)
print ("beginning cube")
print_grid(starting_cube)

print("final value:")
# print_grid2(grid,'final_value')

print ("xxxx")
print_raw_input_array(starting_cube,grid)


print("final changed:%r" % (changed,))
if changed == False:        #if it didn't finish
    print_details()

# pprint.pprint(checkrows)
# pprint.pprint(checkcols)
# pprint.pprint(checkinner)

# print(grid)