import re
import urllib.parse
from TrieNode import TrieNode
import enchant

#will be used to check if string is a word
d = enchant.Dict("en_US")

#root of TrieNode
root = TrieNode('*')

np_entries_count = 0
nt_entries_count = 0
word_count = 0


list_of_file_names = {"reut2-001.sgm"}
#"reut2-001.sgm","reut2-002.sgm","reut2-003.sgm","reut2-004.sgm","reut2-005.sgm",
#"reut2-006.sgm","reut2-007.sgm","reut2-008.sgm","reut2-009.sgm","reut2-010.sgm","reut2-011.sgm","reut2-012.sgm",
#"reut2-013.sgm","reut2-014.sgm","reut2-015.sgm","reut2-016.sgm","reut2-017.sgm","reut2-018.sgm","reut2-019.sgm",
#"reut2-020.sgm","reut2-021.sgm

#go through every file
for file_name in list_of_file_names:
    print("file count: ",word_count)
    word_count+=1
    #open file and read into string
    file = open(file_name,"r")
    content = file.read()


    #get empty places tags
    empty_places = re.findall(r'<PLACES>()</PLACES>',content)
    print ("Empty PLACES tag: ", len(empty_places))

    empty_topics = re.findall(r'TOPICS>()</TOPICS>',content)
    print ("Empty TOPICS tag: ", len(empty_topics))


    #find all unique places
    places = re.findall(r'<PLACES>(.*?)</PLACES>',content)
    places = ''.join(str(e) for e in places)
    places = re.findall(r'<D>(.*?)</D>',places)
    print ("unique places: ", len(places))
    #put places in prefix tree
    for place in places:
        TrieNode.add(root,place)

    #find all unique TOPICS
    topics = re.findall(r'<TOPICS>(.*?)</TOPICS>',content)
    topics = ''.join(str(e) for e in topics)
    topics = re.findall(r'<D>(.*?)</D>',topics)
    print ("unique topics: ", len(topics))
    #put topics in prefix tree
    for topic in topics:
        TrieNode.add(root,topic)

    #get each paragraph in <BODY> tag
    paragraphs = re.findall(r'<BODY.*?>([\s\S]*?)</BODY>',content)
    #put each word in words list
    words = []
    for paragraph in paragraphs:
        words_copy = re.findall(r'\b([a-zA-Z]+)\b',paragraph)
        words.extend(words_copy)

    for word in words:
        #put in prefix tree if word is in english dictionary
        if d.check(word):
            word_count+=1
            TrieNode.add(root,word)

        #check if string is word

    print("word count: ",word_count)


    file.close()
