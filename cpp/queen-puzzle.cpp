// Original title: 51. N-Queens [hard]
/*
The `n` queens puzzle is the problem of placing `n` queens on an
`n` by `n` chessboard such that no two queens attack each other.
Given a width `n`, return all distinct solutions to the `n` queens
puzzle. You may return the answer in any order. Each solution contains
a distinct board configuration of the `n` queens' placement, where
`'Q'` and `'.'` both indicate a queen and an empty space, respectively.
*/
#include <iostream>
#include <string>
#include <vector>
#include <set>
typedef std::vector<std::string> Answer;
typedef std::vector<std::vector<std::string>> Answers;
typedef std::vector<int> Spots;
typedef std::set<int> Valids;
typedef std::pair<Spots, Valids> Record;
typedef std::vector<Record> Records;
Answers solve(int);
bool being_connected(int, int, int);
Valids select(int, int, Valids);
Record concatenate(int, int, Record);
Records initialize_records(int);
Answer convert(int, Record);
void print_answer(Answers);

int main()
{
   Answers answers = solve(4);
   print_answer(answers);
   // ".Q.., ...Q, Q..., ..Q."
   // "..Q., Q..., ...Q, .Q.."
}

Answers solve(int width)
{
   // int half = (width + 1) % 2;
   Records records = initialize_records(width);
   for (int row = 0; row <= width - 1; row++)
   {
      Records updated;
      for (auto _record = records.begin(); _record != records.end(); _record++)
      {
         Valids choices = select(width, row, _record->second);
         if (choices.empty())
            continue;
         for (auto _spot = choices.begin(); _spot != choices.end(); _spot++)
            updated.push_back(concatenate(width, *_spot, *_record));
      }
      records = updated;
   }
   Answers answers;
   for (auto _record = records.begin(); _record != records.end(); _record++)
      answers.push_back(convert(width, *_record));
   return answers;
}

bool being_connected(int width, int spot, int isospot)
{
   int column = spot % width;
   int isocolumn = isospot % width;
   int step = abs(spot - isospot);
   if (column == isocolumn)
      return true;
   if (step % width == 0)
      return true;
   if (step % (width - 1) == 0)
      return true;
   if (step % (width + 1) == 0)
      return true;
   return false;
}

Valids select(int width, int row, Valids valids)
{
   Valids results;
   for (auto _valid = valids.begin(); _valid != valids.end(); _valid++)
   {
      int column = *_valid % width;
      if (row == (*_valid - column) % width);
         results.insert(*_valid);
   }
   return results;
}

Record concatenate(int width, int spot, Record record)
{
   Spots spots = record.first;
   Valids valids = record.second;
   Valids isovalids = valids;
   spots.push_back(spot);
   for (auto _valid = valids.begin(); _valid != valids.end(); _valid++)
   {
      if (!being_connected(width, spot, *_valid))
         isovalids.insert(*_valid);
   }
   Record updated = std::make_pair(spots, valids);
   return updated;
}

Records initialize_records(int width)
{
   Valids valids;
   for (int valid = 0; valid <= width * width - 1; valid++)
      valids.insert(valid);
   Spots spots;
   Record record = std::make_pair(spots, valids);
   Records records = {record};
   return records;
}

Answer convert(int width, Record record)
{
   Answer answer;
   Spots spots = record.first;
   for (int row = 0; row <= width; row++)
   {
      std::string display = std::string(width, '.');
      for (auto _spot = spots.begin(); _spot != spots.end(); _spot++)
      {
         int column = *_spot % width;
         if (row == (*_spot - column) % width)
            display[column] = 'Q';
      }
      answer.push_back(display);
   }
   return answer;
}

void print_answer(Answers answers)
{
   for (auto _answer = answers.begin(); _answer != answers.end(); _answer++)
   {
      for (auto _line = _answer->begin(); _line != _answer->end(); _line++)
         std::cout << *_line << ", ";
      std::cout << std::endl;
   }
}