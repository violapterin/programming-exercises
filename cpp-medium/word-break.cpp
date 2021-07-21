// 139. Word Break [medium]
/*
   Given a string `text` and a dictionary of strings `dictionary`,
return true if `text` can be segmented into a space- separated
sequence of one or more words in `dictionary`.
   Note that the same word in the dictionary may be reused multiple
times in the segmentation.
   `1 <= text.length <= 300`
   `1 <= dictionary.length <= 1000`
   `1 <= dictionary[i].length <= 20`
   `text` and `dictionary[i]` consist of only lowercase English letters.
   All the strings of `dictionary` are unique.
*/

#include <iostream>
#include <string>
#include <set>
#include <map>
#include <vector>
#include <algorithm>
typedef std::vector<std::string> Dictionary;
typedef std::set<std::string> Group;
typedef std::map<char, Group> Table;
struct Order;
bool shall_break_word(std::string, Dictionary&);
bool shall_check_table(std::string, Table&);

int main()
{
   std::string text = "applepenapple";
   Dictionary dictionary = {"apple", "pen"};
   if (shall_break_word(text, dictionary))
   {
      std::cout << "Yes!" << std::endl;
   }
   else
   {
      std::cout << "No!" << std::endl;
   }
   // "Yes!"
}

/*
struct Order
{
   inline bool operator()(std::string& first, std::string& second)
   {
      return first.size() > second.size();
   }
};
*/

bool shall_break_word(std::string text, Dictionary& dictionary)
{
   std::string alphabet = "abcdefghijklmnopqrstuvwxyz";
   Table table = Table();
   for (int head = 0; head <= 25; head ++)
   {
      char symbol = alphabet[head];
      Group group = Group();
      table[symbol] = Group();
   }
   for (
      auto entry_ = dictionary.begin();
      entry_ != dictionary.end(); entry_++
   )
   {
      char symbol = (*entry_)[0];
      table[symbol].insert(*entry_);
   }
   /*
   Order order;
   for (
      auto group_ = table.begin();
      group_ != table.end(); group_++
   )
   {
      std::sort(group_->begin(), group_->end(), order);
   }
   */
   bool whether = shall_check_table(text, table);
   return whether;
}

bool shall_check_table(std::string text, Table& table)
{
   char symbol = text[0];
   Group group = table[symbol];
   for (
      auto word_ = group.begin();
      word_ != group.end(); word_++
   )
   {
      int size = word_->size();
      if (size > text.size()) { continue; }
      if (text.compare(0, size, *word_) == 0)
      {
         if (size == text.size()) { return true; }
         std::string remain = text.substr(size, std::string::npos);
         if (shall_check_table(remain, table)) { return true; }
      }
   }
   return false;
}
