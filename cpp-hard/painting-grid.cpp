// 1931. Painting a Grid With Three Different Colors [hard]
/*
You are given two integers `m` and `n`. Consider an `m` by `n` grid
where each cell is initially white. You can paint each cell red,
green, or blue. All cells must be painted. Return the number of ways
to color the grid with no two adjacent cells having the same color.
Since the answer can be very large, return it modulo `10^9 + 7`.

Constraints: `1 <= m <= 5`, `1 <= n <= 1000`.
*/

#include <iostream>
#include <string>
#include <vector>
//#include <algorithm>
#include <map>
typedef std::map<int, int> Table;
typedef std::vector<Table> Configuration;
int find_count_coloring(int, int);
int give_additional(int, int, int);
int give_additional(int, int);
int power_two_modulo(int);
int modulo(int);

int main()
{
   int width = 2;
   int height = 3;
   int count = find_count_coloring(width, height);
   std::cout << "There are " << count << " ways." << std::endl;
   // int width = 5;
   // int height = 5;
   // "580986"
}


int find_count_coloring(int width, int height)
{
   int total = 1 << (width - 1);
   Configuration configuration;
   for (int pattern = 0; pattern <= total - 1; pattern++)
   {
      configuration.push_back(Table());
   }
   if (height >= 2)
   {
      for (int pattern = 0; pattern <= total - 1; pattern++)
      {
         int additional = give_additional(width, pattern);
         configuration[pattern][width + additional] = 1;
      }
   }

   for (int row = 1; row <= height - 2; row++)
   {
      Configuration hold;
      for (int pattern = 0; pattern <= total - 1; pattern++)
      {
         hold.push_back(Table());
      }
      for (int pattern_old = 0; pattern_old <= total - 1; pattern_old++)
      {
         Table table_old = configuration[pattern_old];
         for (int pattern_new = 0; pattern_new <= total - 1; pattern_new++)
         {
            int additional = give_additional(width, pattern_old, pattern_new);
            for(
               auto pair_ = table_old.begin();
               pair_ != table_old.end(); pair_++
            )
            {
               int count = modulo(pair_->second);
               hold[pattern_new][pair_->first + additional] += count;
            }
         }
      }
      configuration = hold;
   }

   int result = 0;
   for (int pattern = 0; pattern <= total - 1; pattern++)
   {
      for(
         auto pair_ = configuration[pattern].begin();
         pair_ != configuration[pattern].end(); pair_++
      )
      {
         int count_coloring = 3 * power_two_modulo(pair_->first - 1);
         int count_method = modulo(pair_->second);
         result += count_coloring * count_method;
         result = modulo(result);
      }
   }
   return result;
}

int give_additional(int width, int pattern_new)
{
   int result = 1;
   if (width >= 3)
   {
      for (int step = 0; step <= width - 3; step++)
      {
         int mask_new = (pattern_new & (3 << step)) ^ (2 << step);
         if (mask_new == 0) { result += 1; }
      }
      for (int step = 0; step <= width - 3; step++)
      {
         int mask_new = (pattern_new & (3 << step)) ^ (1 << step);
         if (mask_new == 0) { result -= 1; }
      }
   }
   return result;
}

int give_additional(int width, int pattern_old, int pattern_new)
{
   int result = 1;
   if (width >= 3)
   {
      for (int step = 0; step <= width - 3; step++)
      {
         int mask_new = (pattern_new & (3 << step)) ^ (2 << step);
         if (mask_new == 0) { result += 1; }
      }
      for (int step = 0; step <= width - 3; step++)
      {
         int mask_old = (pattern_old & (3 << step)) ^ (2 << step);
         int mask_new = (pattern_new & (3 << step)) ^ (1 << step);
         if (mask_new == 0) { if (mask_old != 0) { result -= 1; } }
      }
   }
   return result;
}

int power_two_modulo(int power)
{
   int result = 1;
   for (int step = 1; step <= power; step++)
   {
      result *= 2;
      result = modulo(result);
   }
   return result;
}

int modulo(int natural)
{
   int characteristic = 1000000007;
   int result = natural % characteristic;
   return result;
}