#include <stdio.h> // fgets, printf
#include <ctype.h> // isalnum
#define LIMIT_SIZE_FILE 4096
#define FLAG_USUAL 0
#define FLAG_COMPLEXITY 1

// argv[0]: input filename
// argv[1]: flag
int main(int argc, char** argv)
{
   char source[LIMIT_SIZE_FILE];
   FILE* document = fopen(argv[0], "r");
   fgets(source, LIMIT_SIZE_FILE, document);
   fclose(document);

   int length = find_size(source);
   int number_vertex = find_maximum_numeral(length, source);
   bool graph[number_vertex][number_vertex];
   for (int row = 0; row <= number_vertex - 1; row++)
      for (int column = 0; column <= number_vertex - 1; column++)
         graph[row][column] = false;

   construct_graph(length, source, graph);

   int flag = argv[1];
   sort_topological(flag, number_vertex, graph);
}

void sort_topological(int flag, int number_vertex, bool** graph)
{
   bool active[number_vertex];
   for (int row = 0; row <= number_vertex - 1; row++)
      active[row] = false;
   for (int row = 0; row <= number_vertex - 1; row++)
      for (int column = 0; column <= number_vertex - 1; column++) {
         active[row] = true;
         active[column] = true;
      }

   while (true) {
      int target = 0;
      bool skipped = true;
      for (int column = 0; column <= number_vertex - 1; column++)
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
      if (skipped)
         break;

      printf("vertex:", ' ', target, '\n');
      for (int row = 0; row <= number_vertex - 1; row++)
         graph[row][target] = false;
      active[target] = false;
   }
}

void feed_vertex(char* left, int length, bool** graph)
{
   int count = 0;
   char* left = source;
   char* right = source;
   while ((*right != '\n') && (*right != ' ')) {
      right += 1;
      count += 1;
   }
   int numeral_main = strtol(left, NULL, right - left);
   while (count != length) {
      if (*right == '\n') {
         int numeral_another = strtol(left, NULL, right - left);
         graph[numeral_main][numeral_another] = true;
         left = right + 1;
         while (!isalnum(*left))
            left += 1;
         right = left;
         continue;
      }
      right += 1;
      count += 1;
   }
   return graph;
}

void construct_graph(int length, char* source, bool** graph)
{
   int count = 0;
   char* left = source;
   char* right = source;
   while (count != length) {
      if (*right == '\n') {
         feed_vertex(left, right - left, graph);
         left = right + 1;
         while (!isalnum(*left))
            left += 1;
         right = left;
         continue;
      }
      right += 1;
      count += 1;
   }
}

int find_maximum_numeral(int length, char* source)
{
   int maximum = 0;
   int count = 0;
   char* left = source;
   char* right = source;
   while (count != length) {
      if (!isalnum(*right)) {
         int hold = strtol(left, NULL, right - left);
         if (hold > maximum)
            maximum = hold;
         left = right + 1;
         while (!isalnum(*left))
            left += 1;
         right = left;
         continue;
      }
      right += 1;
      count += 1;
   }
   return maximum;
}

int find_size(char* source)
{
   int count = 0;
   char* left = source;
   while ((*right != NULL) && (right - left < LIMIT_SIZE_FILE)) {
      right += 1;
      count += 1;
   }
   return count;
}
