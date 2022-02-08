# To Handle 
- Priority Ordering should be updated with ` decrease_key() ` which is not supported in heapq. I should use my own heapm and implement the necessary functions.
        - `push()` should return the index pushed
        - `decrease_key()` should decrease the element in the given index 

-`two_n_directional_neighbors_in_n_d_space` only handles cases where the target is on the other corner. 

# Bottlenecks
(75x75)
A_Star took 0.015575466156005859 for 14 tests 100 times with the giant matrix
 with a hashset for queue checks.
It took 0.015471618175506591 for 14 tests 100 times with the same giant with list lookup.

(100x100)
0.027578718662261963 for giant (99, 99) 14 tests 100 times. (priority_queue lookup)
0.028038556575775146 for giant (99, 99) 14 tests 100 times. (set lookup)