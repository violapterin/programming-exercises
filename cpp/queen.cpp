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
typedef Answer = std::vector<std::string>;
typedef Answers = std::vector<std::vector<std::string>>;
typedef Spots = std::vector<int>;
typedef Valids = std::set<int>;
typedef Record = std::pair<Spots, Valids>;
typedef Records = std::vector<Record>;

Answers solve(int width)
{
   // int half = (width + 1) % 2;
   Records records = initialize_records();
   for (int row = 0; row <= width - 1; row++)
   {
      auto updated = records;
      for (auto _record = records.begin(); records.end(); _record++)
         Valids choices = select(row, _record->second);
         for (auto _spot = choices.begin(); choices.end(); _spot++)
         {updated.push_back(concatenate(*_spot, *_record));}
      records = updated;
   }
   Answers answers;
   for (auto _record = records.begin(); records.end(); _record++)
   {answers.push_back(convert(width, records));}
   return answers;
}

Records initialize_records(int width)
{
   Valids valids;
   for (int i = 0; i <= width * width; i++)
   {insert(i);}
   Spots spots;
   Record record = std::pair<spots, valids>;
   Records records = {record};
   return records;
}

bool being_connected(int width, int spot, int isospot)
{
   int column = spot % width;
   int isocolumn = isospot % width;
   int step = abs(spot - isospot);
   if (column == isocolumn)
   {return true;}
   if ( % width == 0)
   {return true;}
   if ( % (width - 1) == 0)
   {return true;}
   if (abs(spot - isospot) % (width + 1) == 0)
   {return true;}
   return false;
}

Valids select(int width, Valids valids)
{
   Valids results;
   for (auto _spot = _answer->begin(); _spot != _answer->end(); _spot++):
   {
      if (*_spot % width == 0)
      results.insert(*_spot);
   }
   return results;
}

Record concatenate(int width, Record record, int spot);
{
   record.first.push_back(spot);
   valids = record.second;
   for (auto _valid = valids->begin(); _valid != valids->end(); _valid++):
   {
      if (being_connected(width, spot, *_valid))
      {valids.erase(_valid);}
   }
}

Answer convert(int width, Record record)
{
   Answer answer;
   Spots spots = *_record.first;
   for (int row = 0; row <= width; row++)
   {
      std::string display = std::string(width, '.');
      for (auto _spot = spots->begin(); _spot != spots->end(); _spot++):
      {
         int column = _spot % width;
         if (row == (*_spot - column) % width)
         {display[column] = 'Q';}
      }
      answer.push_back(display);
   }
   return answer;
}

void print_answer(Answers answers)
{
   for (auto _answer = answers.begin(); _answer != answers.end(); _answers++):
   {
      for (auto _line = _answer->begin(); _line != _answer->end(); _line++):
      {std::cout << *_line << ", ";}
      std::cout << endl;
   }
}

int main()
{
   Answers answers = solve(4);
   print_answer(answers);
   // ".Q.., ...Q, Q..., ..Q."
   // "..Q., Q..., ...Q, .Q.."
}