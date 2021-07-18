// 611. Valid Triangle Number [medium]
/*
   Given an integer array `choice`, return the number of triplets
chosen from the array that can make triangles if we take them
as side lengths of a triangle.
   `1 <= choice.length <= 1000`
   `0 <= choice[i] <= 1000`
*/

#include <iostream>
#include <vector>
#include <algorithm>
typedef std::vector<int> Choice;
int count_triangle_number(Choice&);
int count_triangle_number_variable(Choice);
int count_triangle_number_fixed(int, Choice);

int main()
{
   Choice choice = {2, 2, 3, 4};
   int count = count_triangle_number(choice);
   std::cout << count << std::endl;
   // "3"
   /* (2,3,4), (2,3,4), (2,2,3) */
}

int count_triangle_number(Choice& choice)
{
   std::sort(choice.begin(), choice.end());
   int count = count_triangle_number_variable(choice);
   return count;
}

int count_triangle_number_variable(Choice choice)
{
   if (choice.size() < 3)
   {
      return 0;
   }
   int small = choice[0];
   choice.erase(choice.begin());
   int count_partial = count_triangle_number_variable(choice);
   int count_fixed = count_triangle_number_fixed(small, choice);
   int count = count_fixed + count_partial;
   return count;
}

int count_triangle_number_fixed(int small, Choice choice)
{
   if (choice.size() < 2)
   {
      return 0;
   }
   int count = 0;
   for (
      auto less_ = choice.begin();
      less_ != choice.end() - 1; less_++
   )
   {
      for (
         auto greater_ = less_ + 1;
         greater_ != choice.end(); greater_++
      )
      {
         if (*greater_ < *less_ + small)
         {
            count += 1;
         }
      }
   }
   return count;
}