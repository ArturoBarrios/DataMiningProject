import re
import urllib.parse
from TrieNode import TrieNode
import enchant
import operator

#will be used to check if string is a word
d = enchant.Dict("en_US")

#root of TrieNode
root = TrieNode('*')

np_places_count = 0
nt_topics_count = 0
word_count = 0
word_list = []

distinct_places = []
distinct_topics = []
distinct_places_and_empty = []
distinct_topics_and_empty = []
distinct_topics_count = dict()
distinct_places_count = dict()
topics_places_word_count = dict()
words_count_dict = dict()
words_for_each_paragraph = []
wfep_count = 0
places_with_count = dict()
topics_with_count = dict()
uncommon_count = 20
tfij_dict = dict()
N = 0
dft_dict = dict()
list_of_file_names = {"reut2-000.sgm"}

# ,"reut2-001.sgm","reut2-002.sgm","reut2-003.sgm","reut2-004.sgm","reut2-005.sgm",
#  "reut2-006.sgm","reut2-007.sgm","reut2-008.sgm","reut2-009.sgm","reut2-010.sgm","reut2-011.sgm","reut2-012.sgm",
#  "reut2-013.sgm","reut2-014.sgm","reut2-015.sgm","reut2-016.sgm","reut2-017.sgm","reut2-018.sgm","reut2-019.sgm",
#  "reut2-020.sgm","reut2-021.sgm"}
irrelevant_words = []
word_threshold = 10


#uncommon words
uncommon_name = "UNCOMMON_WORDS_LIST.txt"
new_uncommon_words_file = open(uncommon_name,"r")
new_uncommon_words = []
new_uncommon_words_temp = []
# for line in new_uncommon_words_file:
#     new_uncommon_words.append(line)
with open(uncommon_name,"r") as my_file:
    new_uncommon_words_temp = my_file.read().splitlines()
for w in new_uncommon_words_temp:
    if w.strip() not in new_uncommon_words:
        new_uncommon_words.append(w.strip())

#initialize dft_dict
for w in new_uncommon_words:
    dft_dict[w] = 0


uncommon_words_count_t = dict()
uncommon_words_count_p = dict()
dft_t = dict()
dft_p = dict()

z_topic_count = 0
z_place_count = 0




#return a list of words and their word count for each paragraphs
for file_name in list_of_file_names:

    all_places = []
    all_topics = []
    paragraphs = []
    paragraphs_unformatted = []
    all_places_unformatted = []
    all_topics_unformatted = []
    #newest shit
    #open file and read into string
    file = open(file_name,"r")
    content = file.read()
    #paragraphs,topics,and places
    all_p_t_B = re.findall(r'(<TOPICS>[\s\S]*?<\/BODY>)',content)
    #for each p,t,p grab p,t,and p
    for ptB in all_p_t_B:
        #body text
        body = re.findall(r'<BODY.*?>([\s\S]*?)</BODY>',ptB)
        paragraphs_unformatted.append(body)

        #place
        place = re.findall(r'<PLACES>(.*?)</PLACES>|<PLACES></PLACES>',ptB)

        if(len(place)>1):
            place = place[len(place)-1]
            #print("place: ",place)
        all_places_unformatted.append(place)

        #topic
        topic = re.findall(r'<TOPICS>(.*?)</TOPICS>|<TOPICS></TOPICS>',ptB)

        if(len(topic)>1):
            topic = topic[len(topic)-1]
        #t_arr = []
        #t_arr.append(topic)
        if(len(topic) != 0):
            all_topics_unformatted.append(topic)
        else:
            all_topics_unformatted.append(" ")


    #put unformatted places into all_places
    for topic in all_topics_unformatted:
        if(topic==''):
            topic = ['']
        topic = "".join(str(topic[0]))
        topic = re.findall(r"<D>(.*?)</D>|z",topic)
        t_string = ""
        if topic:
            for t in topic:
                t_string+=(t+",")
                #put into distinct topics list
                if t not in distinct_topics:
                    distinct_topics.append(t)
                    distinct_topics_and_empty.append(t)
                    distinct_topics_count[t] = 1
                else:
                    distinct_topics_count[t]+=1
        else:
            t_string = ("z"+str(z_topic_count))
            z_topic_count+=1
            distinct_topics_and_empty.append(t_string)
        all_topics.append(t_string)
    # print(all_topics)
    # print(len(all_topics))

    #put unformatted places into all_places
    for place in all_places_unformatted:

        if(place==''):
            place = ['']

        place = "".join(str(place[0]))
        place = re.findall(r"<D>(.*?)</D>|z",place)
        p_string = ""
        if place:
            for p in place:
                p_string+=(p+",")
                #put into distinct places list
                if p not in distinct_places:
                    distinct_places.append(p)
                    distinct_places_and_empty.append(p)
                    distinct_places_count[p] = 1
                else:
                    distinct_places_count[p]+=1

        else:
            p_string = ("z"+str(z_place_count))
            distinct_places_and_empty.append(p_string)
            z_place_count+=1

        all_places.append(p_string)
    #print("place: ",all_places)
    # print(len(all_places))

    #get each paragraph in file
    for p in paragraphs_unformatted:
        # p = str(p)
        # p = p.replace("\\n"," ")

        paragraphs.append(p[0])
        N+=1

    #end of newest shit

    #put each word in words list
    words = []
    paragraph_index = 0

    #keep adding to dft#*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*
    for place in distinct_places_and_empty:
        if place not in dft_p:
            temp = dict()
            for w in new_uncommon_words:
                temp[w] = 0
            dft_p[place] = temp
    for topic in distinct_topics_and_empty:
        if topic not in dft_t:
            temp = dict()
            for w in new_uncommon_words:
                temp[w] = 0
            dft_t[topic] = temp

    for paragraph in paragraphs:
        N+=1
        #*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&
        for p in all_places[paragraph_index].split(','):
            if ',' in p:
                p = p[0:len(p)-1]
            if p != '':
                for uw in new_uncommon_words:
                    if uw in paragraph.split():
                        dft_p[p][uw]+=1

        #*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&
        for t in all_topics[paragraph_index].split(','):
            if ',' in t:
                t = t[0:len(t)-1]
            if t != '':
                for uw in new_uncommon_words:
                    if uw in paragraph.split():
                        dft_t[t][uw]+=1


        words_copy = re.findall(r'\b([a-zA-Z]+)\b',paragraph)
        words.extend(words_copy)
        word_list.extend(words_copy)
        #arti

        #topics and places with word count
        if "PLACE: "+str(all_places[paragraph_index])+" TOPIC: "+ str(all_topics[paragraph_index]) not in topics_places_word_count:
            topics_places_word_count["PLACE: "+str(all_places[paragraph_index])+" TOPIC: "+ str(all_topics[paragraph_index])] = len(words_copy)
        else:
            topics_places_word_count["PLACE: "+str(all_places[paragraph_index])+" TOPIC: "+ str(all_topics[paragraph_index])] += len(words_copy)

        #topics and places with count for each word
        words_count_in_para = dict()
        for word in words_copy:
            word = word.lower()


            if word in words_count_in_para:
                words_count_in_para[word]+=1
            else:
                words_count_in_para[word] = 1
        if not(any("PLACE: "+str(all_places[paragraph_index])+" TOPIC: "+ str(all_topics[paragraph_index])in d for d in words_for_each_paragraph)):
            temp_dict = dict()
            temp_dict[("PLACE: "+str(all_places[paragraph_index])+" TOPIC: "+ str(all_topics[paragraph_index]))] = words_count_in_para
            words_for_each_paragraph.append(temp_dict)
        else:
             temp_dict = dict()
             cur_words_in_para = dict()
             #words count in paragraph
             temp_dict["PLACE: "+str(all_places[paragraph_index])+" TOPIC: "+ str(all_topics[paragraph_index])] = words_count_in_para
             dict_index = 0
             found = False
             while not found:
                 #print("index: ",dict_index)
                 dv = dict()
                 dv = words_for_each_paragraph[dict_index]

                 #found match
                 if "PLACE: "+str(all_places[paragraph_index])+" TOPIC: "+ str(all_topics[paragraph_index]) in dv:
                     #print("dv check: ",dv)
                     values = dv.get("PLACE: "+str(all_places[paragraph_index])+" TOPIC: "+ str(all_topics[paragraph_index]))
                     #print("values: ",values)
                     temp_dict = temp_dict.get("PLACE: "+str(all_places[paragraph_index])+" TOPIC: "+ str(all_topics[paragraph_index]))
                     #print("temp_dict: ", temp_dict)
                    # print(" ")
                     #merge values and temp_dict
                     a = {k: values.get(k,0)+temp_dict.get(k,0) for k in set(values)}
                     b =  dict()
                     b["PLACE: "+str(all_places[paragraph_index])+" TOPIC: "+ str(all_topics[paragraph_index])] = a

                     words_for_each_paragraph[dict_index] = b
                     #print("result: ",words_for_each_paragraph[dict_index])
                     #print(" ")
                     found = True
                 dict_index+=1


                 #if ("PLACE: "+str(all_places[paragraph_index])+" TOPIC: "+ str(all_topics[paragraph_index]) in dv


        paragraph_index += 1
        #loop through words in each paragraph
        # for word in words:
        #     words_for_each_paragraph[wfep_count]
        #     ["PLACE: "+all_places[paragraph_index]+" TOPIC: "+ all_topics[paragraph_index]] =


    d_words = []
    for word in words:
        #put in prefix tree if word is in english dictionary
        if d.check(word):
            word_count+=1
            TrieNode.add(root,word)
            d_words.append(word)
    words = []
    file.close()

    new_count = 0
    for word in d_words:
        words_count_dict[word] = (TrieNode.find_prefix(root,word)[1])

# for k,v in dft_p.items():
#     print(k)
#     for k2,v2 in v.items():
#         print(v2, end = ' ')
# print("\n\n\n\n\n\n\n")
# #
# for k,v in dft_t.items():
#     print(k)
#     for k2,v2 in v.items():
#         print(v2, end = ' ')


#irrelevant words
# for k,v in words_count_dict.items():
#     if v > word_threshold:
#         irrelevant_words.append(k)
#
# #print(irrelevant_words)
#
#
# #get places with count
# for place in distinct_places_and_empty:
#     for k, v in topics_places_word_count.items():
#         #print("k: ", places_with_count)
#         if place in k:
#             #add to count
#             if place not in places_with_count:
#                 places_with_count[place]=v
#             else:
#                 places_with_count[place]+=v
#
#
# #get topics with count
# for topic in distinct_topics_and_empty:
#     for k, v in topics_places_word_count.items():
#         if topic in k:
#             if topic not in topics_with_count:
#                 topics_with_count[topic]=v
#             else:
#                 topics_with_count[topic]+=v
#
# #dictionary of uncommon words for each places
# topics_uncommon_words = dict()
# #dictionary of uncommon words for each topic
# places_uncommon_words = dict()
#
# places_words_count = dict()
# topics_words_count = dict()
# # for place in distinct_places:
# #     places_words_count[place] = 0
# # for topic in distinct_topics:
# #     topics_words_count[topic] = 0
#
# #eric begin to put dictioanries(temp_irr_words_dict into uncommon_words_count_p
# for place in distinct_places_and_empty:
#     temp_irr_words_dict = dict()
#     for w in new_uncommon_words:
#         temp_irr_words_dict[w] = 0
#
#     uncommon_words_count_p[place] = temp_irr_words_dict
# #end focus on place
#
#
# for topic in distinct_topics_and_empty:
#     temp_irr_words_dict = dict()
#     for w in new_uncommon_words:
#         temp_irr_words_dict[w] = 0
#         tfij_dict[w] = 0
#     uncommon_words_count_t[topic] = temp_irr_words_dict
#
# #eric end to put dictioanries(temp_irr_words_dict into uncommon_words_count_p
#
# #get ditionary of most uncommon words for each topic and place
# for topic_place_list in words_for_each_paragraph:
#     #print(topic_place_list)
#     #k = PLACE: , TOPIC:
#     #v = {word: word_count}
#     for k,v in topic_place_list.items():
#         for topic in distinct_topics_and_empty:
#
#             #print(k,v)
#             #check if topic is in key
#             #add new words and count
#             if topic in k:
#                 if topic not in topics_words_count:
#                     topics_words_count[topic] = v
#                 #add words and count
#                 else:
#                     temp = dict()
#                     temp = v
#                     temp_merged =  {k: topics_words_count[topic].get(k,0)+temp.get(k,0) for k in set(topics_words_count[topic])|set(temp)}
#                     topics_words_count[topic] = temp_merged
#         for place in distinct_places_and_empty:
#             # if place=="cayman-islands":
#             #     print(v)
#             #     print("\n\n\n\n")
#             if place in k:
#                 if place not in places_words_count:
#                     places_words_count[place] = v
#
#                 else:
#                     temp = dict()
#                     temp = v
#                     temp_merged =  {k: places_words_count[place].get(k,0)+temp.get(k,0) for k in set(places_words_count[place])|set(temp)}
#                     places_words_count[place] = temp_merged
#
#
#
#
# #find top 10 words for each places
# for k,v in places_words_count.items():
#     uncommon = sorted(v.items(),key=operator.itemgetter(1))
#     uncommon_words = []
#     count = 0
#
#     for w,c in uncommon:
#
#         uncommon_words.append(w)
#         #new
#         if w in new_uncommon_words:
#             #print("w: ", w)
#             temp = {w:1}
#             temp2 = {}
#             place = k
#
#             if w in new_uncommon_words:
#
#                 if(place in distinct_places_count):
#                     uncommon_words_count_p[place][w] = c
#                 #in case it's an empty place
#                 else:
#                     uncommon_words_count_p[place][w] = c
#                 tfij_dict[w]+=c
#             count+=1
#             # print("\n\n\n\n")
# #ericericeric end
#
#
#
#     # print("\n")
#     i = 0
#     current_uncommon_count = 0
#     found = False
#     #get first item
#     if(len(uncommon)>0):
#         places_uncommon_words[k] = uncommon[0]
#     else:
#         places_uncommon_words[k] = None
#     #print("irr: ", uncommon[i])
#     while i<len(uncommon_words) and not found:
#         if(uncommon_words[i] not in irrelevant_words):
#             places_uncommon_words[k] = uncommon[i]
#             found = True
#             current_uncommon_count+=1
#         i+=1
#
#     while current_uncommon_count<uncommon_count and i<len(uncommon_words):
#         if(uncommon_words[i] not in irrelevant_words):
#             places_uncommon_words[k]+=uncommon[i]
#             current_uncommon_count+=1
#         i+=1
#
#
#
# #find top 10 words for topics
# for k,v in topics_words_count.items():
#     #v = {word:count}
#     #for k2,v2 in v.items():
#     uncommon = sorted(v.items(),key=operator.itemgetter(1))
#     if len(uncommon)>0:
#         topics_uncommon_words[k] = uncommon[0]
#     else:
#         topics_uncommon_words[k] = None
#     uncommon_words = []
#     topic = k
#     for w,c in uncommon:
#         uncommon_words.append(w)
#         if w in new_uncommon_words:
#             if w in new_uncommon_words:
#                 if topic in distinct_topics_count:
#                     uncommon_words_count_t[topic][w]=(c)
#                 else:
#                     uncommon_words_count_t[topic][w]=c
#
#     i = 0
#     current_uncommon_count = 0
#     found = False
#     #get first item
#     if len(uncommon)>0:
#         topics_uncommon_words[k] = uncommon[0]
#     else:
#         topics_uncommon_words[k] = None
#     #print("irr: ", uncommon[i])
#     while i<len(uncommon_words) and not found:
#         if(uncommon_words[i] not in irrelevant_words):
#             topics_uncommon_words[k] = uncommon[i]
#             found = True
#             current_uncommon_count+=1
#         i+=1
#
#     while current_uncommon_count<uncommon_count and i<len(uncommon_words):
#         if(uncommon_words[i] not in irrelevant_words):
#             topics_uncommon_words[k]+=uncommon[i]
#             current_uncommon_count+=1
#         i+=1

# print(tfij_dict)
# print("\n\n\n\n\n\n")
# print(dft_dict)
# print("\n\n\n\n\n\n\n")
# print(N)

    # i = 1
    # while i<uncommon_count and i<len(uncommon):
    #     topics_uncommon_words[k] += uncommon[i]
    #     i+=1

# print("count_p: ",distinct_places_count)
# print("count_t: ",distinct_topics_count)
#
# for w in new_uncommon_words:
#     print(w)
# print (len(new_uncommon_words))
#
# #
# #
# #
# for k,v in uncommon_words_count_p.items():
#     print(k)
#     for k2,v2 in uncommon_words_count_p[k].items():
#         print(v2, end=' ')
#
#     print("\n\n")
#
# print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
# #print (len(new_uncommon_words))
#
#
# for k,v in uncommon_words_count_t.items():
#     print(k)
#     for k2,v2 in uncommon_words_count_t[k].items():
#         print(v2,end=' ')
#     print("")
#     print(" ")
# print(len(new_uncommon_words))





######uncomment this when finding closest distance############################################
#CLASSIFYING PART OF CODE
k_test_value = 1
k_length = 1
average_topics_accuracy = 0
average_places_accuracy = 0
accuracy_topic_sum = 0
accuracy_places_sum = 0
while k_test_value<=k_length:
    #classifying topics
    topics_id_file_name = "TopicsIDReference.txt"
    places_id_file_name = "PlacesIDReference.txt"
    topics_distances_fname = "topics_distances_test.txt"
    places_distances_fname = "places_distances_test.txt"

    places_topics_ids = dict()
    #id closes neighbor id
    topics_closest_neighbor = dict()
    places_closes_neighbor = dict()
    file = open(topics_id_file_name,"r")
    content = file.readlines()

    #create dictionary of id of topic/place
    for line in content:
        result = line.split()
        places_topics_ids[result[0]] = result[1]
    #print(places_topics_ids)
    file.close()
    file = open(topics_distances_fname,"r")
    content = file.readlines()

    for line in content:

        #1:25334
        topics_id_distances = dict()
        temp_arr = line.split(',')
        id = int(temp_arr[0].strip('"'))

        curr_id = 1
        #create sorted dictionary with distances
        for i in temp_arr[1:]:
            topics_id_distances[curr_id] = float(temp_arr[curr_id])
            curr_id+=1

        topics_id_distances = sorted(topics_id_distances.items(), key=operator.itemgetter(1))
        #find min for z until it's not the id of an unknown place
        min_index = 0
        found = False
        i = 0
        while not found :
            #print(places_id_distances[i][0])
            #print((places_id_distances[i][0]))
            if 'z' not in places_topics_ids[str(topics_id_distances[i][0])] or 'zinc' in places_topics_ids[str(topics_id_distances[i][0])]:
                found = True
                topics_closest_neighbor[places_topics_ids[str(id)]] =  places_topics_ids[str(topics_id_distances[i][0])]
                #print(i)
            i+=1


    file.close()
    # #==============================================================
    #
    #
    places_topics_ids = dict()
    #id closes neighbor id
    places_closest_neighbor = dict()
    file = open(places_id_file_name,"r")
    content = file.readlines()

    #create dictionary of id of topic/place
    for line in content:
        result = line.split()
        places_topics_ids[result[0]] = result[1]
    #print(places_topics_ids)
    file.close()


    #classifying places
    file = open(places_distances_fname,"r")
    content = file.readlines()

    for line in content:

        #1:25334
        places_id_distances = dict()
        temp_arr = line.split(',')
        id = int(temp_arr[0].strip('"'))

        curr_id = 1
        #create sorted dictionary with distances
        for i in temp_arr[1:]:
            places_id_distances[curr_id] = float(temp_arr[curr_id])
            curr_id+=1

        places_id_distances = sorted(places_id_distances.items(), key=operator.itemgetter(1))
        #find min for z until it's not the id of an unknown place
        min_index = 0
        found = False
        i = 0
        while not found :
            #print(places_id_distances[i][0])
            #print((places_id_distances[i][0]))
            if 'z' not in places_topics_ids[str(places_id_distances[i][0])] or 'zambia' in places_topics_ids[str(places_id_distances[i][0])] or'zimbabwe' in places_topics_ids[str(places_id_distances[i][0])] or 'zaire' in places_topics_ids[str(places_id_distances[i][0])]:
                found = True
                places_closest_neighbor[places_topics_ids[str(id)]] =  places_topics_ids[str(places_id_distances[i][0])]
                #print(i)
            i+=1

    topics_correct = 0
    places_correct = 0
    total_topics = len(topics_closest_neighbor)
    total_places = len(places_closest_neighbor)
    print("topics closest neighbors: ")
    for k,v in topics_closest_neighbor.items():
        if(k==v):
            topics_correct +=1
        print(k,v)
    print("\n\n\n\n\n\n\n")
    print("places closest neighbors")
    for k,v in places_closest_neighbor.items():
        if(k==v):
            places_correct +=1
        print(k,v)
    print("K:",k_test_value)
    print ("TOPICS ACCURACY: ",topics_correct/total_topics)
    print ("PLACES ACCURACY: ",places_correct/total_places)
    print("TOPICS ERROR: ", 1-(topics_correct/total_topics))
    print("PLACES ERROR: ", 1-(places_correct/total_places))
    accuracy_topic_sum+=(topics_correct/total_topics)
    accuracy_places_sum+=(places_correct/total_places)

    k_test_value+=1
print("\n\n\n\n\n\n\n\n\n\n")
average_places_accuracy = accuracy_places_sum/k_length
average_topics_accuracy = accuracy_topic_sum/k_length

print("AVERAGE PLACES ACCURACY: ", average_places_accuracy)
print("AVERAGE TOPICS ACCURACY: ",average_topics_accuracy)


######uncomment this when finding closest distance##################################################


    #print("\n\n\n\n\n\n\n\n")

# for line in content:
#     temp_arr = line.split(',')
#     id = temp_arr[0]
#     id = int(id.strip('"'))
#     print(places_topics_ids[str(id)])
#     temp_arr = temp_arr[1:]
#     del temp_arr[id-1]
#     temp_arr = [float(i) for i in temp_arr]
#     z_neighbor_found = False
#     while(z_neighbor_found)
#     #find closes neighbor
#     min_index = temp_arr.index(min(temp_arr))
#     actual_id = min_index
#     print(min_index)
#     if(id>min_index):
#         actual_id = min_index-1
#     actual_id = actual_id+1
#     places_closest_neighbor[places_topics_ids[str(id)]] =  places_topics_ids[str(actual_id)]


#print("\n\n\n\n\n\n\n")
#print(places_closest_neighbor)

# print(irrelevant_words)
#
# test_word_count = 0
# print("topics_places_word_count: ")
# for k, v in topics_places_word_count.items():
#     print (k, ": ",v)
#     test_word_count+=v
# print(" ")
#
# print("words with count: ")
# for k, v in words_count_dict.items():
#     new_count+=1
#     print (k, ": ",v)
# print(" ")
#
# print("words for each paragraph: ")
# for topic_list in words_for_each_paragraph:
#     print("topic_list: ",topic_list)
#     print(" ")
# print(" ")
#
# print("places_uncommon: ")
# for k,v in places_uncommon_words.items():
#     print (k,":",v)
#     print(" ")
# print(" ")
# #
# print("topics_uncommon")
# for k,v in topics_uncommon_words.items():
#     print (k,":",v)
#     print(" ")
#
#
# #get count of each topic and each places
#
# print("distinct_places count: ",len(distinct_places))
# print("distinct_topics count: ",len(distinct_topics))
# print("distinct places: ", distinct_places)
# print("distinct topics: ", distinct_topics)
# print ("Places with count: ",places_with_count)
# print ("Topics with count: ",topics_with_count)
# print("topics_places_word_count: ",test_word_count)
# print("unique word count: ",new_count)
# print("word count: ",word_count)
# print("empty places: ", np_places_count)
# print("empty topics: ", nt_topics_count)
print("N: ",N)
