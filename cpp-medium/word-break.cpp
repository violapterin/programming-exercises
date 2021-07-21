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
   `s` and `dictionary[i]` consist of only lowercase English letters.
   All the strings of `dictionary` are unique.
*/

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
typedef std::vector<std::string> Dictionary;
struct Order;
bool shall_break_word(std::string, Dictionary&);
bool shall_break_word_sorted(std::string, Dictionary&);
//bool shall_match_beginning(std::string, std::string);

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

struct Order {
   inline bool operator()(
      const std::string& first,
      const std::string& second
   ) const
   {
      return first.size() >= second.size();
   }
};

bool shall_break_word(std::string text, Dictionary& dictionary)
{
   Order order;
   std::sort(dictionary.begin(), dictionary.end(), order);
   whether = shall_break_word_sorted(text, dictionary);
   return whether;
}

bool shall_break_word_sorted(std::string text, Dictionary& dictionary)
{
   for (
      auto entry_ = dictionary.begin();
      entry_ != dictionary.end(); entry_++
   )
   {
      if (text.size() < entry_->size()) { continue; }
      if (text[0] != (*entry_)[0]) { continue; }
      int size = entry_->size();
      std::string slice = text.substr(0, size);
      if (slice != *entry_) { continue; }
      if (size == text.size()) { return true; }
      std::string remain = text.substr(size, std::string::npos);
      if (shall_break_word_sorted(remain, dictionary)) { return true; }
   }
   return false;
}
