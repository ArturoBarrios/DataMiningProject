import re
import urllib.parse
from TrieNode import TrieNode
import enchant

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

list_of_file_names = {"reut2-000.sgm"}
#go through every file
for file_name in list_of_file_names:
    #open file and read into string
    file = open(file_name,"r")
    content = file.read()
    #get empty places tags
    empty_places = re.findall(r'<PLACES>()</PLACES>',content)
    np_places_count += len(empty_places)

    empty_topics = re.findall(r'TOPICS>()</TOPICS>',content)

    nt_topics_count += len(empty_topics)


    #find all unique places
    places = re.findall(r'<PLACES>(.*?)</PLACES>',content)
    places = ''.join(str(e) for e in places)
    places = re.findall(r'<D>(.*?)</D>',places)

    #put places in prefix tree
    for place in places:
        TrieNode.add(root,place)
        if place not in distinct_places:
            distinct_places.append(place)


    #find all unique TOPICS
    topics = re.findall(r'<TOPICS>(.*?)</TOPICS>',content)
    topics = ''.join(str(e) for e in topics)
    topics = re.findall(r'<D>(.*?)</D>',topics)

    #put topics in prefix tree
    for topic in topics:
        TrieNode.add(root,topic)
        if topic not in distinct_topics:
            distinct_topics.append(topic)

    #get each paragraph in <BODY> tag
    paragraphs = re.findall(r'<BODY.*?>([\s\S]*?)</BODY>',content)
    #put each word in words list
    words = []
    for paragraph in paragraphs:
        words_copy = re.findall(r'\b([a-zA-Z]+)\b',paragraph)
        words.extend(words_copy)
        word_list.extend(words_copy)

    for word in words:
        #put in prefix tree if word is in english dictionary
        if d.check(word):
            word_count+=1
            TrieNode.add(root,word)
    words = []
    file.close()
        #check if string is word


print("empty places: ", np_places_count)
print("empty topics: ", nt_topics_count)
print("distinct places: ", distinct_places)
print("distinct topics: ", distinct_topics)
print("word count: ",word_count)
