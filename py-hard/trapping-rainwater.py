#! /usr/bin/env python3

# 42. Trapping Rain Water [hard]
'''
Given `size` non-negative integers representing an elevation map
`rain` where the width of each bar is `1`, compute how much water
it can trap after raining.
   `0 <= size <= 3 * 10^4`
   `0 <= rain[i] <= 10^5`
'''
# Accepted ________, 2021

import typing as TYPE

def main():
   #rain = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1] # 6
   rain = [4,2,0,3,2,5] # 5
   solution = Solution()
   number = solution.count_trap(rain)
   print("There are", number, "drops.")
   # 6

class Solution:

   def count_trap(self, rain: TYPE.List[int]) -> int:
      print("rain:", rain)
      if (len(rain) <= 1):
         return 0
      left = self.probe_increasing(rain)
      if left > 0:
         return self.count_trap(rain[left:])
      middle = self.probe_decreasing(rain)
      if middle >= len(rain) - 1:
         return 0
      right = middle + self.probe_increasing(rain[middle:])
      rain_left = rain[:right + 1]
      rain_right = rain[right:]
      print("rain_left:", rain_left)
      print("rain_right:", rain_right)
      limit = min(rain_left[0], rain_left[-1])
      water = sum([max(0, limit - value) for value in rain_left])
      print("water:", water)
      return water + self.count_trap(rain_right)

   def probe_decreasing(self, rain: TYPE.List[int]) -> int:
      if (len(rain) <= 1):
         return 0
      last = rain[0]
      head = 1
      while head < len(rain):
         if (rain[head] <= last):
            last = rain[head]
         else:
            break
         head += 1
      return head - 1

   def probe_increasing(self, rain: TYPE.List[int]) -> int:
      if (len(rain) <= 1):
         return 0
      last = rain[0]
      head = 1
      while head < len(rain):
         if (rain[head] >= last):
            last = rain[head]
         else:
            break
         head += 1
      return head - 1
            

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()