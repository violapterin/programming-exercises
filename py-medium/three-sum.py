#! /usr/bin/env python3

# 15. 3Sum [medium]
'''
   Given an integer array `choice`, return all the triplets
`[choice[i], choice[j], choice[k]]` such that `i != j`, `i != k`,
and `j != k`, and `choice[i] + choice[j] + choice[k] == 0`.
   Notice that the solution set must not contain duplicate triplets.
   Constraints:
   `0 <= choice.length <= 3000`
   `-105 <= choice[i] <= 105`
'''

import typing as TYPE

def main():
   choice = [-1, 0, 1, 2, -1, -4]
   solution = Solution()
   many_triple = solution.find_triple(choice)
   print(many_triple)
   # [[-1, -1, 2], [-1, 0, 1]]

class Solution:

   def find_triple(self,
      choice: TYPE.List[int]
   ) -> TYPE.List[TYPE.List[int]]:
      many_triple = []
      choice.sort()
      record = dict()
      for value in choice:
         record[value] = 0
      for value in choice:
         record[value] += 1
      for index_front in range(len(choice)):
         front_hold = choice[index_front]
         partial = choice[index_front + 1:]
         for index_back in range(len(partial)):
            back_hold = partial[index_back]
            novel_hold = - back_hold - front_hold
            front = front_hold
            novel = novel_hold
            back = back_hold
            if front > novel:
               front, novel = novel, front
            if front > back:
               front, back = back, front
            if novel > back:
               novel, back = back, novel
            if not record.get(front):
               continue
            if not record.get(novel):
               continue
            if not record.get(back):
               continue
            whether_append = False
            if (front == novel):
               if (novel == back):
                  if (record[front] >= 3):
                     whether_append = True
               else:
                  if (record[front] >= 2) and record[back] >= 1:
                     whether_append = True
            else:
               if (novel == back):
                  if (record[front] >= 1) and record[novel] >= 2:
                     whether_append = True
               else:
                  if (record[front] >= 1) and record[novel] >= 1 and record[back] >= 1:
                     whether_append = True
            if whether_append:
               many_triple.append((front, novel, back))
      many_triple = list(set(many_triple))
      many_triple = [list(triple) for triple in many_triple]
      return many_triple
      

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()
