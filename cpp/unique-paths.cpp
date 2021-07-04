#include <iostream>
#include <vector>
typedef std::vector<int> Array;
int uniquePaths(int height_max, int width_max);
Array calculate_rightwards(Array);
Array calculate_expanded(Array);
Array calculate_shrinked(Array);
Array calculate(Array, bool, bool);

int uniquePaths(int height_max, int width_max) {
   Array change = {1};
   int bound_first = std::min(height_max, width_max);
   int bound_second = std::abs(width_max - height_max);
   for (int head = 1; head <= bound_first - 1; head++)
   {
      change = calculate_expanded(change);
   }
   for (int head = 1; head <= bound_second; head++)
   {
      change = calculate_rightwards(change);
   }
   for (int head = 1; head <= bound_first - 1; head++)
   {
      change = calculate_shrinked(change);
   }
   return change.front();
}

Array calculate_rightwards(Array given)
{
   return calculate(given, false, true);
}

Array calculate_expanded(Array given)
{
   return calculate(given, true, true);
}

Array calculate_shrinked(Array given)
{
   return calculate(given, false, false);
}

Array calculate(Array given, bool whether_left, bool whether_right)
{
   int size = given.size();
   Array array;
   if (whether_left)
   {
      array.push_back(given.front());
   }
   for (auto count_ = array.begin() + 1; count_ != array.end() - 1; count_++)
   {
      int step = count_ - array.begin();
      std::cout << "step - 1: " << step << std::endl;
      int novel = given[step - 1] + given[step];
      array.push_back(novel);
   }
   if (whether_right)
   {
      array.push_back(given.back());
   }
   return array;
}

int main()
{
   int p = uniquePaths(3, 7);
   std::cout << p << std::endl;
}