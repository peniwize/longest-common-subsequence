# Start of "solution.py".

from collections import deque
import inspect
import time
from typing import List
from typing import Optional
from typing import Set

"""
    Given two strings text1 and text2, return the length of their longest 
    common subsequence. If there is no common subsequence, return 0.

    A subsequence of a string is a new string generated from the original 
    string with some characters (can be none) deleted without changing the 
    relative order of the remaining characters.

        * For example, "ace" is a subsequence of "abcde".
    
    A common subsequence of two strings is a subsequence that is common to 
    both strings.

    Constraints:

        * 1 <= text1.length, text2.length <= 1000
        * text1 and text2 consist of only lowercase English characters.
"""

"""
"""
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        #
        # TODO: >>> Under Construction <<<
        #
        return -1

def test1(solution):
    text1 = "abcde"
    text2 = "ace"
    expected = 3
    startTime = time.time()
    result = solution.longestCommonSubsequence(text1, text2)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

def test2(solution):
    text1 = "abc"
    text2 = "abc"
    expected = 3
    startTime = time.time()
    result = solution.longestCommonSubsequence(text1, text2)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

def test3(solution):
    text1 = "abc"
    text2 = "def"
    expected = 0
    startTime = time.time()
    result = solution.longestCommonSubsequence(text1, text2)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

if "__main__" == __name__:
    test1(Solution())

    test2(Solution())

    test3(Solution())

# End of "solution.py".
