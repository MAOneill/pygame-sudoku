# dictinners={}
# dictinners['inner1']={}
# dictinners['inner2']={}
# dictinners['inner1']['row1']=5  #this would actuall be an object
# dictinners['inner1']['row2']=7
# dictinners['inner2']['row2']=7


# print(dictinners['inner1']['row2'])

innerrow = {1:(1,2,3),2:(1,2,3),3:(1,2,3),
            4:(4,5,6),5:(4,5,6),6:(4,5,6),
            7:(7,8,9),8:(7,8,9),9:(7,8,9)}

innercol = {1:(1,2,3),2:(4,5,6),3:(7,8,9),
            4:(1,2,3),5:(4,5,6),6:(7,8,9),
            7:(1,2,3),8:(4,5,6),9:(7,8,9)}


for inners in range(1,10):
    myrows = innerrow.get(inners,None)  
    mycols = innercol.get(inners,None)

    for x in myrows:
        for y in mycols:
            print("inner: %d = row: %d col: %d" % (inners,x,y))


