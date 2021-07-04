// Original title: 464. Can I Win [medium]
/*
In the 100 game, two players take turns adding, to a running total,
any integer from `1` to `10`. The player who first causes the running 
total to reach or exceed `100` wins.What if we change the game so that
players cannot re-use integers? For example, two players might take
turns drawing from a common pool of numbers from `1` to `15` without
token replacement until they reach a `total >= 100`. Given two integers
`bound_upper` and `goal`, return true if the first player to move can force
a win, otherwise, return false. Assume both players play optimally.
*/
// Accepted March 1, 2021.

#include <iostream>
#include <unordered_map>
typedef std::unordered_map<int, bool> Many_answer;
int convert(int);
void find_answer(Many_answer&, int, int);
bool can_i_win(int, int);

int main()
{
   if (can_i_win(10, 11))
      std::cout << "Yes!" << std::endl;
   else
      std::cout << "No!" << std::endl;
   // "No!"
}

bool can_i_win(int bound_upper, int goal)
{
   int token = (1 << bound_upper) - 1;
   if (goal <= bound_upper) {return true;}
   if (goal > (bound_upper + 1) * bound_upper / 2)
      return false;
   Many_answer many_answer;
   find_answer(many_answer, token, goal);
   return many_answer[token];
}

void find_answer(Many_answer& many_answer, int token, int total)
{
   if (token == 0)
   {
      many_answer[token] = false;
      return;
   }
   int remain_max = convert(token);
   if (total <= remain_max)
   {
      many_answer[token] = true;
      return;
   }
   for (int remain = 1; remain <= remain_max; remain++)
   {
      int lead = 1 << (remain - 1);
      if (lead & token)
      {
         if (total <= remain)
         {
            many_answer[token] = true;
            return;
         }
         if (many_answer.find(token - lead) == many_answer.end())
            find_answer(many_answer, token - lead, total - remain);
         if (!many_answer[token - lead])
         {
            many_answer[token] = true;
            return;
         }
      }
   }
   many_answer[token] = false;
}

int convert(int token)
{
   double hold = token;
   int result = 0;
   while (hold >= 1 - 1e-9)
   {
      hold /= 2;
      result++;
   }
   return result;
}
