// 3. Longest Substring Without Repeating Characters
/*
   Given a string `s`, find the length of the longest substring
without repeating characters.
   `0 <= s.length <= 5 * 104`
   `s` consists of English letters, digits, symbols and spaces.
*/

#include <iostream>
#include <string>
#include <set>
typedef std::set<char> Many_symbol;
typedef std::tuple<int, int, Many_symbol> Record;
int find_length_longest_substring(std::string);
Record update_record(char, Record);

int main()
{
   text = "abbcdb";
   size = find_length_longest_substring(text);
   std::cout << size << std::endl;
   // "3"
   /* substring: "bcd" */
}

int find_length_longest_substring(std::string text)
{
   Record record = std::make_tuple(0, 0, Many_symbol());
   for (int count = 0; count <= text.size(); count++)
   {
      char symbol = text[count];
      update_record(symbol, record);
   }
   length_detached_longest = std::get<0>(record);
   return length_detached_longest;
}

Record update_record(char symbol_new, Record record_old)
{
   int length_detached = std::get<0>(record_old);
   int length_connected = std::get<1>(record_old);
   Many_symbol many_symbol = std::get<2>(record_old);
   if (symbol_new)
   if (many_symbol.find(symbol_new) == many_symbol.end())
   {
      many_symbol.insert(symbol_new);
      length_connected += 1;
   }
   else
   {
      length_detached += 1;
   }
   if (length_detached < length_connected)
   {
      length_detached = length_connected;
   }
   Record record_new = std::make_tuple(
      length_detached,
      length_connected,
      many_symbol
   );
   return record_new;
}
