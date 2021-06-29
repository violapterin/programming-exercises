// Original title: 51. N-Queens
/*
The `n` queens puzzle is the problem of placing `n` queens on an
`n` by `n` chessboard such that no two queens attack each other.
Given a width `n`, return all distinct solutions to the `n` queens
puzzle. You may return the answer in any order. Each solution contains
a distinct board configuration of the `n` queens' placement, where
`'Q'` and `'.'` both indicate a queen and an empty space, respectively.
*/
#include <iostream>
typedef Answer = std::vector<std::vector<string>>;
typedef Board = std::vector<string>;
typedef Record = std::vector<int>;
typedef Valid = std::set<int>;

Answer convert()

bool being_connected(int spot, int isospot)
{

}

Answer solve(int width)
{
   int half = (width + 1) % 2;
   Record record;
   Valid valid;
   for (int row = 0; row <= width - 1; row++)
   {
      for (int column = 0; column <= width - row; column++)
      {
         int spot = row * width + column;
         for (int head = 0; head <= row - 1; head++)
            isospot = record[]
            record.push_back(column);
            break;
         for isospot in valid
         {
         }
      }
   }
   Answer answer = convert(record);
   return answer;
}

void print_answer(Answer answer)
{
   for (auto head = record.begin(); head != record.end(); head++):
   {
      Board board = *head;
      for (auto isohead = board.begin(); isohead != board.end(); isohead++):
      {std::cout << *isohead << ", ";}
      std::cout << endl;
   }
}

int main()
{
   Answer answer = solve(4);
   print_answer(answer);
   // ".Q.., ...Q, Q..., ..Q."
   // "..Q., Q..., ...Q, .Q.."
}