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
// Accepted July 25, 2021

#include <iostream>
#include <string>
#include <tuple>
#include <map>

typedef std::tuple<int, int, int> Index;
typedef std::tuple<std::string, std::string, std::string> Text;
typedef std::map<Index, bool> Record;
bool be_interleaved(std::string, std::string, std::string);
void fill_record(Text, Record&, Index);

int main()
{
   std::string this_string = "ab";
   std::string that_string = "bc";
   std::string goal = "babc";
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
   Record record;
   for (int limit = 0; limit <= goal.size(); limit++)
   {
      for (int size = 0; size <= limit; size++)
      {
         Text text = std::make_tuple(
            this_string.substr(0, size),
            that_string.substr(0, limit - size),
            goal.substr(0, limit)
         );
         Index present = std::make_tuple(
            size,
            limit - size,
            limit
         );
         fill_record(text, record, present);
      }
   }
   Index final = std::make_tuple(
      this_string.size(),
      that_string.size(),
      goal.size()
   );
   bool be = record[final];
   return be;
}

void fill_record(Text text, Record& record, Index present)
{
   std::string text_this = std::get<0>(text);
   std::string text_that = std::get<1>(text);
   std::string text_goal = std::get<2>(text);
   int index_this = std::get<0>(present);
   int index_that = std::get<1>(present);
   int index_goal = std::get<2>(present);
   if (index_goal != index_this + index_that)
   {
      record[present] = false;
      return;
   }
   if (index_this == 0)
   {
      if (text_goal == text_that) { record[present] = true; }
      else { record[present] = false; }
      return;
   }
   if (index_that == 0)
   {
      if (text_goal == text_this) { record[present] = true; }
      else { record[present] = false; }
      return;
   }
   Index last_this = std::make_tuple(
      index_this - 1,
      index_that,
      index_goal - 1
   );
   Index last_that = std::make_tuple(
      index_this,
      index_that - 1,
      index_goal - 1
   );
   bool whether_this = (text_this.back() == text_goal.back());
   bool whether_that = (text_that.back() == text_goal.back());
   if (whether_this) { record[present] = record[last_this]; }
   if (whether_that) { record[present] = record[last_that]; }
   if (whether_this && whether_that)
   {
      record[present] = record[last_this] || record[last_that];
   }
}

