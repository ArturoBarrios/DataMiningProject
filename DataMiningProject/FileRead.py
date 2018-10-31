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
topics_places_word_count = dict()
words_count_dict = dict()
words_for_each_paragraph = []
wfep_count = 0
places_with_count = dict()
topics_with_count = dict()
uncommon_count = 20
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

uncommon_words_count_t = dict()
uncommon_words_count_p = dict()





#return a list of words and their word count for each paragraphs
for file_name in list_of_file_names:

    all_places = []
    all_topics = []
    #open file and read into string
    file = open(file_name,"r")
    content = file.read()
    #get empty places tags
    #empty_places = re.findall(r'<PLACES>()</PLACES>',content)

    #np_places_count += len(empty_places)

    #empty_topics = re.findall(r'TOPICS>()</TOPICS>',content)
    #nt_topics_count += len(empty_topics)
    #find all unique places
    places = re.findall(r'<PLACES>(.*?)</PLACES>|<PLACES></PLACES>',content)

    places_new = ""

    for e in places:
        if e == '':
            places_new+="z"
        else:
            places_new += e

    #recently added
    index = 0
    while index<len(places):
        temp_places = "".join(str(places[index]))
        places[index] = re.findall(r"<D>(.*?)</D>|z",temp_places)
        index+=1

    #recently added

    #places = "".join(str(e) for e in places_new)

    #places = re.findall(r"<D>(.*?)</D>|z",places)
    #print ("all_places: ", places)

    #put places in prefix tree
    for place in places:
        if place:
            p_string = ""
            for p in place:
                p_string+=(p+",")
                TrieNode.add(root,p)
                if p not in distinct_places:

                    distinct_places.append(p)
            all_places.append(p_string);
        else:
            np_places_count+=1
            all_places.append("")


    #find all unique TOPICS
    topics = re.findall(r'<TOPICS>(.*?)</TOPICS>|<TOPICS></TOPICS>',content)
    topics_new = ""
    for e in topics:
        if e == '':
            topics_new+="z"
        else:
            topics_new += e

    #recently added
    index = 0
    while index<len(topics):
        temp_topics = "".join(str(topics[index]))
        topics[index] = re.findall(r"<D>(.*?)</D>|z",temp_topics)
        index+=1
    #recently added
    #topics = "".join(str(e) for e in topics_new)
    #topics = re.findall(r"<D>(.*?)</D>|z",topics)

    #put topics in prefix tree
    for topic in topics:
        if topic:
            t_string = ""
            for t in topic:
                t_string+=(t+",")
                TrieNode.add(root,topic)
                if t not in distinct_topics:
                    distinct_topics.append(t)
            all_topics.append(t_string)
        else:
            nt_topics_count+=1
            all_topics.append("")


    #get each paragraph in <BODY> tag
    paragraphs = re.findall(r'<BODY.*?>([\s\S]*?)</BODY>',content)
    #put each word in words list
    words = []
    paragraph_index = 0
    for paragraph in paragraphs:
        words_copy = re.findall(r'\b([a-zA-Z]+)\b',paragraph)
        words.extend(words_copy)
        word_list.extend(words_copy)
        #topics and places with word count
        if "PLACE: "+str(all_places[paragraph_index])+" TOPIC: "+ str(all_topics[paragraph_index]) not in topics_places_word_count:
            topics_places_word_count["PLACE: "+str(all_places[paragraph_index])+" TOPIC: "+ str(all_topics[paragraph_index])] = len(words_copy)
        else:
            topics_places_word_count["PLACE: "+str(all_places[paragraph_index])+" TOPIC: "+ str(all_topics[paragraph_index])] += len(words_copy)

        #topics and places with count for each word
        words_count_in_para = dict()
        for word in words_copy:
            word = word.lower()

            #get TOPIC: [uword: word:count,word2:count,....wordn:count
                  #uword2: word:count,word2:count,....wordn:count]
            # if(word in new_uncommon_words):
            #     print("yaiiii")
            #
            #     values_temp = dict()
            #     values_temp[word] = 1
            #     for w,c in uncommon_words
                # a = {k: values.get(k,0)+temp_dict.get(k,0) for k in set(values_temp)}
                # uncommon_words_count["TOPIC: "+str(all_topics[paragraph_index])] =

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

#irrelevant words
for k,v in words_count_dict.items():
    if v > word_threshold:
        irrelevant_words.append(k)

#print(irrelevant_words)


#get places with count
for place in distinct_places:
    for k, v in topics_places_word_count.items():
        #print("k: ", places_with_count)
        if place in k:
            #add to count
            if place not in places_with_count:
                places_with_count[place]=v
            else:
                places_with_count[place]+=v


#get topics with count
for topic in distinct_topics:
    for k, v in topics_places_word_count.items():
        if topic in k:
            if topic not in topics_with_count:
                topics_with_count[topic]=v
            else:
                topics_with_count[topic]+=v

#dictionary of uncommon words for each places
topics_uncommon_words = dict()
#dictionary of uncommon words for each topic
places_uncommon_words = dict()

places_words_count = dict()
topics_words_count = dict()
# for place in distinct_places:
#     places_words_count[place] = 0
# for topic in distinct_topics:
#     topics_words_count[topic] = 0

#eric begin to put dictioanries(temp_irr_words_dict into uncommon_words_count_p
temp_irr_words_dict = dict()
for w in new_uncommon_words:
    temp_irr_words_dict[w] = 0
for place in distinct_places:
    t = dict()
    t = temp_irr_words_dict
    uncommon_words_count_p[place] = t
for topic in distinct_topics:
    t = dict()
    t = temp_irr_words_dict
    uncommon_words_count_t[topic] = t
#eric end to put dictioanries(temp_irr_words_dict into uncommon_words_count_p

#get ditionary of most uncommon words for each topic and place
for topic_place_list in words_for_each_paragraph:

    #k = PLACE: , TOPIC:
    #v = {word: word_count}
    for k,v in topic_place_list.items():
        for topic in distinct_topics:


            #check if topic is in key
            #add new words and count
            if topic in k:
                if topic not in topics_words_count:
                    topics_words_count[topic] = v
                #add words and count
                else:
                    temp = dict()
                    temp = v
                    temp_merged =  {k: topics_words_count[topic].get(k,0)+temp.get(k,0) for k in set(topics_words_count[topic])}
                    topics_words_count[topic] = temp_merged
        for place in distinct_places:


            if place in k:

                if place not in places_words_count:
                    places_words_count[place] = v
                else:
                    temp = dict()
                    temp = v
                    temp_merged =  {k: places_words_count[place].get(k,0)+temp.get(k,0) for k in set(places_words_count[place])}
                    places_words_count[place] = temp_merged


#find top 10 words for each places
for k,v in places_words_count.items():

    #v = {word:count}
    #for k2,v2 in v.items():
    uncommon = sorted(v.items(),key=operator.itemgetter(1))
    uncommon_words = []
    place = k
    # print(uncommon)
    # print("\n")
    for w,c in uncommon:
        uncommon_words.append(w)
        #new
        if w in new_uncommon_words:
            #print("w: ", w)
            temp = {w:1}
            temp2 = {}

            #temp2 = dict()

            #print(temp2)
            # print("\n\n\n\n")
            # print("temp: ",temp)
            # print("\n")
            # print("places_wordds_count: ",uncommon_words_count_p[place])
            # print("\n\n\n\n")
#eric begin
            uncommon_words_count_p[place] = {k2: uncommon_words_count_p[place].get(k2,0)+temp.get(k,0) for k2 in set(uncommon_words_count_p[place])|set(temp)}

            # print("\n\n\n\n")
#eric end



    # print("\n")
    i = 0
    current_uncommon_count = 0
    found = False
    #get first item
    places_uncommon_words[k] = uncommon[0]
    #print("irr: ", uncommon[i])
    while i<len(uncommon_words) and not found:
        if(uncommon_words[i] not in irrelevant_words):
            places_uncommon_words[k] = uncommon[i]
            found = True
            current_uncommon_count+=1
        i+=1

    while current_uncommon_count<uncommon_count and i<len(uncommon_words):
        if(uncommon_words[i] not in irrelevant_words):
            places_uncommon_words[k]+=uncommon[i]
            current_uncommon_count+=1
        i+=1



#find top 10 words for topics
for k,v in topics_words_count.items():
    #v = {word:count}
    #for k2,v2 in v.items():
    uncommon = sorted(v.items(),key=operator.itemgetter(1))
    topics_uncommon_words[k] = uncommon[0]
    uncommon_words = []
    topic = k
    for w,c in uncommon:
        uncommon_words.append(w)

        if w in new_uncommon_words:
        #     #print("w: ", uncommon_words_count_p[k])
        #     temp = dict()
        #     temp[w] = 1
        #     temp_merged = {k: uncommon_words_count_t[topic].get(k,0)+temp.get(k,0) for k in set(uncommon_words_count_t[topic])}
            uncommon_words_count_t[topic][w] += 1
    i = 0
    current_uncommon_count = 0
    found = False
    #get first item
    topics_uncommon_words[k] = uncommon[0]
    #print("irr: ", uncommon[i])
    while i<len(uncommon_words) and not found:
        if(uncommon_words[i] not in irrelevant_words):
            topics_uncommon_words[k] = uncommon[i]
            found = True
            current_uncommon_count+=1
        i+=1

    while current_uncommon_count<uncommon_count and i<len(uncommon_words):
        if(uncommon_words[i] not in irrelevant_words):
            topics_uncommon_words[k]+=uncommon[i]
            current_uncommon_count+=1
        i+=1

    # i = 1
    # while i<uncommon_count and i<len(uncommon):
    #     topics_uncommon_words[k] += uncommon[i]
    #     i+=1

#topic
# for w in new_uncommon_words:
#     print(w)
# print (len(new_uncommon_words))
#
#


# for k,v in uncommon_words_count_p.items():
#     #print(k,v)
#     for k2,v2 in uncommon_words_count_p[k].items():
#         #print(k2,v2)
#         if(v2>0):
#             print(k2,v2,end=' ')
#     print("\n")
#
# print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
#
# for k,v in uncommon_words_count_t.items():
#     #print(k,v)
#     for k2,v2 in uncommon_words_count_t[k].items():
#         print(v2,end=' ')
#     print("")
    #print(" ")

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
