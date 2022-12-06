#! /usr/bin/env python3

# 42. Trapping Rain Water [hard]
'''
Given `size` non-negative integers representing an elevation map
`rain` where the width of each bar is `1`, compute how much water
it can trap after raining.
   `0 <= size <= 3 * 10^4`
   `0 <= rain[i] <= 10^5`
'''
# Accepted August 14, 2021

import typing as TYPE

def main():
   rain = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1] # 6
   solution = Solution()
   number = solution.count_trap(rain)
   print("There are", number, "drops.")
   # 6

class Solution:

   def count_trap(self, rain: TYPE.List[int]) -> int:
      return self.count_left(rain, 0, len(rain) - 1)

   def count_left(self,
      rain: TYPE.List[int],
      start: int,
      stop: int
   ) -> int:
      if (stop - start <= 1):
         return 0
      left = self.probe_left(rain, start)
      if (left >= len(rain)):
         return self.count_right(rain, start, stop)
      water_left = sum([max(0, rain[start] - value) for value in rain[start:left+1]])
      water_right = self.count_left(rain, left, stop)
      return water_left + water_right

   def count_right(self,
      rain: TYPE.List[int],
      start: int,
      stop: int
   ) -> int:
      if (stop - start <= 1):
         return 0
      right = self.probe_right(rain, stop)
      if (right < 0):
         return self.count_left(rain, start, stop)
      water_right = sum([max(0, rain[stop] - value) for value in rain[right:stop+1]])
      water_left = self.count_right(rain, start, right)
      return water_left + water_right

   def probe_right(self, rain: TYPE.List[int], start: int) -> int:
      limit = rain[start]
      head = start - 1
      while (head >= 0):
         if (rain[head] >= limit):
            break
         head -= 1
      return head

   def probe_left(self, rain: TYPE.List[int], start: int) -> int:
      limit = rain[start]
      head = start + 1
      while head < len(rain):
         if (rain[head] >= limit):
            break
         head += 1
      return head
            

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()