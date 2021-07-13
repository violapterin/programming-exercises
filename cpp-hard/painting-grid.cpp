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
//#include <vector>
//#include <algorithm>
#include <cmath>
//typedef std::vector<int> Rain;
int find_count_coloring(int, int);
int give_additional(int, int, int);

int main()
{
   int width = 5;
   int height = 5;
   int 
   int count = find_count_coloring(width, height);
   std::cout << "There are " << count << " ways." << std::endl;
   // "580986"
}


int find_count_coloring(int width, int height)
{
   int total = 1 << (width - 1);
   std::vector<int> count_old(total, 1);
   for (int row = 1; row <= height - 1; row++)
   {
      std::vector<int> count_new(total, 0);
      for (int pattern_new = 1; pattern_new <= total; pattern_new++)
      {
         for (int pattern_old = 1; pattern_old <= total; pattern_old++)
         {
            additional = give_additional(width, pattern_old, pattern_new);
            count = count_old[pattern_old] + additional;
            count = modulo(count);
            count_new[pattern_new] += count;
         }
         count_new[pattern_new] = modulo(count_new[pattern_new]);
      }
      count_old = count_new;
   }
   int count_region = 0;
   for (int pattern = 1; pattern <= total; pattern++)
   {
      count_region += count_old[pattern];
   }
   int result = power_three_modulo(count_region);
   return result;
}

int give_additional(int width, int pattern_old, int pattern_new)
{
   int result = 1;
   if (width >= 3)
   {
      for (int step = 0; step <= width - 3; step++)
      {
         int mask_new = pattern_new ^ (2 << step);
         if (mask_new) { result += 1; }
      }
      for (int step = 0; step <= width - 3; step++)
      {
         int mask_old = pattern_old ^ (2 << step);
         int mask_new = pattern_new ^ (1 << step);
         if (mask_new) {
            if (mask_old != 0) { result -= 1; }
         }
      }
   }
   return result;
}

int power_three_modulo(int power)
{
   int result = 1;
   for (int step = 1; step <= power; step++)
   {
      result *= 3;
      result = modulo(result);
   }
   return result;
}

int modulo(int natural)
{
   int characteristic = 1 000 000 007;
   int result = natural % characteristic;
   return result;
}