#! /usr/bin/env python3

# 611. Valid Triangle Number [medium]
'''
   Given an integer array `choice`, return the number of triplets
chosen from the array that can make triangles if we take them
as side lengths of a triangle.
   `1 <= choice.length <= 1000`
   `0 <= choice[i] <= 1000`
'''
# Accepted July 19, 2021

import typing as TYPE

def main():
   choice = [2, 2, 3, 4]
   solution = Solution()
   count = solution.count_triangle_number(choice)
   print("There are", count, "valid triplets.")
   # "3"
   # # [2,3,4], [2,3,4], [2,2,3]

class Solution:

   def count_triangle_number(self, choice: TYPE.List[int]) -> int:
      choice.sort()
      distinct = []
      record = []
      key = 0
      cumulative = 0
      for value in choice:
         if (value == 0):
            continue
         self.push_distinct(distinct, value)
         while (key < value):
            record[key] = cumulative
            key += 1
         cumulative += 1
         record[key] = cumulative
      if (distinct.empty()):
         return 0
      while (key < distinct[-1] * 2):
         record[key] = cumulative
         key += 1
      number = self.count_various(record, distinct)
      return number

   def count_various(self,
      record: TYPE.List[int],
      distinct: TYPE.List[int]
   ) -> int:
      if not distinct:
         return 0
      small = distinct[0]
      distinct = distinct[1:]
      number_fixed = self.count_fixed(record, small, distinct)
      number_partial = self.count_various(record, distinct)
      number = number_fixed + number_partial
      return number

   def count_fixed(self,
      record: TYPE.List[int],
      small: int,
      distinct: TYPE.List[int],
   ) -> int:
      number = 0
      novel_small = record[small] - record[small - 1]
      number += self.pick_three(novel_small)
      if not distinct:
         return number
      number += (
         (record[small * 2 - 1] - record[small])
         * self.pick_two(novel_small)
      )
      for value in distinct:
         bound = value + small - 1
         novel_medium = record[value] - record[value - 1]
         if (novel_medium == 0):
            continue
         total_above = record[bound] - record[value]
         add_distinct = total_above * novel_medium
         add_pair_medium = novel_medium * (novel_medium - 1) / 2
         number += novel_small * (add_distinct + add_pair_medium)
      return number

   def push_distinct(self, choice: TYPE.List[int], value: int):
      whether_update = False
      if not choice:
         whether_update = True
      elif (choice[-1] < value):
         whether_update = True
      if (whether_update):
         choice.append(value)

   def pick_two(self, number: int) -> int:
      if (number < 2):
         return 0
      return number * (number - 1) / 2

   def pick_three(self, number: int) -> int:
      if (number < 3):
         return 0
      return number * (number - 1) * (number - 2) / 6

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()