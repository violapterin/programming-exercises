#include <stdio.h> // fgets, printf
#include <stdlib.h> // strtol
#include <ctype.h> // isalnum
#include <stdbool.h> // bool
#include <string.h> // strlen
#define LIMIT_LENGTH_LINE 512
#define USUAL_TERMINAL 0
#define USUAL_FILE 1
#define VERBOSE_TERMINAL 2
#define VERBOSE_FILE 3
#define SUCCINT_TERMINAL 4
#define SUCCINT_FILE 5

void sort_topological(int, int, int*, int**, FILE*, bool**);
void construct_vertex(char* , bool**);
int find_maximum_numeral(char*);
void print_graph(int, bool**); // debug

// argv[0]: program name
// argv[1]: flag
// argv[2]: input filename
// argv[3]: output filename
int main(int argc, char** argv)
{
   char* string_program = argv[0];
   char* string_flag = argv[1];
   char* filename_input = argv[2];
   char* filename_output = argv[3];

   FILE* stream_input = fopen(filename_input, "r");
   if (stream_input == NULL) {
      printf("Error opening file!\n");
      exit(1);
   }
   char content[LIMIT_LENGTH_LINE];
   int maximum = 0;
   while (fgets(content, LIMIT_LENGTH_LINE, stream_input) != NULL) {
      int hold = find_maximum_numeral(content);
      if (hold > maximum) {
         maximum = hold;
      }
   }
   fclose(stream_input);

   bool* graph[maximum];
   for (int row = 0; row <= maximum - 1; row++) {
      graph[row] = (bool*) malloc(maximum * sizeof(bool));
   }
   for (int row = 0; row <= maximum - 1; row++) {
      for (int column = 0; column <= maximum - 1; column++) {
         graph[row][column] = false;
      }
   }

   stream_input = fopen(filename_input, "r");
   if (stream_input == NULL) {
      printf("Error opening file!\n");
      exit(1);
   }
   while (fgets(content, LIMIT_LENGTH_LINE, stream_input) != NULL) {
      construct_vertex(content, graph);
   }
   fclose(stream_input);

   // print_graph(maximum, graph); // XXX
   int complexity_vertex[maximum];
   int* complexity_edge[maximum];
   for (int row = 0; row <= maximum - 1; row++) {
      complexity_vertex[row] = 0;
   }
   for (int row = 0; row <= maximum - 1; row++) {
      complexity_edge[row] = (int*) malloc(maximum * sizeof(int));
   }
   for (int row = 0; row <= maximum - 1; row++) {
      for (int column = 0; column <= maximum - 1; column++) {
         complexity_edge[row][column] = 0;
      }
   }
   int flag = strtol(string_flag, NULL, 0);
   FILE* stream_output = fopen(filename_output, "w");
   if (stream_output == NULL) {
      printf("Error opening file!\n");
      exit(1);
   }
   sort_topological(
      flag, maximum,
      complexity_vertex, complexity_edge,
      stream_output, graph
   );
   fclose(stream_output);
}

void sort_topological(
   int flag, int maximum,
   int* complexity_vertex, int** complexity_edge,
   FILE* stream_output, bool** graph
)
{
   bool active[maximum];
   for (int row = 0; row <= maximum - 1; row++) {
      active[row] = false;
   }
   for (int row = 0; row <= maximum - 1; row++) {
      for (int column = 0; column <= maximum - 1; column++) {
         if (graph[row][column]) {
            active[row] = true;
            active[column] = true;
         }
      }
   }

   while (true) {
      int trivial = true;
      for (int column = 0; column <= maximum - 1; column++) {
         if (active[column]) {
            trivial = false;
            break;
         }
         complexity_vertex[column] += 1;
      }
      if (trivial) {
         break;
      }

      int target = -1;
      for (int column = 0; column <= maximum - 1; column++) {
         if (!active[column]) {
            continue;
         }
         bool with_arrival = false;
         for (int row = 0; row <= maximum - 1; row++) {
            if (graph[row][column]) {
               with_arrival = true;
               complexity_edge[row][column] += 1; // complexity
               break;
            }
            complexity_vertex[row] += 1; // complexity
         }
         if (!with_arrival) {
            target = column;
         }
         complexity_vertex[column] += 1; // complexity
      }

      bool whether_terminal = (
         (flag == USUAL_TERMINAL)
         || (flag == VERBOSE_TERMINAL)
         || (flag == SUCCINT_TERMINAL)
      );
      bool whether_file = (
         (flag == USUAL_FILE)
         || (flag == VERBOSE_FILE)
         || (flag == SUCCINT_FILE)
      );
      if (target != -1) {
         if (whether_terminal) {
            printf("sorted vertex: %d\n", target + 1); // one based
         }
         if (whether_file) {
            fprintf(stream_output, "sorted vertex: %d\n", target + 1); // one based
         }
         for (int column = 0; column <= maximum - 1; column++) {
            graph[target][column] = false;
            complexity_vertex[column] += 1; // complexity
         }
         active[target] = false;
      }
      else {
         if (whether_terminal) {
            printf("cycle!\n");
         }
         if (whether_file) {
            fprintf(stream_output, "cycle!\n");
         }
         break;
      }
   }

   for (int row = 0; row <= maximum - 1; row++) {
      if (complexity_vertex[row] == 0) {
         continue;
      }
      if ((flag == VERBOSE_TERMINAL) || (flag == SUCCINT_TERMINAL)) {
         printf(
            "instructions for vertex %d: %d\n",
            row, complexity_vertex[row]
         );
      }
      else if ((flag == VERBOSE_FILE) || (flag == SUCCINT_FILE)) {
         fprintf(
            stream_output,
            "instructions for vertex %d: %d\n",
            row, complexity_vertex[row]
         );
      }
   }

   for (int row = 0; row <= maximum - 1; row++) {
      for (int column = 0; column <= maximum - 1; column++) {
         if (complexity_edge[row][column] == 0) {
            continue;
         }
         if ((flag == VERBOSE_TERMINAL) || (flag == SUCCINT_TERMINAL)) {
            printf(
               "instructions for edge (%d, %d): %d\n",
               row, column, complexity_edge[row][column]
            );
         }
         else if ((flag == VERBOSE_FILE) || (flag == SUCCINT_FILE)) {
            fprintf(
               stream_output,
               "instructions for edge (%d, %d): %d\n",
               row, column, complexity_edge[row][column]
            );
         }
      }
   }

   int total_vertex = 0;
   int total_edge = 0;
   int total = 0;
   for (int row = 0; row <= maximum - 1; row++) {
      total_vertex += complexity_vertex[row];
   }
   for (int row = 0; row <= maximum - 1; row++) {
      for (int column = 0; column <= maximum - 1; column++) {
         total_edge += complexity_edge[row][column];
      }
   }
   total = total_edge + total_vertex;
   if ((flag == VERBOSE_TERMINAL) || (flag == SUCCINT_TERMINAL)) {
      printf("total instructions on vertices: %d\n", total_vertex);
      printf("total instructions on edges: %d\n", total_edge);
      printf("total instructions: %d\n", total);
   }
   else if ((flag == VERBOSE_FILE) || (flag == SUCCINT_FILE)) {
      fprintf(stream_output, "total instructions on vertices: %d\n", total_vertex);
      fprintf(stream_output, "total instructions on edges: %d\n", total_edge);
      fprintf(stream_output, "total instructions: %d\n", total);
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
   left = right + 1;
   count += 1;
   while (count <= length - 1) {
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
   while (count <= length - 1) {
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
      if (hold > maximum) {
         maximum = hold;
      }
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
         if (graph[row][column]) {
            printf("1");
         }
         else {
            printf("0");
         }
         printf(" ");
      }
      printf("\n");
   }
}
