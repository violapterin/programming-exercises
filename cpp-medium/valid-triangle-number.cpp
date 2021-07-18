// 611. Valid Triangle Number [medium]
/*
   Given an integer array `choice`, return the number of triplets
chosen from the array that can make triangles if we take them
as side lengths of a triangle.
   `1 <= choice.length <= 1000`
   `0 <= choice[i] <= 1000`
*/

#include <iostream>
#include <vector>
typedef std::vector<int> Array;
int count_triangle_number(Array&);

int main()
{
   int array = {2, 2, 3, 4};
   int count = count_triangle_number(Array&);
   std::cout << count << std::endl;
   // "3"
   /* (2,3,4), (2,3,4), (2,2,3) */
}
