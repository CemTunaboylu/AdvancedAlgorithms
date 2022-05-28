from aho_corasick import *
from sys import path
path.append("..")
from pretty_ux import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

CHECK_MARK =  u'\N{heavy check mark}'
SUCCESS = f"{bcolors.OKGREEN}" + CHECK_MARK + f"{bcolors.ENDC}" # Success 
FAIL = u'\N{cross mark}' # Fail

def ac_trie_add_test(ac_trie, words=None, verbose=False):
        if not words:
                words = [ "he", "she", "his", "hers" ]
        for w in words:
                ac_trie.add_seq(w)
        if verbose:
                print_ac(ac_trie)

def print_ac(ac):
        ACAutomaton.print_automaton(ac_trie.initial_state, "")
        for char, child in ac.initial_state:
                print(f"{char}: {child}")


def ac_trie_find_test(ac_trie=None, words=None):
        if not words:
                words = [ "he", "she", "his", "hers" ]

        for w in words:
                r = ac_trie.find_seq(w)
                print(f"{w} \t\t {SUCCESS if r else FAIL}")
                r = ac_trie.find_seq(w[1:])
                print(f"{w[1:]} \t\t {SUCCESS if r else FAIL}")

def ac_trie_delete_test(ac_trie=None, words=None):
        if not words:
                words = [ "she","hers" ]
        for w in words:
                r = ac_trie.del_seq(w)
                print(f"{w} is gone \t\t {SUCCESS if r else FAIL}")

        ac_trie_find_test(ac_trie)

def faillink_test(ac_trie, words = [ "he", "she", "his", "hers" ]):
        ac_trie.form_faillinks()
        f_links = set()
        for w in words:
                marcher = ac_trie.initial_state
                for s in w:
                        f_links.add( (s, marcher[s].id, marcher[s].fail_link.id) )
                        marcher = marcher[s]
        for fl in f_links:
                s, i, f_id = fl
                print(f"faillink of {s}({i}) :  is {f_id} ") 


if __name__ == "__main__":
        ac_trie = ACAutomaton()
        ac_trie_add_test(ac_trie)
        # ACAutomaton.print_automaton(ac_trie.initial_state)
        # ac_trie_find_test(ac_trie)
        # ac_trie_delete_test(ac_trie)
        faillink_test(ac_trie)        
