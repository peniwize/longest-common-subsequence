# Start of "solution.py".

from collections import deque
import copy
import inspect
import time
from typing import List
from typing import Optional
from typing import Set

"""
    https://github.com/peniwize/longest-common-subsequence.git
    https://leetcode.com/problems/longest-common-subsequence/
    
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
    This solution tests the hypothesis that the solution is to find the 
    first largest combination of text1 and text2 that matches and return
    the length of that combination.

    Time = O(n*2**m)
           m: len(text2)
           n: len(text1)
           * note: text1 is the shorter of the two.

    Space = O(2**n+n) => O(2**n)
            2**n: cache storing all combinations for (n choose k).
            n: call stack depth when calculating n choose k combinations.
"""
class Solution1_BruteForce:
    def genCombos(self, combos: set, text: str, k: int, I: int, combo: List):
        if len(combo) == k:
            combos.add("".join(combo))
            return
        if len(text) == I:
            return
        for i in range(I, len(text)):
            combo.append(text[i])
            self.genCombos(combos, text, k, i + 1, combo)
            del combo[len(combo) - 1]
    
    def findAnyCombo(self, combos: set, text: str, k: int, I: int, combo: List) -> bool:
        if len(combo) == k:
            return "".join(combo) in combos
        if len(text) == I:
            return False
        for i in range(I, len(text)):
            combo.append(text[i])
            if self.findAnyCombo(combos, text, k, i + 1, combo):
                return True
            del combo[len(combo) - 1]
        return False
    
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        if len(text2) < len(text1):
            text1, text2 = text2, text1
        
        for k in range(len(text1), 0, -1):
            combos = set()
            self.genCombos(combos, text1, k, 0, [])
            if self.findAnyCombo(combos, text2, k, 0, []):
                return k

        return 0

"""
    This solution implementes a recurrence relation that will visit every 
    combination of elements BETWEEN the sequences.  Since the idea is to 
    visit every possible sub-sequence in each sequence and find the longest 
    one that exists in both sequences, this algoithm works its way down to
    the smallest sub-sequences (of size one) in each sequence, determines
    the sub-sequence length (1 if they match; 0 if they don't), and then 
    returns that value to be used in the next larger sub-sequence (of size 
    two) size calculation.  This works because each sub-sequence is composed
    of nested sub-sequences so only one [new] element must be compared in 
    each recursive step.  All other elements of the sub-sequence will have 
    already been analyzed and the result of their comparisons returned by the
    preceeding recursive steps.  The preceeding isn't a great explanation,
    however the following examples and implementation will help.
    
    TODO: I need to better explain how visiting every combination of elements
          BETWEEN the sequences effectively visits every combination of 
          elements in each sequence.

    Example 1:
    
    Seq a) A B C
    Seq b) X Y Z

    This example shows how ALL combinations are produced when / because
    NO elements match.  Each level of indentation corresponds to a 
    recursive call.  These are the combinations that are produced:

        AX
            BX
                CX
                CY
                CZ
            BY
                CY
                CZ
            BZ
                CZ
        AY
            BY
                CY
                CZ
            BZ
                CZ
        AZ
            BZ
                CZ

    Each sequence ('a' and 'b' above) has an element index that starts at 
    zero and is strategically incremented in order to produce the combinations.
    (The code below actually creates subsequences via splicing rather than 
    using indexes, but the effect is exactly the same.)
    When the two elements don't match, the recursion occurs twice in order to
    visit every combination from [sequence 'a', less one element, 
    and sequence 'b'] and [sequence 'b', less one element, and sequence 'a'].

    Example 2:

    Seq a) A B C
    Seq b) D A C

    This example shows how the element indexes in both sequences are advanced 
    when the elements match.  Combination 'CC' doesn't show this because 'C' 
    is at the end of the sequence so there is nowhere to advance.
    Combination 'AA' shows that the next combination produced is 'BC' rather
    than 'BA', which would have been produced if they hadn't matched.

    AD
        BD
            CD
            CA
            CC  <-- *match* (at end of sequence so cannot move ahead)
        BA
            CA
            CC  <-- *match* (at end of sequence so cannot move ahead)
        BC
            CC  <-- *match* (at end of sequence so cannot move ahead)
    AA          <-- *match*; _SKIP_ TO NEXT ELEMENT IN _BOTH_ SEQUENCES.
        BC
            CC  <-- *match* (at end of sequence so cannot move ahead)
    AC
        BC
            CC  <-- *match* (at end of sequence so cannot move ahead)

    See previous solutions for context.

    ChatGPT explains the worst case complexity analysis very well:

    "The exact worst-case time complexity is difficult to express in a simple 
     closed form due to the nature of the recursive calls, but it's evident 
     that the growth rate is exponential. To give a more precise figure, 
     consider the number of possible subsequences of text1 combined with the 
     number of possible subsequences of text2. Since there are 2**n possible 
     subsequences for a string of length n (each element can either be 
     included or excluded), the total number of operations involves examining 
     all pairs of subsequences from the two strings, leading to 2**n * 2**m
     = 2**[n+m] operations in the worst case."

    "Thus, the worst-case time complexity is O(2**[n+m]), which occurs when 
     there are no common elements between text1 and text2, as this forces the 
     exploration of all possible subsequence pairs without any early 
     termination due to matching elements."

    "The space complexity is primarily determined by the depth of the 
     recursive call stack and the space needed to store the intermediate 
     string slices. In the worst case, the maximum depth of the recursive 
     call stack is n+m, as the function could be called recursively reducing 
     one character at a time from either text1 or text2 until both strings 
     are empty."
    
    Time = O(2**[m+n])
           m = len(text1)
           n = len(text2)

    Space = O(m+n)  [maximum call stack depth]
"""
class Solution2_BruteForce:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # Return zero when the end of either sequence is reached.
        # The LCS must be zero in the case because one contains no elements.
        if 0 == len(text1) or 0 == len(text2):
            return 0
        
        # Return the LCS of the sub-sequences of each sequence PLUS ONE (for the match).
        # The sub-sequences exlcude the matching element from each sequence.
        if text1[len(text1)-1] == text2[len(text2)-1]:
            return 1 + self.longestCommonSubsequence(text1[:len(text1)-1], text2[:len(text2)-1])
        
        # Return the length of the larger of the two LCS's that are produced 
        # from each sequence.  The first LCS is calculated from the first 
        # sequence, less the element that didn't match, and the second 
        # sequence.  The second LCS is calculated from the second sequence, 
        # less the element that didn't match, and the first sequence.
        c = self.longestCommonSubsequence(text1[:len(text1)-1], text2)
        d = self.longestCommonSubsequence(text1, text2[:len(text2)-1])
        return max(c, d)

"""
    Equivalent to Solution2_BruteForce except first characters are compared
    rather than last characters.  This proves it doesn't matter whether 
    combinations are produced from right to left or left to right.
    See previous solutions for context.

    Time = O(2**[m+n])
           m = len(text1)
           n = len(text2)

    Space = O(m+n)  [maximum call stack depth]
"""
class Solution3_BruteForce:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        if 0 == len(text1) or 0 == len(text2):
            return 0
        if text1[0] == text2[0]:
            return 1 + self.longestCommonSubsequence(text1[1:], text2[1:])
        c = self.longestCommonSubsequence(text1[1:], text2)
        d = self.longestCommonSubsequence(text1, text2[1:])
        return max(c, d)

"""
    Top down DP approach.
    Equivalent to Solution3_BruteForce except the result of each character 
    combination is cached / reused rather than being recalculated every time.
    This prevents 'CC', 'BC' and 'CA', in the example below, from being
    recalculated multiple times.

    Example 2:

    Seq a) A B C
    Seq b) D A C

    This example shows how the element indexes in both sequences are advanced 
    when the elements match.  Combination 'CC' doesn't show this because 'C' 
    is at the end of the sequence so there is nowhere to advance.
    Combination 'AA' shows that the next combination produced is 'BC' rather
    than 'BA', which would have been produced if they hadn't matched.

    AD
        BD
            CD
            CA
            CC  <-- *match* (at end of sequence so cannot move ahead)
        BA
            CA
            CC  <-- *match* (at end of sequence so cannot move ahead)
        BC
            CC  <-- *match* (at end of sequence so cannot move ahead)
    AA          <-- *match*; _SKIP_ TO NEXT ELEMENT IN _BOTH_ SEQUENCES.
        BC
            CC  <-- *match* (at end of sequence so cannot move ahead)
    AC
        BC
            CC  <-- *match* (at end of sequence so cannot move ahead)

    See previous solutions for context.

    Time = O(m*n)
           m = len(text1)
           n = len(text2)
           Each pair of elements between text1 and text2 is evaluated only 
           once, because the results are cached.  In the worst case, when
           there are no common elements between the sequences, all characters
           in each sequence will be evaluated.

    Space = O(min(m, n) + m*n) = O(m*n)
            m = len(text1)
            n = len(text2)
            min(m, n) = max call stack depth
            m*n = max cache size
"""
class Solution4_TopDownDP:
    def longestCommonSubsequence(self, 
                                 text1: str, 
                                 text2: str, 
                                 text1Idx: int = None, 
                                 text2Idx: int = None, 
                                 cache: dict = None) -> int:
        if None == text1Idx: text1Idx = 0
        if None == text2Idx: text2Idx = 0
        if None == cache: cache = {}
        if text1Idx == len(text1) or text2Idx == len(text2):
            return 0
        if (text1Idx, text2Idx) in cache:
            return cache[(text1Idx, text2Idx)]
        if text1[text1Idx] == text2[text2Idx]:
            result = 1 + self.longestCommonSubsequence(text1, text2, text1Idx + 1, text2Idx + 1, cache)
        else:
            c = self.longestCommonSubsequence(text1, text2, text1Idx + 1, text2Idx, cache)
            d = self.longestCommonSubsequence(text1, text2, text1Idx, text2Idx + 1, cache)
            result = max(c, d)
        cache[(text1Idx, text2Idx)] = result
        return result

"""
    Botton up DP.
    The result of each sub-problem is calculated only once and the results 
    are tabulated.

    Example 2:

    Seq a) A B C
    Seq b) D A C

    This example shows how the element indexes in both sequences are advanced 
    when the elements match.  Combination 'CC' doesn't show this because 'C' 
    is at the end of the sequence so there is nowhere to advance.
    Combination 'AA' shows that the next combination produced is 'BC' rather
    than 'BA', which would have been produced if they hadn't matched.

    AD
        BD
            CD
            CA
            CC  <-- *match* (at end of sequence so cannot move ahead)
        BA
            CA
            CC  <-- *match* (at end of sequence so cannot move ahead)
        BC
            CC  <-- *match* (at end of sequence so cannot move ahead)
    AA          <-- *match*; _SKIP_ TO NEXT ELEMENT IN _BOTH_ SEQUENCES.
        BC
            CC  <-- *match* (at end of sequence so cannot move ahead)
    AC
        BC
            CC  <-- *match* (at end of sequence so cannot move ahead)

    A 2D grid is used to illustrate the solution.  This grid has 
    sequence 'a' elements + 1 COLUMNS and sequence 'b' elements + 1 ROWS.
    This allows each element in each sequence to be individually compared with
    each element in the other.  Each cell whose corresponding elements do NOT
    match contains:
      +------+
      | n=   |
      | max→ |
      |  ↓   |
      +------+
    which indicates that the value (n) of that cell is the maximum value of 
    the adjacent cells on the right and bottom.  Since this is a recurrence 
    relation, the values in these cells are similarly recursively calculated.
    The recursion base case (where recursion stops) is illustrated by a cell
    with a zero (0) in it, which is any right or down index that is out of 
    bounds.  Each cell whose corresponding elements DO match contains:
      +------+
      | n=   |
      |  1+  |
      |    ↘ |
      +------+
    which indicates that the value (n) of that cell is equal to one (1), 
    because the elements match, plus the value in the adjacent cell one 
    step down and one step to the right, i.e. the adjacent south east cell.  
    The value in the south east cell is produced from the two subsequences 
    created from each sequence that led to the south east cell with the 
    element that corresponds to the south east cell removed from the sequence.
    Calculation is done from the bottom row to the top row and from the right-
    most column to the left-most column.
    The final result is the value in cell (0, 0).
    
         A      B      C
      +------+------+------+------+
      | 2=   | 1=   | 1=   |      |
    D | max→ | max→ | max→ |  0   |
      |  ↓   |  ↓   |  ↓   |      |
      +------+------+------+------+
      | 2=   | 1=   | 1=   |      |
    A |  1+  | max→ | max→ |  0   |
      |    ↘ |  ↓   |  ↓   |      |
      +------+------+------+------+
      | 1=   | 1=   | 1=   |      |
    C | max→ | max→ |  1+  |  0   |
      |  ↓   |  ↓   |    ↘ |      |
      +------+------+------+------+
      |      |      |      |      |
      |  0   |  0   |  0   |  0   |
      |      |      |      |      |
      +------+------+------+------+

    Since this solution uses tabulation, the calculations can be done in any
    direction (left to right, right to left, top to bottom, bottom to top).  
    It doesn't affect the outcome, however the approach I've taken is easy to 
    relate to the recurrence relation and recursive solutions.

    See previous solutions for context.

    Time = O((m+1) * (n+1)) => O(m*n)
           m = len(text1)
           n = len(text2)
           Each pair of elements between text1 and text2 is evaluated.
           
    Space = O((m+1) * (n+1)) => O(m*n)
            m = len(seq1)
            n = len(seq2)
            m*n = max cache size
"""
class Solution5_DP:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        cache = [[0] * (len(text1) + 1) for _ in range(len(text2) + 1)]
        for row in range(len(text2) - 1, -1, -1): # Bottom to top.
            for col in range(len(text1) - 1, -1, -1): # Right to left.
                if text1[col] == text2[row]:
                    cache[row][col] = 1 + cache[row + 1][col + 1]
                else:
                    cache[row][col] = max(cache[row + 1][col], cache[row][col + 1])
        return cache[0][0]

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

def test4(solution):
    text1 = "bsbininm"
    text2 = "jmjkbkjkv"
    expected = 1
    startTime = time.time()
    result = solution.longestCommonSubsequence(text1, text2)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

def test5(solution):
    text1 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    text2 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    expected = 210
    startTime = time.time()
    result = solution.longestCommonSubsequence(text1, text2)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

def test100(solution):
    text1 = ""
    text2 = ""
    expected = 0
    startTime = time.time()
    result = solution.longestCommonSubsequence(text1, text2)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

def test101(solution):
    text1 = "abcbdab"
    text2 = "bdcaba"
    expected = 4
    startTime = time.time()
    result = solution.longestCommonSubsequence(text1, text2)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

def test102(solution):
    text1 = "abcbdab"
    text2 = "asdjcefhiuhi"
    expected = 2
    startTime = time.time()
    result = solution.longestCommonSubsequence(text1, text2)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

if "__main__" == __name__:
    test1(Solution1_BruteForce())
    test1(Solution2_BruteForce())
    test1(Solution3_BruteForce())
    test1(Solution4_TopDownDP())
    test1(Solution5_DP())

    test2(Solution1_BruteForce())
    test2(Solution2_BruteForce())
    test2(Solution3_BruteForce())
    test2(Solution4_TopDownDP())
    test2(Solution5_DP())

    test3(Solution1_BruteForce())
    test3(Solution2_BruteForce())
    test3(Solution3_BruteForce())
    test3(Solution4_TopDownDP())
    test3(Solution5_DP())

    test4(Solution1_BruteForce())
    test4(Solution2_BruteForce())
    test4(Solution3_BruteForce())
    test4(Solution4_TopDownDP())
    test4(Solution5_DP())

    #test5(Solution1_BruteForce())
    #test5(Solution2_BruteForce())
    #test5(Solution3_BruteForce())
    test5(Solution4_TopDownDP())
    test5(Solution5_DP())

    test100(Solution1_BruteForce())
    test100(Solution2_BruteForce())
    test100(Solution3_BruteForce())
    test100(Solution4_TopDownDP())
    test100(Solution5_DP())

    test101(Solution1_BruteForce())
    test101(Solution2_BruteForce())
    test101(Solution3_BruteForce())
    test101(Solution4_TopDownDP())
    test101(Solution5_DP())

    test102(Solution1_BruteForce())
    test102(Solution2_BruteForce())
    test102(Solution3_BruteForce())
    test102(Solution4_TopDownDP())
    test102(Solution5_DP())

# End of "solution.py".
