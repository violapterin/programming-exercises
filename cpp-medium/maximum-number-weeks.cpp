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
   `1 <= size <= 105`
   `1 <= milestones[index] <= 109`
*/

#include <iostream>
#include <algorithm>
#include <vector>
#include <unordered_set>
typedef std::vector<int> Array;
typedef std::pair<int, int> Pair;
typedef std::vector<Pair> Queue;
int find_number_round(Array&);
int find_total(Array&);

int main()
{
   //Array bound = {5, 2, 1};
   Array bound = {5,7,5,7,9,7};
   int number = find_number_round(bound);
   std::cout << "There are " << number << " weeks." << std::endl;
   // 7
}

int find_number_round(Array& array)
{
   int size = array.size();
   int total = find_total(array);
   if (size == 1) { return array[0]; }
   Queue queue;
   int count = 0;
   for (
      auto value_ = array.begin();
      value_ != array.end(); value_++
   )
   {
      queue.push_back(Pair(*value_, count));
      count += 1;
   }
   int small = 0;
   int previous = -1;
   auto order = [](auto &left, auto &right)
   {
      return left.first > right.first;
   };
   while (true)
   {
      std::sort(queue.begin(), queue.end(), order);
      for (int head = 0; head < size; head++)
      {
         std::cout << '(' << queue[head].first << ',' << queue[head].second << ')' << ',';
      }
      std::cout << std::endl;
      if (queue[1].first == 0)
      //if (queue[1].first == 0 && previous == queue[0].second)
      {
         break;
      }
      if (queue[0].first == 0)
      {
         break;
      }
      queue[0].first -= queue[1].first;
      queue[1].first = 0;
      if (previous == queue[0].second) { previous = queue[1].second; }
      if (previous == queue[1].second) { previous = queue[0].second; }
      else
      {
         previous = queue[0].second;
         /*
         if (queue[0].first > 0)
         {
            queue[0].first -= 1;
         }
         */
      }
      std::cout << "previous:" << previous << std::endl;
   }
   std::sort(queue.begin(), queue.end(), order);
   if (queue[0].first > 0)
   //if (queue[0].first > 0 && previous != queue[0].second)
   {
      queue[0].first -= 1;
   }
   for (int head = 0; head < size; head++)
   {
      std::cout << '(' << queue[head].first << ',' << queue[head].second << ')' << ',';
   }
   std::cout << std::endl;
   int remain = total - queue[0].first;
   return remain;
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

/*
int find_number_round(Queue& queue)
{
   int size = queue.size();
   int total = find_total(queue);
   int small = 0;
   if (size == 1) { return queue[0]; }

   while (true)
   {
      std::sort(queue.begin(), queue.end(), std::greater<int>());
      for (int head = 0; head < size; head++)
      {
         std::cout << queue[head] << ',';
      }
      std::cout << std::endl;
      int small = 0;
      if (queue[0] >= queue[1])
      {
         small = queue[1];
      }
      else
      {
         small = queue[0];
      }
      if (small == 0) { break; }
      queue[1] -= small;
      queue[0] -= small;
   }
   int remain = total - queue[0];
   if (queue[0] > 0) { remain += 1; }
   return remain;
}
*/