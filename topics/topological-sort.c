#include <stdio.h>
#include <string.h>
#define LIMIT_SIZE_FILE 4096
#define FLAG_USUAL 0
#define FLAG_COMPLEXITY 1


struct Node_text {
   char* text;
   Node_text* next;
};

struct Node_vertex {
   Vertex* vertex;
   Node_text* next;
};

struct Vertex {
   int count;
   Node_vertex* head_vertex_in;
   Node_vertex* head_vertex_out;
};

struct Fact_vertex {
   char* name_head;
   Node_text* head_name_other;
};


void draw_vertex(Fact_vertex* fact, Node_vertex* graph) {
   
}

Node_text* chop_text(char* delimiter, char* slice) {
   char* pch = strchr(str,'.');
   while (pch!=NULL) {
      pch=strchr(pch+1,'.');
   }
}

int main(int argc, char **argv)
{
   char source[LIMIT_SIZE_FILE];
   FILE* document = fopen(argv[0], "r");
   fgets(source, LIMIT_SIZE_FILE, document);
   fclose(document);
   int size_file = find_length_text(source);
   int number_vertex = find_maximum_numeral(size_file, source);

   bool graph[number_vertex][number_vertex];
   for (int row = 0; row <= number_vertex - 1; row++)
      for (int column = 0; column <= number_vertex - 1; column++)
         graph[row][column] = false;
   construct_graph(source, size_file, graph);

   sort_topological(flag, number_vertex, graph);
}

void construct_graph(char* source, int size, bool** graph) {
   int count = 0;
   char* left = source;
   char* right = source;
   while (count != size)
   {
      if (*right == '\n')
      {
         feed_vertex(left, right - left, graph);
         left = right + 1;
         right = left;
         continue;
      }
      right += 1;
      count += 1;
   }
}

void feed_vertex(char* left, int size, bool** graph) {
   int count = 0;
   char* left = source;
   char* right = source;
   while (*right != '\n')
   {
      right += 1;
      count += 1;
   }
   int numeral_main = strtol(left, NULL, right - left);
   while (count != size)
   {
      if(*right == '\n')
      {
         int numeral_another = strtol(left, NULL, right - left);
         graph[numeral_main][numeral_another] = true;
         left = right + 1;
         right = left;
         continue;
      }
      right += 1;
      count += 1;
   }
   return graph;
}

void sort_topological(int flag, int number_vertex, bool** graph) {
   bool active[number_vertex];
   for (int row = 0; row <= number_vertex - 1; row++)
      active[row] = false;
   for (int row = 0; row <= number_vertex - 1; row++)
      for (int column = 0; column <= number_vertex - 1; column++)
         active[row] = true;
         active[column] = true;

   while (true) {
      int target = 0;
      bool skipped = true;
      for (int column = 0; column <= number_vertex - 1; column++)
         if (!active[column])
            continue;
         skipped = false;
         bool with_arrival = false;
         for (int row = 0; row <= number_vertex - 1; row++)
            if (graph[row][column])
            {
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