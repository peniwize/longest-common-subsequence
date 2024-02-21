/*!
    \file "main.cpp"

    Author: Matt Ervin <matt@impsoftware.org>
    Formatting: 4 spaces/tab (spaces only; no tabs), 120 columns.
    Doc-tool: Doxygen (http://www.doxygen.com/)

    https://github.com/peniwize/longest-common-subsequence.git
    https://leetcode.com/problems/longest-common-subsequence/
*/

//!\sa https://github.com/doctest/doctest/blob/master/doc/markdown/main.md
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN

#include "utils.hpp"

/*
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
*/

/*
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

    See previous solutions for context:
    * https://leetcode.com/problems/longest-common-subsequence/solutions/4754158/python-brute-force-dp-full-explanation-t-o-m-n-s-o-m-n/
    * https://github.com/peniwize/longest-common-subsequence.git

    Time = O((m+1) * (n+1)) => O(m*n)
           m = len(text1)
           n = len(text2)
           Each pair of elements between text1 and text2 is evaluated.
           
    Space = O((m+1) * (n+1)) => O(m*n)
            m = len(seq1)
            n = len(seq2)
            m*n = max cache size
*/
class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        int_fast64_t cache[text2.size() + 1][text1.size() + 1] = {};
        for (int row = text2.size() - 1; 0 <= row; --row) {
            for (int col = text1.size() - 1; 0 <= col; --col) {
                if (text1[col] == text2[row]) {
                    cache[row][col] = 1 + cache[row + 1][col + 1];
                } else {
                    cache[row][col] = (std::max)(cache[row + 1][col], cache[row][col + 1]);
                }
            }
        }

        return cache[0][0];
    }
};

// {----------------(120 columns)---------------> Module Code Delimiter <---------------(120 columns)----------------}

namespace doctest {
    const char* testName() noexcept { return doctest::detail::g_cs->currentTest->m_name; }
} // namespace doctest {

TEST_CASE("Case 1")
{
    cerr << doctest::testName() << '\n';
    string text1 = "abcde";
    string text2 = "ace";
    int expected = 3;
    auto solution = Solution{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.longestCommonSubsequence(text1, text2);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

TEST_CASE("Case 2")
{
    cerr << doctest::testName() << '\n';
    string text1 = "abc";
    string text2 = "abc";
    int expected = 3;
    auto solution = Solution{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.longestCommonSubsequence(text1, text2);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

TEST_CASE("Case 3")
{
    cerr << doctest::testName() << '\n';
    string text1 = "abc";
    string text2 = "def";
    int expected = 0;
    auto solution = Solution{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.longestCommonSubsequence(text1, text2);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

TEST_CASE("Case 4")
{
    cerr << doctest::testName() << '\n';
    string text1 = "bsbininm";
    string text2 = "jmjkbkjkv";
    int expected = 1;
    auto solution = Solution{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.longestCommonSubsequence(text1, text2);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

TEST_CASE("Case 5")
{
    cerr << doctest::testName() << '\n';
    string text1 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
    string text2 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
    int expected = 210;
    auto solution = Solution{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.longestCommonSubsequence(text1, text2);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

TEST_CASE("Case 100")
{
    cerr << doctest::testName() << '\n';
    string text1 = "";
    string text2 = "";
    int expected = 0;
    auto solution = Solution{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.longestCommonSubsequence(text1, text2);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

TEST_CASE("Case 101")
{
    cerr << doctest::testName() << '\n';
    string text1 = "abcbdab";
    string text2 = "bdcaba";
    int expected = 4;
    auto solution = Solution{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.longestCommonSubsequence(text1, text2);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

TEST_CASE("Case 102")
{
    cerr << doctest::testName() << '\n';
    string text1 = "abcbdab";
    string text2 = "asdjcefhiuhi";
    int expected = 2;
    auto solution = Solution{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.longestCommonSubsequence(text1, text2);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

/*
    End of "main.cpp"
*/
