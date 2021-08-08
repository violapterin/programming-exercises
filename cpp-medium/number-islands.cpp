// 200. Number of Islands [medium]
/*
   Given an `height` by `width` planar binary grid which represents
a map of '1' (land) and '0' (water), return the number of islands.
   An island is surrounded by water and is formed by connecting
adjacent lands horizontally or vertically. You may assume all four
edges of the grid are all surrounded by water.
*/

#include <iostream>
#include <vector>
#include <set>
typedef std::vector<char> Row;
typedef std::vector<Row> Chart;
typedef std::set<int> Node;
typedef std::vector<Node> Tree;
typedef std::vector<bool> Mark;
int count_island(Chart&);
void spread(Tree&, int, Mark&);
void initialize_tree(Chart&, Tree&);
void initialize_mark(Chart&, Mark&);

int main()
{
   Row row_1 = {'1', '1', '0', '0', '0'};
   Row row_2 = {'1', '1', '0', '0', '0'};
   Row row_3 = {'0', '0', '1', '0', '0'};
   Row row_4 = {'0', '0', '0', '1', '1'};
   Chart chart = {row_1, row_2, row_3, row_4};
   int count = count_island(chart);
   std::cout << "There are " << count << " islands." << std::endl;
   // "3"
}


int count_island(Chart& chart)
{
   Tree tree;
   initialize_tree(chart, tree);
   Mark mark;
   initialize_mark(chart, mark);
   int present = 0;
   int count = 0;
   int total = chart.size() * chart[0].size();
   while (present < total)
   {
      if (chart[present] == '0') { continue; }
      if (!mark[present])
      {
         count += 1;
         mark[present] = true;
         spread(tree, present, mark);
      }
      present += 1;
   }
   return count;
}

void spread(Tree& tree, int start, Mark& mark)
{
   Node local;
   for (
      auto visit_ = tree[start].begin();
      visit_ != tree[start].end(); visit_++
   )
   {
      if (!mark[*visit_])
      {
         local.insert(*visit_);
         mark[*visit_] = true;
      }
   }
   for (
      auto visit_ = local.begin();
      visit_ != local.end(); visit_++
   )
   {
      spread(tree, *visit_, mark);
   }
}

void initialize_tree(Chart& chart, Tree& tree)
{
   int height = chart.size();
   int width = chart[0].size();
   for (int row = 0; row < chart.size(); row++)
   {
      for (int column = 0; column < chart[row].size(); column++)
      {
         tree.push_back(Node());
      }
   }
   for (int row = 0; row + 1 < height; row++)
   {
      for (int column = 0; column < width; column++)
      {
         int last = row * width + column;
         int next = (row + 1) * width + column;
         if (chart[row][column] == '1' && chart[row + 1][column] == '1')
         {
            tree[last].insert(next);
            tree[next].insert(last);
         }
      }
   }
   for (int row = 0; row < height; row++)
   {
      for (int column = 0; column + 1 < width; column++)
      {
         int last = row * width + column;
         int next = row * width + column + 1;
         if (chart[row][column] == '1' && chart[row][column + 1] == '1')
         {
            tree[last].insert(next);
            tree[next].insert(last);
         }
      }
   }
}

void initialize_mark(Chart& chart, Mark& mark)
{
   int height = chart.size();
   int width = chart[0].size();
   mark.reserve(height * width);
   for (int row = 0; row < height; row++)
   {
      for (int column = 0; column + 1 < width; column++)
      {
         int index = row * width + column;
         mark[index] = false;
      }
   }
}