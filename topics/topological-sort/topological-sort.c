#include <stdio.h> // fgets, printf
#include <stdlib.h> // strtol
#include <ctype.h> // isalnum
#include <stdbool.h> // bool
#include <string.h> // strlen
#define LIMIT_LENGTH_LINE 32
#define FLAG_USUAL 0
#define FLAG_COMPLEXITY 1

void sort_topological(int, int, bool**);
void construct_vertex(char* , bool**);
int find_maximum_numeral(char*);

/*
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
*/

// argv[1]: input filename
// argv[2]: flag
int main(int argc, char** argv)
{
   FILE* stream_file = fopen(argv[1], "r");
   char content[LIMIT_LENGTH_LINE];
   int maximum = 0;
   while (fgets(content, LIMIT_LENGTH_LINE, stream_file) != NULL) {
      printf("content:%s\n", content);
      int hold = find_maximum_numeral(content);
      if (hold > maximum)
         maximum = hold;
   }
   fclose(stream_file);

   bool* graph[maximum];
   printf("number vertex: %d", maximum);
   for (int row = 0; row <= maximum - 1; row++)
      graph[row] = (bool*) malloc(maximum * sizeof(bool));
   for (int row = 0; row <= maximum - 1; row++)
      for (int column = 0; column <= maximum - 1; column++) {
         printf("constructing row %d column %d:\n", row, column);
         graph[row][column] = false;
      }

   stream_file = fopen(argv[1], "r");
   while (fgets(content, LIMIT_LENGTH_LINE, stream_file) != NULL)
      construct_vertex(content, graph);
   fclose(stream_file);

   /*
   int flag = strtol(argv[2], NULL, 1);
   sort_topological(flag, maximum, graph);
   */
}

void sort_topological(int flag, int maximum, bool** graph)
{
   bool active[maximum];
   for (int row = 0; row <= maximum - 1; row++)
      active[row] = false;
   for (int row = 0; row <= maximum - 1; row++)
      for (int column = 0; column <= maximum - 1; column++) {
         if (graph[row][column]) {
            active[row] = true;
            active[column] = true;
         }
      }

   while (true) {
      bool trivial = true;
      for (int column = 0; column <= maximum - 1; column++)
         if (active[column]) {
            trivial = false;
            break;
         }
      if (trivial)
         break;

      int target = 0;
      bool skipped = true;
      for (int column = 0; column <= maximum - 1; column++) {
         if (!active[column])
            continue;
         skipped = false;
         bool with_arrival = false;
         for (int row = 0; row <= maximum - 1; row++)
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
      for (int row = 0; row <= maximum - 1; row++)
         graph[row][target] = false;
      active[target] = false;
   }
}

void construct_vertex(char* source, bool** graph)
{
   int count = 0;
   int length = strlen(source);
   char* left = source;
   char* right = source;
   while (!isalnum(*left)) {
      left += 1;
      count += 1;
   }
   right = left;
   while (isalnum(*right)) {
      right += 1;
      count += 1;
   }
   int numeral_main = strtol(left, NULL, 10);
   while (!isalnum(*left)) {
      left += 1;
      count += 1;
   }
   right = left;
   while (count != length - 1) {
      if (isalnum(*right)) {
         right += 1;
         count += 1;
         continue;
      }
      int numeral_another = strtol(left, NULL, 10);
      graph[numeral_main][numeral_another] = true;
      left = right + 1;
      while (!isalnum(*left)) {
         left += 1;
         count += 1;
      }
      right = left;
   }
}

int find_maximum_numeral(char* source)
{
   int count = 0;
   int length = strlen(source);
   printf("length:%d\n", length);
   int maximum = 0;
   char* left = source;
   char* right = source;
   while (count != length - 1) {
      while (!isalnum(*left)) {
         left += 1;
         count += 1;
         continue;
      }
      if (isalnum(*right)) {
         right += 1;
         count += 1;
         continue;
      }
      int hold = strtol(left, NULL, 10);
      printf("hold:%d\n", hold);
      if (hold > maximum)
         maximum = hold;
      left = right + 1;
      right = left;
      count += 1;
      continue;
   }
   return maximum;
}
