// 42. Trapping Rain Water [hard]
/*
Given `n` non-negative integers representing an elevation map
where the width of each bar is `1`, compute how much water
it can trap after raining.
   `n == height.length`
   `0 <= n <= 3 * 10^4`
   `0 <= height[i] <= 10^5`
*/
// Accepted June 29, 2021.

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cassert>
typedef std::vector<int> Rain;
int find_index_biggest(Rain);
int trap(Rain rain);

int main()
{
   Rain v = {0,1,0,2,1,0,1,3,2,1,2,1};
   std::cout << trap(v) << std::endl;
   // "6"
}

int trap(Rain rain)
{
   if (rain.size() <= 2)
      return 0;
   int index_first = find_index_biggest(rain);
   auto clip = rain;
   clip.erase(clip.begin() + index_first);
   int index_second = find_index_biggest(clip);
   if (index_second >= index_first)
      index_second += 1;
  
   int index_left = index_first;
   int index_right = index_second;
   if (index_first > index_second)
   {
      index_left = index_second;
      index_right = index_first;
   }
   auto left = rain.begin() + index_left;
   auto right = rain.begin() + index_right;
   int surface = rain[index_second];
   int already = 0;
   for (auto head = left + 1; head != right; head++){
      int step = surface - *head;
      if (step >= 0)
         already += step;
   }
   auto subrain = rain;
   auto subleft = subrain.begin() + index_left;
   auto subright = subrain.begin() + index_right;
   subrain.erase(subleft, subright);
   subrain[index_left] = surface;
   int result = trap(subrain) + already;
   return result;
}

int find_index_biggest(Rain rain)
{
   int hold = 0;
   int index = 0;
   for(auto head=rain.begin(); head!=rain.end(); head++){
      if (hold < *head){
         hold = *head;
         index = head - rain.begin();
      }
   }
   return index;
}