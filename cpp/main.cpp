/*!
    \file "main.cpp"

    Author: Matt Ervin <matt@impsoftware.org>
    Formatting: 4 spaces/tab (spaces only; no tabs), 120 columns.
    Doc-tool: Doxygen (http://www.doxygen.com/)

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

class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {

//
//!\todo TODO: >>> Under Construction <<<
//
return -1;

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

/*
    End of "main.cpp"
*/
