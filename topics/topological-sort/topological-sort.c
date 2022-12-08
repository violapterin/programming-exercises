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
      int hold = find_maximum_numeral(content);
      if (hold > maximum)
         maximum = hold;
   }
   fclose(stream_file);

   bool* graph[maximum];
   printf("number vertex: %d\n", maximum);
   for (int row = 0; row <= maximum - 1; row++)
      graph[row] = (bool*) malloc(maximum * sizeof(bool));
   for (int row = 0; row <= maximum - 1; row++)
      for (int column = 0; column <= maximum - 1; column++) {
         graph[row][column] = false;
      }

   stream_file = fopen(argv[1], "r");
   while (fgets(content, LIMIT_LENGTH_LINE, stream_file) != NULL)
      construct_vertex(content, graph);
   fclose(stream_file);

   int flag = strtol(argv[2], NULL, 1);
   sort_topological(flag, maximum, graph);
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
      printf("vertex:%d\n", target + 1); // // 1 based
      for (int row = 0; row <= maximum - 1; row++)
         graph[row][target] = false;
      active[target] = false;
   }
}

void construct_vertex(char* source, bool** graph)
{
   printf("source: %s", source);
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
   left = right + 1;
   count += 1;
   while (count != length - 1) {
      while (!isalnum(*left)) {
         left += 1;
         count += 1;
         continue;
      }
      right = left;
      while (isalnum(*right)) {
         right += 1;
         count += 1;
         continue;
      }
      int numeral_another = strtol(left, NULL, 10);
      printf("constructing edge %d, %d:\n", numeral_main, numeral_another);
      graph[numeral_main - 1][numeral_another - 1] = true; // // 0 based
      left = right + 1;
      right = left;
      count += 1;
   }
}

int find_maximum_numeral(char* source)
{
   int count = 0;
   int length = strlen(source);
   int maximum = 0;
   char* left = source;
   char* right = source;
   while (count != length - 1) {
      while (!isalnum(*left)) {
         left += 1;
         count += 1;
         continue;
      }
      while (isalnum(*right)) {
         right += 1;
         count += 1;
         continue;
      }
      int hold = strtol(left, NULL, 10);
      if (hold > maximum)
         maximum = hold;
      left = right + 1;
      right = left;
      count += 1;
   }
   return maximum;
}
