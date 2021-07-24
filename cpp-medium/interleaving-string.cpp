// 97. Interleaving String [medium]
/*
   Given strings `s1`, `s2`, and `s3`, find whether `s3` is formed
by an interleaving of `s1` and `s2`.
   An interleaving of two strings `s` and `t` is a configuration
where they are divided into nonempty substrings such that:
   `s = s1 + s2 + ... + sn`
   `t = t1 + t2 + ... + tm`
   `|n - m| <= 1`
   The interleaving is `s1 + t1 + s2 + t2 + s3 + t3 + ...` or
`t1 + s1 + t2 + s2 + t3 + s3 + ...`
   Note: `a + b` is the concatenation of strings `a` and `b`.
   `0 <= s1.length, s2.length <= 100`
   `0 <= s3.length <= 200`
   `s1`, `s2`, and `s3` consist of lowercase English letters.
*/

#include <iostream>
#include <string>

bool be_interleaved(std::string, std::string, std::string);

int main()
{
   std::string this_string = "aabcc";
   std::string that_string = "dbbca";
   std::string goal = "aadbbcbcac";
   if (be_interleaved(this_string, that_string, goal))
   {
      std::cout << "Yes!" << std::endl;
   }
   else
   {
      std::cout << "No!" << std::endl;
   }
   // "Yes!"
}

bool be_interleaved(
   std::string this_string,
   std::string that_string,
   std::string goal
)
{
   //std::cout << "compare:" << this_string << ' ' << that_string << std::endl;
   if (this_string.empty())
   {
      if (that_string == goal) { return true; }
      else { return false; }
   }
   if (that_string.empty())
   {
      if (this_string == goal) { return true; }
      else { return false; }
   }
   char start = goal[0];
   char this_start = this_string[0];
   char that_start = that_string[0];
   std::string this_remain = this_string.substr(1);
   std::string that_remain = that_string.substr(1);
   std::string goal_remain = goal.substr(1);
   bool whether_this = (start == this_start);
   bool whether_that = (start == that_start);
   if (!whether_this && !whether_that) { return false; }
   else if (whether_this && !whether_that)
   {
      return be_interleaved(this_remain, that_string, goal_remain);
   }
   else if (!whether_this && whether_that)
   {
      return be_interleaved(this_string, that_remain, goal_remain);
   }
   else
   {
      bool be_this = be_interleaved(
         this_string,
         that_remain,
         goal_remain
      );
      bool be_that = be_interleaved(
         this_remain,
         that_string,
         goal_remain
      );
      return (be_this || be_that);
   }
   return false;
}
