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
int count_triangle_number(Choice&);
int count_triangle_number_variable(Choice*);
int count_triangle_number_fixed(int, Choice*);

int main()
{
   std::string text = "applepenapple";
   Dictionary dictionary = {"apple", "pen"};
   if (count = break_word(text, dictionary))
   {
      std::cout << "Yes!" << std::endl;
   }
   else
   {
      std::cout << "Yes!" << std::endl;
   }
   // "Yes!"
}

bool break_word(string text, Dictionary& dictionary)
{
   for entry in dictionary
   if (whether_match_beginning(text, entry))
   remain = text - start
   break_word(remain, Dictionary& dictionary)
}

bool whether_match_beginning(std::string parent, std::string child)
{
   bool whether;
   int size = child.size()
   slice = parent[:size]
   if (slice == child) { whether = true; }
   return whether
}
