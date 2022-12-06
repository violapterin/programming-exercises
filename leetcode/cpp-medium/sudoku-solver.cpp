// 37. Sudoku Solver [hard]
/*
   Write a program to solve a Sudoku puzzle by filling the empty
cells. A sudoku solution must satisfy all of the following rules:
   Each of the digits 1-9 must occur exactly once in each row. Each
of the digits 1-9 must occur exactly once in each column. Each of
the digits 1-9 must occur exactly once in each of the 9 3- by- 3
sub-boxes of the grid.
   The '.' character indicates empty cells.
   Constraints:
   `board.length == 9`
   `board[i].length == 9`
   `board[i][j]` is a digit or '.'.
   It is guaranteed that the input board has only one solution.
*/

#include <iostream>
#include <vector>
typedef std::vector<char> Row;
typedef std::vector<Row> Board;
void solve_sudoku(Board&);
void print_sudoku(Board&);
int main()
{
   Row row_1 = {'5' ,'3' ,'.' ,'.' ,'7' ,'.' ,'.' ,'.' ,'.'};
   Row row_2 = {'6' ,'.' ,'.' ,'1' ,'9' ,'5' ,'.' ,'.' ,'.'};
   Row row_3 = {'.' ,'9' ,'8' ,'.' ,'.' ,'.' ,'.' ,'6' ,'.'};
   Row row_4 = {'8' ,'.' ,'.' ,'.' ,'6' ,'.' ,'.' ,'.' ,'3'};
   Row row_5 = {'4' ,'.' ,'.' ,'8' ,'.' ,'3' ,'.' ,'.' ,'1'};
   Row row_6 = {'7' ,'.' ,'.' ,'.' ,'2' ,'.' ,'.' ,'.' ,'6'};
   Row row_7 = {'.' ,'6' ,'.' ,'.' ,'.' ,'.' ,'2' ,'8' ,'.'};
   Row row_8 = {'.' ,'.' ,'.' ,'4' ,'1' ,'9' ,'.' ,'.' ,'5'};
   Row row_9 = {'.' ,'.' ,'.' ,'.' ,'8' ,'.' ,'.' ,'7' ,'9'};
   Board board = {
      row_1, row_2, row_3,
      row_4, row_5, row_6,
      row_7, row_8, row_9
   };
   solve_sudoku(board);
   print_sudoku(board);
   /*
   {
      {'5' ,'3' ,'4' ,'6' ,'7' ,'8' ,'9' ,'1' ,'2'},
      {'6' ,'7' ,'2' ,'1' ,'9' ,'5' ,'3' ,'4' ,'8'},
      {'1' ,'9' ,'8' ,'3' ,'4' ,'2' ,'5' ,'6' ,'7'},
      {'8' ,'5' ,'9' ,'7' ,'6' ,'1' ,'4' ,'2' ,'3'},
      {'4' ,'2' ,'6' ,'8' ,'5' ,'3' ,'7' ,'9' ,'1'},
      {'7' ,'1' ,'3' ,'9' ,'2' ,'4' ,'8' ,'5' ,'6'},
      {'9' ,'6' ,'1' ,'5' ,'3' ,'7' ,'2' ,'8' ,'4'},
      {'2' ,'8' ,'7' ,'4' ,'1' ,'9' ,'6' ,'3' ,'5'},
      {'3' ,'4' ,'5' ,'2' ,'8' ,'6' ,'1' ,'7' ,'9'}
   }
   */
}

void solve_sudoku(Board&)
{
}

void print_sudoku(Board&)
{
}
