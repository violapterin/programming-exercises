/*
Given an array of distinct integers candidates and a target integer target,
return a list of all unique combinations of candidates where the chosen
numbers sum to target. You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times.
Two combinations are unique if the frequency of at least one of the chosen
numbers is different. It is guaranteed that the number of unique combinations
that sum up to target is less than `150` combinations for the given input.
*/

#include <iostream>
#include <vector>
typedef std::vector<int> Tuple;
typedef std::vector<Tuple> Many_tuple;
Many_tuple find_combination(Tuple&, int);
Many_tuple concatenate(Many_tuple, Many_tuple);
void print_tuple(Many_tuple);

Many_tuple find_combination(Tuple& choice, int target)
{
   Many_tuple empty;
   if (choice.size() == 0)
   {
      return empty;
   }
   Many_tuple whole;
   Many_tuple previous;
   for (
      auto value_ = choice.begin();
      value_ != choice.end(); value_++
   )
   {
      Many_tuple decided;
      int target_novel = target - *value_;
      std::cout << "target:" << target_novel << std::endl;
      if (target_novel == 0)
      {
         Tuple single = {*value_};
         decided.push_back(single);
      }
      else if (target_novel > 0)
      {
         decided = find_combination(choice, target_novel);
         for (
            auto combination_ = decided.begin();
            combination_ != decided.end(); combination_++
         )
         {
            combination_->push_back(*value_);
         }
         std::cout << "how many:" << decided.size() << std::endl;
      }
      Many_tuple previous = concatenate(previous, decided);
   }
   return whole;
}

Many_tuple concatenate(
   Many_tuple this_many_tuple, Many_tuple that_many_tuple
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

void print_tuple(Many_tuple many_tuple)
{
   for (
      auto tuple_ = many_tuple.begin();
      tuple_ != many_tuple.end(); tuple_++
   )
   {
      std::cout << "[";
      for (
         auto value_ = tuple_->begin();
         value_ != tuple_->end(); value_++
      )
      {
         std::cout << *value_ << ",";
      }
      std::cout << "]" << std::endl;
   }
}

int main()
{
   Tuple choice = {2, 3, 5};
   int target = 8;
   Many_tuple many_tuple = find_combination(choice, target);
   print_tuple(many_tuple);
   // [2,2,2,2,]
   // [2,3,3,]
   // [3,5,]
}
