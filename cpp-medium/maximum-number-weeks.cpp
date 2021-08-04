// 1953. Maximum Number of Weeks for Which You Can Work [medium]
/*
   There are `size` projects numbered from `0` to `size - 1`. You
are given an integer array milestones where each `milestones[index]`
denotes the number of milestones the ith project has.
   You can work on the projects following these two rules:
   Every week, you will finish exactly one milestone of one
project. You must work every week.
   You cannot work on two milestones from the same project for
two consecutive weeks.
   Once all the milestones of all the projects are finished, or
if the only milestones that you can work on will cause you to
violate the above rules, you will stop working. Note that you may
not be able to finish every project's milestones due to these
constraints.
   Return the maximum number of weeks you would be able to work
on the projects without violating the rules mentioned above.
   Constraints:
   `size == milestones.length`
   `1 <= size <= 10^5`
   `1 <= milestones[index] <= 10^9`
*/
// Accepted August 5, 2021

#include <iostream>
#include <algorithm>
#include <vector>
typedef std::vector<int> Array;
//typedef std::pair<int, int> Pair;
//typedef std::vector<Pair> Queue;
long long find_number_round(Array&);
int find_start_greatest(Array&);
void winnow(Array&);
void decrease(Array&, int, int);
int find_total(Array&);
void print(Array&);

int main()
{
   Array bound = {3, 2, 1};
   int number = find_number_round(bound);
   std::cout << "There are " << number << " weeks." << std::endl;
   // 7
}

long long find_number_round(Array& array)
{
   int size = array.size();
   long long total = 0;
   for (int index = 0; index < array.size(); index++)
   {
      total += array[index];
   }
   auto big_ = std::max_element(array.begin(), array.end());
   int big = *big_;
   array.erase(big_);
   long long remain = total - big;
   if (remain < big) { return total + remain - big + 1; }
   return total;
}

/*
long long find_number_round(Array& array)
{
   int size = array.size();
   long long total = 0;
   if (size == 1)
   {
      if (array.front() > 0) { return 1; }
      else { return 0; }
   }
   std::sort(array.begin(), array.end(), std::less<int>());
   //print(array);
   while (true)
   {
      //std::sort(array.begin(), array.end(), std::less<int>());
      winnow(array);
      //if (!array.empty()) { print(array); }
      int size = array.size();
      if (size <= 1) { break; }
      int start = find_start_greatest(array);
      //std::cout << "start:" << start << std::endl;
      if (start == 0)
      {
         if (size % 2 == 0)
         {
            decrease(array, 0, size - 1);
            total += size;
         }
         else
         {
            decrease(array, 0, size - 2);
            total += size - 1;
         }
      }
      else
      {
         int ruin;
         if (start < size - start) { ruin = start; }
         else { ruin = size - start; }
         decrease(array, 0, ruin - 1);
         decrease(array, start, start + ruin - 1);
         total += ruin * 2;
      }
   }
   if (array.empty()) { return total; }
   if (array.front() > 0)
   {
      array.front() -= 1;
      total += 1;
   }
   return total;
}
*/

int find_start_greatest(Array& array)
{
   int hold = array.back();
   int head = array.size() - 1;
   while (true)
   {
      if (head == 0) { break; }
      if (head >= 1 && array[head - 1] < hold) { break; }
      head -= 1;
   }
   return head;
}

void winnow(Array& array)
{
   while (true)
   {
      if (array.empty()) { return; }
      if (array.back() != 0) { break; }
      array.pop_back();
   }
   while (true)
   {
      if (array.empty()) { return; }
      if (array.front() != 0) { break; }
      array.erase(array.begin());
   }
}

void decrease(Array& array, int start, int stop)
{
   for(int head = start; head <= stop; head++)
   {
      array[head] -= 1;
   }
}

int find_total(Array& array)
{
   int amount = 0;
   for (int index = 0; index < array.size(); index++)
   {
      amount += array[index];
   }
   return amount;
}

void print(Array& array)
{
   for (int head = 0; head < array.size(); head++)
   {
      std::cout << array[head] << ',';
   }
   std::cout << std::endl;
}

