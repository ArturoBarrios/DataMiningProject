from TrieNode import TrieNode

root = TrieNode('*')
TrieNode.add(root,"Arturo")
TrieNode.add(root,'Jewric')
TrieNode.add(root,'B')
TrieNode.add(root,'B')
TrieNode.add(root,'Mike')
TrieNode.add(root,'Mike')
TrieNode.add(root,'big boy')
TrieNode.add(root,'Mike')
TrieNode.add(root,"Arturo")


#testing count and whether they exist
print(TrieNode.find_prefix(root,'Arturo'))
print(TrieNode.find_prefix(root,'Jewric'))
print(TrieNode.find_prefix(root,'B'))
print(TrieNode.find_prefix(root,'Mike'))
print(TrieNode.find_prefix(root,'big boy'))

#testing whether part of prefix can be found
print(TrieNode.find_prefix(root,'Art'))
print(TrieNode.find_prefix(root,'Jew'))
print(TrieNode.find_prefix(root,'Mi'))
print(TrieNode.find_prefix(root,'b'))
print(TrieNode.find_prefix(root,'Artur'))

print("everything above should be true")
print("everything below should be false")
#testing whether they don't exist
print(TrieNode.find_prefix(root,'Arti'))
print(TrieNode.find_prefix(root,'Jews'))
print(TrieNode.find_prefix(root,'C'))
print(TrieNode.find_prefix(root,'Miks'))
print(TrieNode.find_prefix(root,'big girl'))

TrieNode.all_words_count(root)
