import re
import urllib.parse

file_name = "text_file"
file = open(file_name,"r")
content = file.read()
id = 0
min_rating = 3
min_support = 4
min_conf = .6
items_with_rating = dict()
list = []
for c in content:
    if c != ' ' and c!=',' and c!='\n':
        if c!='>' and c!='<':
            list.append(c)
        elif c=='<':
            items_with_rating[id] = list
            id+=1
            list = []

for id,transaction in items_with_rating.items():
    for i in range(len(transaction)):
        curr = 0
        for j in range(i + 1, len(transaction)):
            if(int(transaction[i])>=3 and int(transaction[j])>=3):
                curr+=1
                if(curr>=30):
                    print("yai")

            #compare(mylist[i], mylist[j])
    # for t in transaction:

max_rating = 5
