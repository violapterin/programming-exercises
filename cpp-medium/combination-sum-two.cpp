// Original title: 40. Combination Sum II [medium]
/*
Given a collection of candidate numbers (candidates) and a target
number (target), find all unique combinations in candidates where
the candidate numbers sum to target.

Each number in candidates may only be used once in the combination.
Note: The solution set must not contain duplicate combinations.
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
Many_tuple prune_many_tuple(Many_tuple);
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
      int remain = target;
      auto next_ = value_;
      while (next_ != choice.end())
      {
         if (*next_ == *value_)
         {
            remain -= *next_;
            next_++;
         }
         else { break; }
      }

      if (remain == 0)
      {
         Tuple pure = {};
         for (int count = 1; count <= next_ - value_; count++)
         {
            pure.push_back(*value_);
         }
         whole.push_back(pure);
      }
      else if (remain > 0)
      {
         Many_tuple partial;
         if (next_ != choice.end())
         {
            Tuple other = Tuple(next_, choice.end());
            partial = find_combination(other, remain);
         }
         if (!partial.empty())
         {
            for (int count = 1; count <= next_ - value_; count++)
            {
               push_each(*value_, partial);
            }
            whole = concatenate(whole, partial);
         }
      }
   }
   Many_tuple pruned = prune_many_tuple(whole);
   return pruned;
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

Many_tuple prune_many_tuple(Many_tuple repeated)
{
   Many_tuple pruned = repeated;
   for (
      auto this_tuple_ = pruned.begin();
      this_tuple_ != pruned.end(); this_tuple_++
   )
   {
      auto next_ = this_tuple_ + 1;
      if (next_ == pruned.end()) { continue; }
      auto that_tuple_ = next_;
      while (that_tuple_ != pruned.end())
      {
         if (*this_tuple_ == *that_tuple_)
         {
            that_tuple_ = pruned.erase(that_tuple_);
            continue;
         }
         that_tuple_++;
      }
   }
   return pruned;
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
   Tuple choice = {10, 1, 2, 7, 6, 1, 5};
   int target = 8;
   Many_tuple many_tuple = find_combination(choice, target);
   print_many_tuple(many_tuple);
   // [1,1,6,]
   // [1,2,5,]
   // [1,7,]
   // [2,6,]
}
