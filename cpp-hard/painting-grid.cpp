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
#include <set>
//#include <algorithm>
#include <map>
int find_count_coloring(int, int);
bool be_compatible(int, int, int);
bool be_acceptable(int, int);
std::vector<int> convert_digit(int, int);
//int give_additional(int, int, int);
//int give_additional(int, int);
//int power_two_modulo(int);
int modulo(int);
int give_power(int);

int main()
{
   int width = 5;
   int height = 5;
   int count = find_count_coloring(width, height);
   std::cout << "There are " << count << " ways." << std::endl;
   // int width = 5;
   // int height = 5;
   // "580986"
}

int find_count_coloring(int width, int height)
{
   int total = give_power(width);
   std::vector<std::set<int>> many_compatible;
   for (int pattern_new = 0; pattern_new <= total - 1; pattern_new++)
   {
      std::set<int> set = std::set<int>();
      if (!be_acceptable(width, pattern_new))
      {
         many_compatible.push_back(set);
         continue;
      }
      for (int pattern_old = 0; pattern_old <= total - 1; pattern_old++)
      {
         if (!be_acceptable(width, pattern_old)) { continue; }
         if (!be_compatible(width, pattern_new, pattern_old)) { continue; }
         set.insert(pattern_old);
      }
      many_compatible.push_back(set);
   }

   std::vector<int> record_old(total, 0);
   for (int pattern_new = 0; pattern_new <= total - 1; pattern_new++)
   {
      if (be_acceptable(width, pattern_new))
      {
         record_old[pattern_new] = 1;
      }
   }

   for (int row = 1; row <= height - 1; row++)
   {
      std::vector<int> record_new(total, 0);
      for (int pattern_new = 0; pattern_new <= total - 1; pattern_new++)
      {
         std::set<int> set = many_compatible[pattern_new];
         for (
            auto pattern_old_ = set.begin();
            pattern_old_ != set.end(); pattern_old_++
         )
         {
            record_new[pattern_new] += record_old[*pattern_old_];
            record_new[pattern_new] = modulo(record_new[pattern_new]);
         }
      }
      record_old = record_new;
   }

   int result = 0;
   for (int pattern = 0; pattern <= total - 1; pattern++)
   {
      result += modulo(record_old[pattern]);
      result = modulo(result);
   }
   result = modulo(result);
   return result;
}

bool be_compatible(int width, int this_pattern, int that_pattern)
{
   //std::cout << "comparing:" << this_pattern << " " << that_pattern << std::endl;
   std::vector<int> this_many_digit = convert_digit(width, this_pattern);
   std::vector<int> that_many_digit = convert_digit(width, that_pattern);
   for (int head = 0; head <= width - 1; head++)
   {
      if (this_many_digit[head] == that_many_digit[head])
      {
         //std::cout << "heads:" << this_many_digit[head] << " " << that_many_digit[head] << std::endl;
         //std::cout << "No!" << std::endl;
         return false;
      }
   }
   //std::cout << "Yes!" << std::endl;
   return true;
}

bool be_acceptable(int width, int pattern)
{
   std::vector<int> many_digit = convert_digit(width, pattern);
   int last = many_digit[0];
   for (int head = 1; head <= width - 1; head++)
   {
      int novel = many_digit[head];
      if (last == novel) { return false; }
      last = novel;
   }
   return true;
}

std::vector<int> convert_digit(int width, int pattern)
{
   int remain = pattern;
   std::vector<int> many_digit;
   while (remain)
   {
      int digit = remain % 3;
      many_digit.push_back(digit);
      remain -= digit;
      remain /= 3;
   }
   while (many_digit.size() < width)
   {
      many_digit.push_back(0);
   }
   /*
   std::cout << "convert:";
   for (int head = 0; head <= width - 1; head++)
      std::cout << many_digit[head];
   std::cout << std::endl;
   */
   return many_digit;
}

int modulo(int natural)
{
   int characteristic = 1000000007;
   int result = natural % characteristic;
   return result;
}

int give_power(int power)
{
   int result = 1;
   for (int step = 0; step <= power - 1; step++)
   {
      result *= 3;
   }
   return result;
}

/*
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
*/