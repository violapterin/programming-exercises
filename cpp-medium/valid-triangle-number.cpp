// 611. Valid Triangle Number [medium]
/*
   Given an integer array `choice`, return the number of triplets
chosen from the array that can make triangles if we take them
as side lengths of a triangle.
   `1 <= choice.length <= 1000`
   `0 <= choice[i] <= 1000`
*/
// Accepted July 19, 2021.

#include <iostream>
#include <vector>
#include <algorithm>
typedef std::vector<int> Choice;
int count_triangle_number(Choice&);
int count_triangle_number_variable(Choice*);
int count_triangle_number_fixed(int, Choice*);

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
   int count = count_triangle_number_variable(&choice);
   return count;
}

int count_triangle_number_variable(Choice* choice_)
{
   if (choice_->size() < 3) { return 0; }
   int final = choice_->back();
   choice_->pop_back();
   int count_fixed = count_triangle_number_fixed(final, choice_);
   int count_partial = count_triangle_number_variable(choice_);
   int count = count_fixed + count_partial;
   return count;
}

int count_triangle_number_fixed(int final, Choice* choice_)
{
   if (choice_->size() < 2) { return 0; }
   int count = 0;
   for (
      auto small_ = choice_->begin();
      small_ != choice_->end() - 1; small_++
   )
   {
      for (
         auto middle_ = choice_->end() - 1;
         middle_ != small_; middle_--
      )
      {
         if (*middle_ + *small_ <= final) { break; }
         count += 1;
      }
   }
   return count;
}