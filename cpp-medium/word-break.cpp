// 139. Word Break [medium]
/*
   Given a string `text` and a dictionary of strings `dictionary`,
return true if `text` can be segmented into a space- separated
sequence of one or more words in `dictionary`.
   Note that the same word in the dictionary may be reused multiple
times in the segmentation.
*/

#include <iostream>
#include <vector>
#include <algorithm>
typedef std::vector<std::string> Dictionary;
bool break_word(std::string, Dictionary&);
bool whether_match_beginning(std::string, std::string);

int main()
{
   std::string text = "applepenapple";
   Dictionary dictionary = {"apple", "pen"};
   if (break_word(text, dictionary))
   {
      std::cout << "Yes!" << std::endl;
   }
   else
   {
      std::cout << "Yes!" << std::endl;
   }
   // "Yes!"
}

bool break_word(std::string text, Dictionary& dictionary)
{
   for (
      auto entry_ = dictionary.begin();
      entry_ != dictionary.end(); entry_++
   )
   {
      if (!whether_match_beginning(text, *entry_)) { continue; }
      if (entry_->size() == text.size()) { return true; }
      std::string remain = text.substr(entry_->size(), std::string::npos);
      bool check_remain = break_word(remain, dictionary);
      if (check_remain) { return true; }
   }
   return false;
}

bool whether_match_beginning(std::string parent, std::string child)
{
   if (parent.size() < child.size()) { return false; }
   int size = child.size();
   std::string slice = parent.substr(0, size);
   if (slice == child) { return true; }
   return false;
}
