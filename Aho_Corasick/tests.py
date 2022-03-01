from trie import *
from sys import path 
path.append("..")
from pretty_ux import *


def test_add(trie=None, words = None):
        if not trie:trie = TrieNode()
        if not words : words = ["hack", "hak", "hac"]
        for w in words:
                add(trie, w)

        print_trie(trie)

def test_find(trie, words):
        # print(F"We have {words} ")
        for w in words:
                result = find(trie, w)
                print(f"{w} \t\t { SUCCESS if result else FAIL} ")
                result = find(trie, w[1:])
                print(f"{w[1:]} \t\t { SUCCESS if result else FAIL} ")

def test_del(trie, words):
        for w in words:
                _, trie = delete(trie, w)
                print(f"{w} deletion :  \t { SUCCESS if _ else FAIL} " )

if __name__ == "__main__":
        trie = TrieNode()
        words = ["hack", "hak", "hac"]
        test_add(trie, words)
        test_find(trie, words)
        test_del(trie, ["hak"])
        test_find(trie, words)
