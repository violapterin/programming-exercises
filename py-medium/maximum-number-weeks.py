#! /usr/bin/env python3

# 1953. Maximum Number of Weeks for Which You Can Work [medium]
'''
   There are `size` projects numbered from `0` to `size - 1`. You
are given an integer array milestones where each `milestones[index]`
denotes the number of milestones the ith project has.
   You can work on the projects following these two rules:
   Every week, you will finish exactly one milestone of one
project. You must work every week.
   You cannot work on two milestones from the same project for
two consecutive weeks.
   Once all the milestones of all the projects are finished, or
if the only milestones that you can work on will cause you to
violate the above rules, you will stop working. Note that you may
not be able to finish every project's milestones due to these
constraints.
   Return the maximum number of weeks you would be able to work
on the projects without violating the rules mentioned above.
   Constraints:
   `size == milestones.length`
   `1 <= size <= 10^5`
   `1 <= milestones[index] <= 10^9`
'''
# Accepted August 5, 2021

import typing as TYPE

def main():
   bound = [5, 2, 1]
   solution = Solution()
   number = solution.find_number_round(bound)
   print("There are", number, "weeks.")
   # 7

class Solution:

   def find_number_round(self, array: TYPE.List[int]) -> int:
      total = sum(array)
      big = max(array)
      remain = total - big
      if (remain < big):
         return (total + remain - big + 1)
      return total

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()