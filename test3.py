for j in range(1,10,1):
    exec('var_%d = j'%j)

print(var_2)

#this works for creating dynamic variables names
#from https://stackoverflow.com/questions/13096604/creating-multiple-variables
#but he says not to do this