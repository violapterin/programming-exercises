// 96. Unique Binary Search Trees
/*
   Given an integer `n`, return the number of structurally unique
binary search trees which has exactly `n` nodes of unique values
from `1` to `n`.
   `1 <= n <= 19`
*/
// Accepted August 3, 2021.

#include <iostream>
#include <vector>
typedef std::vector<int> Record;
int find_number_tree(int);
void fill_record(Record&, int);

int main()
{
   int total = 3;
   int number = find_number_tree(total);
   std::cout << "There are " << number << " Trees." << std::endl;
   // 5
}

int find_number_tree(int total)
{
   Record record(total + 1, 0);
   record[0] = 1;
   for (int head = 1; head <= total; head++)
      fill_record(record, head);
   return record[total];
}

void fill_record(Record& record, int total)
{
   int amount = 0;
   for (int head = 0; head <= total - 1; head++)
   {
      amount += record[head] * record[total - head - 1];
   }
   record[total] = amount;
   std::cout << "record" << total << ":" << amount << std::endl;
}