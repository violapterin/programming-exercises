// 3. Longest Substring Without Repeating Characters [medium]
/*
   Given a string `s`, find the length of the longest substring
without repeating characters.
   `0 <= s.length <= 5 * 10^4`
   `s` consists of English letters, digits, symbols and spaces.
*/
// Accepted July 18, 2021

#include <iostream>
#include <string>
#include <tuple>
typedef std::tuple<int, int, std::string> Record;
int find_length_longest_substring(std::string);
Record update_record(char, Record);

int main()
{
   std::string text = "abbcdb";
   int length = find_length_longest_substring(text);
   std::cout << "length of longest substring: " << length << std::endl;
   // "3"
   /* substring: "bcd" */
}

int find_length_longest_substring(std::string text)
{
   Record record = std::make_tuple(0, 0, std::string());
   for (int count = 0; count < text.size(); count++)
   {
      char symbol = text[count];
      record = update_record(symbol, record);
   }
   int length_detached_longest = std::get<0>(record);
   return length_detached_longest;
}

Record update_record(char symbol_new, Record record_old)
{
   int size_detached = std::get<0>(record_old);
   int size_connected = std::get<1>(record_old);
   std::string series = std::get<2>(record_old);
   int cut = series.find_last_of(symbol_new);
   std::string previous;
   if (cut != std::string::npos)
   {
      previous = series.substr(cut + 1, std::string::npos);
   }
   else
   {
      previous = series;
   }
   series = previous + symbol_new;
   size_connected = series.size();
   if (size_detached < size_connected) { size_detached = size_connected; }
   Record record_new = std::make_tuple(
      size_detached,
      size_connected,
      series 
   );
   return record_new;
}
