# Bottlenecks
(75x75)
A_Star took 0.015575466156005859 for 14 tests 100 times with the giant matrix
 with a hashset for queue checks.
It took 0.015471618175506591 for 14 tests 100 times with the same giant with list lookup.

(100x100)
0.027578718662261963 for giant (99, 99) 14 tests 100 times. (priority_queue lookup)
0.028038556575775146 for giant (99, 99) 14 tests 100 times. (set lookup)