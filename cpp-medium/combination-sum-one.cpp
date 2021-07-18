// 39. Combination Sum [medium]
/*
   Given an array of distinct integers `choice` and a target integer
`target`, return a list of all unique combinations of `choice` where
the chosen numbers sum to `target`. You may return the combinations in
any order.
   The same number may be chosen from `choice` an unlimited number
of times. Two combinations are unique if the frequency of at least one
of the chosen numbers is different.
   It is guaranteed that the number of unique combinations that sum up
to `target` is less than `150` combinations for the given input.
   `1 <= choice.length <= 30`
   `1 <= choice[i] <= 200`
   All elements of choice are distinct.
   `1 <= target <= 500`
*/
// Accepted July 11, 2021.

#include <iostream>
#include <algorithm>
#include <vector>
typedef std::vector<int> Tuple;
typedef std::vector<Tuple> Many_tuple;
Many_tuple find_combination(Tuple&, int);
Many_tuple concatenate(Many_tuple, Many_tuple);
void push_each(int, Many_tuple&);
void print_many_tuple(Many_tuple);
void print_tuple(Tuple);

Many_tuple find_combination(Tuple& choice, int target)
{
   std::sort(choice.begin(), choice.end());
   Many_tuple whole;
   for (
      auto value_ = choice.begin();
      value_ != choice.end(); value_++
   )
   {
      Many_tuple partial;
      int remain = target - *value_;
      if (remain == 0)
      {
         Tuple pure = {*value_};
         whole.push_back(pure);
      }
      else if (remain > 0)
      {
         Tuple other = Tuple(value_, choice.end());
         partial = find_combination(other, remain);
         if (!partial.empty())
         {
            push_each(*value_, partial);
            whole = concatenate(whole, partial);
         }
      }
   }
   return whole;
}

void push_each(int value, Many_tuple& many_tuple)
{
   for (
      auto tuple_ = many_tuple.begin();
      tuple_ != many_tuple.end(); tuple_++
   )
   {
      tuple_->push_back(value);
   }
}

Many_tuple concatenate(
   Many_tuple this_many_tuple,
   Many_tuple that_many_tuple
)
{
   Many_tuple whole;
   for (
      auto tuple_ = this_many_tuple.begin();
      tuple_ != this_many_tuple.end(); tuple_++
   )
   {
      whole.push_back(*tuple_);
   }
   for (
      auto tuple_ = that_many_tuple.begin();
      tuple_ != that_many_tuple.end(); tuple_++
   )
   {
      whole.push_back(*tuple_);
   }
   return whole;
}

void print_many_tuple(Many_tuple many_tuple)
{
   for (
      auto tuple_ = many_tuple.begin();
      tuple_ != many_tuple.end(); tuple_++
   )
   {
      print_tuple(*tuple_);
   }
}

void print_tuple(Tuple tuple)
{
   std::cout << "[";
   for (
      auto value_ = tuple.begin();
      value_ != tuple.end(); value_++
   )
   {
      std::cout << *value_ << ",";
   }
   std::cout << "]";
   std::cout << std::endl;
}

int main()
{
   Tuple choice = {2, 3, 5};
   int target = 8;
   Many_tuple many_tuple = find_combination(choice, target);
   print_many_tuple(many_tuple);
   // [2,2,2,2,]
   // [2,3,3,]
   // [3,5,]
}
