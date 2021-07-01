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
#include <cassert>
typedef std::vector<std::string> Answer;
typedef std::vector<Answer> Many_answer;
typedef std::vector<int> Many_spot;
typedef std::set<int> Many_valid;
typedef std::pair<Many_spot, Many_valid> Record;
typedef std::vector<Record> Many_record;
Many_answer solve(int);
Many_valid select(int, int, Many_valid);
Record concatenate(int, int, Record);
bool be_connected(int, int, int);
Many_record initialize_record(int);
Answer convert(int, Record);
void print_answer(Answer);
void print_many_valid(Many_valid); // XXX

int main()
{
   Many_answer many_answer = solve(4);
   for (
      auto answer_ = many_answer.begin();
      answer_ != many_answer.end(); answer_++
   )
   {
      print_answer(*answer_);
   }
   // ".Q.., ...Q, Q..., ..Q."
   // "..Q., Q..., ...Q, .Q.."
}

Many_answer solve(int width)
{
   // int half = (width + 1) % 2;
   Many_record many_record = initialize_record(width);
   for (int row = 0; row <= width - 2; row++)
   {
      Many_record many_updated;
      for (
         auto record_ = many_record.begin();
         record_ != many_record.end(); record_++
      )
      {
         Many_valid many_chosen = select(width, row, record_->second);
         if (many_chosen.empty())
            continue;
         for (
            auto spot_ = many_chosen.begin();
            spot_ != many_chosen.end(); spot_++
         )
         {
            Record updated = concatenate(width, *spot_, *record_);
            many_updated.push_back(updated);
            //print_many_valid(updated.second);
         }
      }
      many_record = many_updated;
   }
   Many_record many_filtered;
   for (
      auto record_ = many_record.begin();
      record_ != many_record.end(); record_++
   )
   {
      std::cout << "how many " << record_->first.size() << std::endl;
      if (record_->first.size() >= 2) // XXX
         many_filtered.push_back(*record_);
   }
   Many_answer many_answer;
   for (
      auto filtered_ = many_filtered.begin();
      filtered_ != many_filtered.end(); filtered_++
   )
      many_answer.push_back(convert(width, *filtered_));
   return many_answer;
}

bool be_connected(int width, int this_spot, int that_spot)
{
   int this_column = this_spot % width;
   int that_column = that_spot % width;
   int this_row = (this_spot - this_column) / width;
   int that_row = (that_spot - that_column) / width;
   if (this_column == that_column)
      return true;
   if (this_row == that_row)
      return true;
   int step = std::abs(this_spot - that_spot);
   if (step % (width - 1) == 0)
      return true;
   if (step % (width + 1) == 0)
      return true;
   return false;
}

Many_valid select(int width, int the_row, Many_valid many_valid)
{
   Many_valid many_chosen;
   for (
      auto valid_ = many_valid.begin();
      valid_ != many_valid.end(); valid_++
   )
   {
      int column = *valid_ % width;
      if (the_row == (*valid_ - column) / width);
         many_chosen.insert(*valid_);
   }
   return many_chosen;
}

void print_many_valid(Many_valid many_valid)
{
   for (
      auto valid_ = many_valid.begin();
      valid_ != many_valid.end(); valid_++
   )
   {
      std::cout << *valid_ << ", ";
   }
   std::cout << std::endl;
}

Record concatenate(int width, int spot, Record record_old)
{
   Many_spot many_spot = record_old.first;
   many_spot.push_back(spot);
   Many_valid many_valid;
   for (
      auto valid_ = record_old.second.begin();
      valid_ != record_old.second.end(); valid_++
   )
   {
      if (!be_connected(width, spot, *valid_))
         many_valid.insert(*valid_);
   }
   Record record_new = std::make_pair(many_spot, many_valid);
   return record_new;
}

Many_record initialize_record(int width)
{
   Many_valid many_valid;
   for (int valid = 0; valid <= width * width - 1; valid++)
      many_valid.insert(valid);
   Many_spot many_spot;
   Record record = std::make_pair(many_spot, many_valid);
   Many_record many_record = {record};
   return many_record;
}

Answer convert(int width, Record record)
{
   Answer answer;
   Many_spot many_spot = record.first;
   for (int the_row = 0; the_row <= width - 1; the_row++)
   {
      //std::cout << "convert row" << the_row << std::endl;
      std::string display = std::string(width, '.');
      for (
         auto spot_ = many_spot.begin();
         spot_ != many_spot.end(); spot_++
      )
      {
         //std::cout << "spot " << *spot_ << std::endl;
         int column = *spot_ % width;
         //std::cout << "column " << *spot_ % width << std::endl;
         //std::cout << "row " << (*spot_ - column) / width << std::endl;
         if (the_row == (*spot_ - column) / width)
         {
            display[column] = 'Q';
            //std::cout << "display" << display << std::endl;
         }
      }
      //std::cout << "final display" << display << std::endl;
      answer.push_back(display);
   }
   return answer;
}

void print_answer(Answer answer)
{
   for (
      auto line_ = answer.begin();
      line_ != answer.end(); line_++
   )
      std::cout << *line_ << ", ";
   std::cout << std::endl;
}
