#include <stdio.h> // fgets, printf
#include <stdlib.h> // strtol
#include <ctype.h> // isalnum
#include <stdbool.h> // bool
#include <string.h> // strlen
#define LIMIT_LENGTH_LINE 512
#define FLAG_USUAL_RESULT_TERMINAL 0
#define FLAG_USUAL_RESULT_FILE 1
#define FLAG_COMPLEXITY_RESULT_TERMINAL 2
#define FLAG_COMPLEXITY_RESULT_FILE 3

void sort_topological(int, int, int*, bool**);
void construct_vertex(char* , bool**);
int find_maximum_numeral(char*);
void print_graph(int, bool**); // XXX

// argv[0]: program name
// argv[1]: flag
// argv[2]: input filename
// argv[3]: output filename
int main(int argc, char** argv)
{
   char* string_program = argv[0];
   char* string_flag = argv[1];
   char* string_input = argv[2];
   char* string_output = argv[3];

   FILE* stream_file = fopen(string_input, "r");
   char content[LIMIT_LENGTH_LINE];
   int maximum = 0;
   while (fgets(content, LIMIT_LENGTH_LINE, stream_file) != NULL) {
      int hold = find_maximum_numeral(content);
      if (hold > maximum)
         maximum = hold;
   }
   fclose(stream_file);

   bool* graph[maximum];
   for (int row = 0; row <= maximum - 1; row++)
      graph[row] = (bool*) malloc(maximum * sizeof(bool));
   for (int row = 0; row <= maximum - 1; row++)
      for (int column = 0; column <= maximum - 1; column++) {
         graph[row][column] = false;
      }

   stream_file = fopen(string_input, "r");
   while (fgets(content, LIMIT_LENGTH_LINE, stream_file) != NULL)
      construct_vertex(content, graph);
   fclose(stream_file);

   // print_graph(maximum, graph); // XXX
   int complexity[maximum];
   for (int row = 0; row <= maximum - 1; row++)
      for (int column = 0; column <= maximum - 1; column++)
         complexity[row] = 0;
   int flag = strtol(string_flag, NULL, 1);
   sort_topological(flag, maximum, complexity, graph);
}

void sort_topological(int flag, int maximum, int* complexity, bool** graph)
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
      int trivial = true;
      for (int column = 0; column <= maximum - 1; column++)
         if (active[column]) {
            trivial = false;
            break;
         }
      if (trivial)
         break;

      int target = -1;
      for (int column = 0; column <= maximum - 1; column++) {
         if (!active[column])
            continue;
         bool with_arrival = false;
         for (int row = 0; row <= maximum - 1; row++)
            if (graph[row][column]) {
               with_arrival = true;
               break;
            }
         if (!with_arrival)
            target = column;
      }

      if (target != -1) {
         printf("vertex: %d\n", target + 1); // // 1 based
         for (int column = 0; column <= maximum - 1; column++)
            graph[target][column] = false;
         active[target] = false;
      }
      else {
         printf("cycle!\n");
         break;
      }
   }
}

void construct_vertex(char* source, bool** graph)
{
   // printf("source: %s", source); // XXX
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
      // printf("constructing edge %d, %d:\n", numeral_main, numeral_another); // XXX
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

void print_graph(int maximum, bool** graph)
{
   for (int row = 0; row <= maximum - 1; row++) {
      for (int column = 0; column <= maximum - 1; column++) {
         if (graph[row][column])
            printf("1");
         else
            printf("0");
         printf(" ");
      }
      printf("\n");
   }
}