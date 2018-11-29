import re
f = open("TFIDF_Topics_v2.csv","r")
data = f.readlines()[0]
data = data.split(",")
data = data[0:len(data)-1]
f.close()

f = open("tidf_xlabels.txt",'w')
count = 0
for word in data:
    f.write ("\""+word+"\""+",")
    print(word)
    count+=1
print(count)


#create places id array
f = open("places_id.txt")
data = f.readlines()
places = dict()
for wordid in data:
    wordid = wordid.split(',')
    id = (re.sub('[^a-zA-Z0-9\n\.]', ' ', wordid[1])).replace('\n','')
    str = re.sub('[^a-zA-Z0-9\n\.]', ' ', wordid[0]).replace('\n','')
    places[int(id)] = str

f.close()


#create topics id array
f = open("topics_id.txt")
data = f.readlines()
topics = dict()
for wordid in data:
    wordid = wordid.split(',')
    id = (re.sub('[^a-zA-Z0-9\n\.]', ' ', wordid[1])).replace('\n','')
    str = re.sub('[^a-zA-Z0-9\n\.]', ' ', wordid[0]).replace('\n','')
    topics[int(id)] = str
f.close()

#generate places iris file
f = open("TFIDF_Places.csv","r")
data = f.readlines()
words = data[0]
words = words.split(",")

wr = open("IDF_Places_Iris.csv","w")
wr.write("ID"+",")
for word in words:
    wr.write(word+",")
wr.write("Species"+"\n")

i = 0
for vector in data:
    if i>0:
        j = 0

        v = vector.split(',')
        for idf in v:
            if int(v[0]) in places:
                if(j<len(v)-1):
                    wr.write(idf+",")

                else:
                    id = v[0]
                    wr.write(places[int(id)]+"\n")
            j+=1
    i+=1

wr.close()
f.close()



#generate topics iris file
f = open("TFIDF_Topics_v2.csv","r")
data = f.readlines()
words = data[0]
words = words.split(",")

wr = open("IDF_Topics_Iris.csv","w")
wr.write("ID"+",")
for word in words:
    wr.write(word+",")
wr.write("Species"+"\n")

i = 0
for vector in data:
    if i>0:
        j = 0
        v = vector.split(',')
        for idf in v:
            if int(v[0]) in topics:
                if(j<len(v)-1):
                    wr.write(idf+",")
                else:
                    id = v[0]
                    wr.write(topics[int(id)]+"\n")
            j+=1
    i+=1

wr.close()
f.close()
