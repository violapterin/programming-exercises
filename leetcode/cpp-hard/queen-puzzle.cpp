// 51. N-Queens [hard]
/*
   The `n` queens puzzle is the problem of placing `n` queens on an
`n` by `n` chessboard such that no two queens attack each other.
   Given a width `n`, return all distinct solutions to the `n` queens
puzzle. You may return the answer in any order. Each solution contains
a distinct board configuration of the `n` queens' placement, where
`'Q'` and `'.'` both indicate a queen and an empty space, respectively.
   `1 <= n <= 9`
*/
// Accepted July 2, 2021

#include <iostream>
#include <string>
#include <vector>
#include <set>
typedef std::vector<std::string> Answer;
typedef std::vector<Answer> Many_answer;
typedef std::vector<int> Many_spot;
typedef std::set<int> Many_valid;
typedef std::pair<Many_spot, Many_valid> Record;
typedef std::vector<Record> Many_record;
Many_answer solve(int);
Record concatenate(int, int, Record);
bool be_connected(int, int, int);
Many_valid select(int, int, Many_valid);
Record find_symmetric(int, Record);
Many_record initialize_record(int);
Answer convert(int, Record);
void print_answer(Answer);

int main()
{
   Many_answer many_answer = solve(4);
   for (
      auto answer_ = many_answer.begin();
      answer_ != many_answer.end(); answer_++
   )
      print_answer(*answer_);
      // ".Q.., ...Q, Q..., ..Q."
      // "..Q., Q..., ...Q, .Q.."
}

Many_answer solve(int width)
{
   int half = (width - 1) / 2;
   Many_record many_record = initialize_record(width);
   for (int row = 0; row <= width - 1; row++)
   {
      Many_record many_updated;
      auto record_ = many_record.begin();
      while (record_ != many_record.end())
      {
         Many_valid many_chosen = select(width, row, record_->second);
         if (many_chosen.empty())
         {
            record_ = many_record.erase(record_);
            continue;
         }
         for (
            auto chosen_ = many_chosen.begin();
            chosen_ != many_chosen.end(); chosen_++
         )
         {
            if (*chosen_ / width == 0 && *chosen_ > half)
               continue;
            Record updated = concatenate(width, *chosen_, *record_);
            many_updated.push_back(updated);
         }
         record_++;
      }
      many_record = many_updated;
   }
   Many_record many_full;
   for (
      auto record_ = many_record.begin();
      record_ != many_record.end(); record_++
   )
   {
      if (record_->first.size() >= width - 1)
         many_full.push_back(*record_);
         if (width % 2 != 1 || record_->first[0] != (width - 1) / 2)
            many_full.push_back(find_symmetric(width, *record_));
   }
   Many_answer many_answer;
   for (
      auto full_ = many_full.begin();
      full_ != many_full.end(); full_++
   )
      many_answer.push_back(convert(width, *full_));
   return many_answer;
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

Many_valid select(int width, int the_row, Many_valid many_valid)
{
   Many_valid many_chosen;
   for (
      auto valid_ = many_valid.begin();
      valid_ != many_valid.end(); valid_++
   )
   {
      int column = *valid_ % width;
      if (the_row == (*valid_ - column) / width)
      {
         many_chosen.insert(*valid_);
      }
   }
   return many_chosen;
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

   int this_column = this_spot % width;
   int that_column = that_spot % width;
   int this_row = (this_spot - this_column) / width;
   int that_row = (that_spot - that_column) / width;
   int step = that_spot - this_spot;
   if (this_column == that_column)
      return true;
   else if (this_row == that_row)
      return true;
   else if (
      step % (width - 1) == 0
      && this_spot % width - that_spot % width == step / (width - 1)
   )
      return true;
   else if (
      step % (width + 1) == 0
      && that_spot % width - this_spot % width == step / (width + 1)
   )
      return true;
   return false;
}

Record find_symmetric(int width, Record given)
{
   Many_spot many_spot_given = given.first;
   Many_valid many_valid_given = given.second;
   Many_spot many_spot;
   Many_valid many_valid;
   for (
      auto spot_ = many_spot_given.begin();
      spot_ != many_spot_given.end(); spot_++
   )
   {
      int column = *spot_ % width;
      int row = (*spot_ - column) / width;
      many_spot.push_back(row * width + (width - 1 - column));
   }
   for (
      auto valid_ = many_valid_given.begin();
      valid_ != many_valid_given.end(); valid_++
   )
   {
      int column = *valid_ % width;
      int row = (*valid_ - column) / width;
      many_valid.insert(row * width + (width - 1 - column));
   }
   Record symmetric = std::make_pair(many_spot, many_valid);
   return symmetric;
}

// // If `width == 4`:
// 0, 1, 2, 3
// 4, 5, 6, 7
// 8, 9, 10, 11
// 12, 13, 14, 15
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
      std::string display = std::string(width, '.');
      for (
         auto spot_ = many_spot.begin();
         spot_ != many_spot.end(); spot_++
      )
      {
         int column = *spot_ % width;
         if (the_row == (*spot_ - column) / width)
            display[column] = 'Q';
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
      std::cout << *line_ << ", ";
   std::cout << std::endl;
}
