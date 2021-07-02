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
void print_many_spot(Many_spot); // XXX

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
   for (int row = 0; row <= width - 1; row++)
   {
      std::cout << "ROW: " << row << std::endl;
      Many_record many_updated;
      auto record_ = many_record.begin();
      while (record_ != many_record.end())
      {
         std::cout << "record spot:" << std::endl;
         print_many_spot(record_->first);
         std::cout << "record valid:" << std::endl;
         print_many_valid(record_->second);
         Many_valid many_chosen = select(width, row, record_->second);
         if (many_chosen.empty())
         {
            record_ = many_record.erase(record_);
            continue;
         }
         for (
            auto spot_ = many_chosen.begin();
            spot_ != many_chosen.end(); spot_++
         )
         {
            Record updated = concatenate(width, *spot_, *record_);
            many_updated.push_back(updated);
            //std::cout << "  choosing:" << *spot_ << std::endl;
            //std::cout << "  updated:" << std::endl;
            //std::cout << "  ";
            print_many_valid(updated.second);
         }
         record_++;
      }
      many_record = many_updated;
   }
   Many_record many_filtered;
   for (
      auto record_ = many_record.begin();
      record_ != many_record.end(); record_++
   )
   {
      if (record_->first.size() >= width - 1)
      {
         many_filtered.push_back(*record_);
      }
   }
   Many_answer many_answer;
   for (
      auto filtered_ = many_filtered.begin();
      filtered_ != many_filtered.end(); filtered_++
   )
   {
      many_answer.push_back(convert(width, *filtered_));
   }
   return many_answer;
}

bool be_connected(int width, int this_unordered, int that_unordered)
{
   int this_spot = this_unordered;
   int that_spot = that_unordered;
   if (this_spot > that_spot)
   {
      that_spot = this_unordered;
      this_spot = that_unordered;
   }
   //std::cout << "checking spots "
   //   << this_spot << ", " << that_spot << std::endl;

   bool whether_connected = false;
   int this_column = this_spot % width;
   int that_column = that_spot % width;
   int this_row = (this_spot - this_column) / width;
   int that_row = (that_spot - that_column) / width;
   int step = that_spot - this_spot;
   if (this_column == that_column)
   {
      //std::cout << "same column" << std::endl;
      whether_connected = true;
   }
   else if (this_row == that_row)
   {
      //std::cout << "same row" << std::endl;
      whether_connected = true;
   }
   else if (
      step % (width - 1) == 0
      && this_spot % width - that_spot % width == step / (width - 1)
   )
   {
      //std::cout << "left down to right up" << std::endl;
      whether_connected = true;
   }
   else if (
      step % (width + 1) == 0
      && that_spot % width - this_spot % width == step / (width + 1)
   )
   {
      //std::cout << "left up to right down" << std::endl;
      whether_connected = true;
   }
   //if (whether_connected)
   //{std::cout << "connected!" << std::endl;}
   return whether_connected;
}

// 0, 1, 2, 3
// 4, 5, 6, 7
// 8, 9, 10, 11
// 12, 13, 14, 15

Many_valid select(int width, int the_row, Many_valid many_valid)
{
   Many_valid many_chosen;
   //std::cout << "the row:" << the_row << std::endl;
   for (
      auto valid_ = many_valid.begin();
      valid_ != many_valid.end(); valid_++
   )
   {
      //std::cout << "valid:" << *valid_ << std::endl;
      int column = *valid_ % width;
      if (the_row == (*valid_ - column) / width)
      {
         //std::cout << "insert:" << *valid_ << std::endl;
         many_chosen.insert(*valid_);
      }
   }
   //print_many_valid(many_chosen);
   return many_chosen;
}

void print_many_spot(Many_spot many_spot)
{
   for (
      auto spot_ = many_spot.begin();
      spot_ != many_spot.end(); spot_++
   )
   {
      std::cout << *spot_ << ", ";
   }
   std::cout << std::endl;
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
      {
         many_valid.insert(*valid_);
      }
   }
   Record record_new = std::make_pair(many_spot, many_valid);
   return record_new;
}

Many_record initialize_record(int width)
{
   Many_valid many_valid;
   for (int valid = 0; valid <= width * width - 1; valid++)
   {
      many_valid.insert(valid);
   }
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
      std::string display = std::string(width, '.');
      for (
         auto spot_ = many_spot.begin();
         spot_ != many_spot.end(); spot_++
      )
      {
         int column = *spot_ % width;
         if (the_row == (*spot_ - column) / width)
         {
            display[column] = 'Q';
         }
      }
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
   {
      std::cout << *line_ << ", ";
   }
   std::cout << std::endl;
}
