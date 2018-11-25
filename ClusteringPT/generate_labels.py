f = open("Iris_t.csv","r")
data = f.readlines()[1]
data = data.split(",")
data = data[1:len(data)-1]
f.close()

#f = open("t_xlabels.txt",'w')
count = 0
for word in data:
    #f.write ("\""+word+"\""+",")
    #print(word)
    count+=1
print(count)
