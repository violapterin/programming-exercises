// 1953. Maximum Number of Weeks for Which You Can Work [medium]
/*
   There are `size` projects numbered from `0` to `size - 1`. You
are given an integer array milestones where each `milestones[index]`
denotes the number of milestones the ith project has.
   You can work on the projects following these two rules:
   Every week, you will finish exactly one milestone of one
project. You must work every week.
   You cannot work on two milestones from the same project for
two consecutive weeks.
   Once all the milestones of all the projects are finished, or
if the only milestones that you can work on will cause you to
violate the above rules, you will stop working. Note that you may
not be able to finish every project's milestones due to these
constraints.
   Return the maximum number of weeks you would be able to work
on the projects without violating the rules mentioned above.
   Constraints:
   `size == milestones.length`
   `1 <= size <= 105`
   `1 <= milestones[index] <= 109`
*/

#include <iostream>
#include <vector>
#include <set>
typedef std::vector<int> Queue;
typedef std::set<Queue*> Record;
int find_number_round(Queue&);
void increment_record(int, Queue&, Record&, Record&);
int find_total(Queue&);

int main()
{
   Queue bound = {5, 2, 1};
   int number = find_number_round(bound);
   std::cout << "There are " << number << " weeks." << std::endl;
   // 7
}

int find_number_round(Queue& bound)
{
   int size = bound.size();
   bound.insert(bound.begin(), 0);
   int total = find_total(bound);
   Queue* initial = new Queue(Queue(size + 1, 0));
   (*initial)[0] = -1;
   Record antique;
   antique.insert(initial);
   int count = 0;
   for (int index = 1; index <= total; index++)
   {
      Record novel;
      increment_record(size, bound, antique, novel);
      //std::cout << "round:" << index << std::endl;
      //std::cout << "novel size:" << novel.size() << std::endl;
      if (novel.empty()) { break; }
      for (
         auto queue_ = antique.begin();
         queue_ != antique.end(); queue_++
      )
      {
         delete (*queue_);
      }
      antique = novel;
      count = index;
   }
   return count;
}

void increment_record(
   int size,
   Queue& bound,
   Record& antique,
   Record& novel
)
{
   for (
      auto queue_ = antique.begin();
      queue_ != antique.end(); queue_++
   )
   {
      int previous = (**queue_)[0];
      for (int index = 1; index <= size; index++)
      {
         if (previous == index) { continue; }
         if ((**queue_)[index] >= bound[index]) { continue; }
         Queue* added = new Queue(**queue_);
         (*added)[index] += 1;
         (*added)[0] = index;
         novel.insert(added);
      }
   }
}

int find_total(Queue& queue)
{
   int amount = 0;
   for (int index = 0; index < queue.size(); index++)
   {
      amount += queue[index];
   }
   return amount;
}