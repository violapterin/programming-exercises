#include <stdio.h> // fgets, printf
#include <stdlib.h> // strtol
#include <ctype.h> // isalnum
#include <stdbool.h> // bool
#include <string.h> // strlen
#define LIMIT_LENGTH 4096
#define FLAG_USUAL 0
#define FLAG_COMPLEXITY 1

void sort_topological(int, int, bool**);
void construct_graph(int, char* , bool**);
void feed_vertex(int, char*, bool**);
int find_maximum_numeral(int, char*);


// argv[1]: input filename
// argv[2]: flag
int main(int argc, char** argv)
{
   // //    stackoverflow.com/questions/11793689/
   // //    read-the-entire-contents-of-a-file-to-c-char-including-new-lines
   FILE *stream;
   char *content;
   stream = fopen(argv[1], "r");
   fseek(stream, 0, SEEK_END);
   int size_file = ftell(stream);
   fseek(stream, 0L, SEEK_SET);
   content = malloc(size_file + 1);
   size_t length = fread(content, 1, size_file, stream);
   content[length] = 0;
   // printf("content:\n%s", content);
   fclose(stream);

   int number_vertex = find_maximum_numeral(length, content);

   /*
   bool* graph[number_vertex];
   printf("number vertex: %d", number_vertex);
   for (int row = 0; row <= number_vertex - 1; row++)
      graph[row] = (bool*) malloc(number_vertex * sizeof(bool));
   for (int row = 0; row <= number_vertex - 1; row++)
      for (int column = 0; column <= number_vertex - 1; column++) {
         printf("constructing row %d column %d:\n", row, column);
         graph[row][column] = false;
      }
   */

   /*
   construct_graph(length, content, graph);

   int flag = strtol(argv[2], NULL, 1);
   sort_topological(flag, number_vertex, graph);
   */
}

void sort_topological(int flag, int number_vertex, bool** graph)
{
   bool active[number_vertex];
   for (int row = 0; row <= number_vertex - 1; row++)
      active[row] = false;
   for (int row = 0; row <= number_vertex - 1; row++)
      for (int column = 0; column <= number_vertex - 1; column++) {
         if (graph[row][column]) {
            active[row] = true;
            active[column] = true;
         }
      }

   while (true) {
      bool trivial = true;
      for (int column = 0; column <= number_vertex - 1; column++)
         if (active[column]) {
            trivial = false;
            break;
         }
      if (trivial)
         break;

      int target = 0;
      bool skipped = true;
      for (int column = 0; column <= number_vertex - 1; column++) {
         if (!active[column])
            continue;
         skipped = false;
         bool with_arrival = false;
         for (int row = 0; row <= number_vertex - 1; row++)
            if (graph[row][column]) {
               with_arrival = true;
               break;
            }
         if (!with_arrival)
            target = column;
      }
      if (skipped) {
         printf("cycle!");
         break;
      }
      printf("vertex:%d\n", target);
      for (int row = 0; row <= number_vertex - 1; row++)
         graph[row][target] = false;
      active[target] = false;
   }
}

void construct_graph(int length, char* source, bool** graph)
{
   int count = 0;
   char* left = source;
   char* right = source;
   while (count != length) {
      if (isalnum(*right)) {
         right += 1;
         count += 1;
         continue;
      }
      feed_vertex(right - left, left, graph);
      left = right + 1;
      while (!isalnum(*left)) {
         left += 1;
         count += 1;
      }
      right = left;
   }
}

void feed_vertex(int length, char* left, bool** graph)
{
   int count = 0;
   char* right = left;
   while (!isalnum(*left)) {
      left += 1;
      count += 1;
   }
   right = left;
   while (isalnum(*right)) {
      right += 1;
      count += 1;
   }
   int numeral_main = strtol(left, NULL, right - left);
   while (!isalnum(*left)) {
      left += 1;
      count += 1;
   }
   right = left;
   while (count != length) {
      if (isalnum(*right)) {
         right += 1;
         count += 1;
         continue;
      }
      int numeral_another = strtol(left, NULL, right - left);
      graph[numeral_main][numeral_another] = true;
      left = right + 1;
      while (!isalnum(*left)) {
         left += 1;
         count += 1;
      }
      right = left;
   }
}

int find_maximum_numeral(int length, char* source)
{
   int maximum = 0;
   int count = 0;
   char* left = source;
   char* right = source;
   printf("right:%s", *right);
   while (count != length) {
      if (isalnum(*right)) {
         right += 1;
         count += 1;
         continue;
      }
      int hold = strtol(left, NULL, right - left);
      if (hold > maximum)
         maximum = hold;
      left = right + 1;
      while (!isalnum(*left)) {
         left += 1;
         count += 1;
      }
      right = left;
   }
   return maximum;
}
