
from typing import Tuple



class TrieNode(object):

    def __init__(self,char: str):
        self.char = char
        self.children = []
        self.word_finished = False
        #full word will have a count greater than 0
        self.count = 0

    #adds word to prefix tree
    def add(root, word: str):
        node = root
        for char in word:
            found_in_children = False
            for child in node.children:
                #child node matches char
                if child.char==char:
                    node = child
                    found_in_children = True
                #child node doesn't match char
                #add new node and append it to the current node
            if not found_in_children:
                new_node = TrieNode(char)
                node.children.append(new_node)
                node = new_node
        #counter of the last node(last character of word) is the only
        #node that should get incremented
        node.count+=1

    #returns false if prefix is not found in TrieNode
    #returns true if prefix is found in TrieNode
    def find_prefix(root,prefix: str):
        curr_node = root

        #iterate through chars in str prefix
        for char in prefix:
            char_not_found = True
            #look for char in children of node
            for child in curr_node.children:

                # char found in children
                if child.char==char:

                    char_not_found = False
                    curr_node = child
                    break
            if char_not_found:
                return False,0

        #prefix found , return True, count of prefix
        return True, curr_node.count
