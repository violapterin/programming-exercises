// 62. Unique Paths [medium]
/*
   A robot is located at the top- left corner of a `m` by `n` grid.
The robot can only move either down or right at any point in time.
The robot is trying to reach the bottom- right corner of the grid.
How many possible unique paths are there?
   `1 <= m, n <= 100`
   The answer will be less than or equal to `2 * 10^9`.
*/
// Accepted July 4, 2021.

#include <iostream>
#include <vector>
typedef std::vector<int> Array;
int count_unique_path(int height_max, int width_max);
Array calculate(Array, bool, bool);

int main()
{
   int count_path = count_unique_path(3, 7);
   std::cout << count_path << std::endl;
   // "28"
}

int count_unique_path(int height_max, int width_max) {
   Array change = {1};
   int bound_first = std::min(height_max, width_max);
   int bound_second = std::abs(width_max - height_max);
   for (int head = 1; head <= bound_first - 1; head++)
      change = calculate(change, true, true);
   for (int head = 1; head <= bound_second; head++)
      change = calculate(change, false, true);
   for (int head = 1; head <= bound_first - 1; head++)
      change = calculate(change, false, false);
   return change.front();
}

Array calculate(Array given, bool whether_left, bool whether_right)
{
   int size = given.size();
   Array array;
   if (whether_left)
      array.push_back(given.front());
   if (size > 1)
   {
      for (int head = 0; head <= size - 2; head++)
         array.push_back(given[head] + given[head + 1]);
   }
   if (whether_right)
      array.push_back(given.back());
   return array;
}