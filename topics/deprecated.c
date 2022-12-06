#include <stdio.h>
#include <string.h>
#define LIMIT_FILE 1024



struct Node
{
   void *item;
   Node* last;
   Node* next;
};

static GenListNode* genLisNewNode(void* data, unsigned int dataSize)
{
    GenListNode* node = NULL;
    if (!data) {
        return NULL;
    }
    node = malloc(sizeof(*node));
    if (!node) {
        return NULL;
    }
    memset(node, 0, sizeof(*node));
    node->data = malloc(dataSize);
    if (!node->data) {
        return NULL;
    }
    memcpy(node->data, data, dataSize);
    return node;
}

void destroy_node(Node* node)
{
   if (!node)
      return;
   if (!(node->last))
      node->last->next = node->next;
   if (!(node->next))
      node->next->last = node->last;
   free(node->last);
   free(node->last);
   free(node);
   return GEN_LIST_NO_ERR;
}

void destroy_node_middle(Node* node) {
   if (!(node->last))
      node->last->next = node->next;
   node->next->last = node->last;
   free(node);
}

void destroy_node_start(Node* node)
{
   if (!node)
      return;
}

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

int convert_number(char* text) {
   return strtol(text, NULL, 10);
}

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
   char source[LIMIT_FILE];
   FILE* document = fopen(argv[0], "r");
   fgets(source, LIMIT_FILE, document);
   fclose(document);

   int** graph = malloc();
   char* slice;
   slice = strtok(source,"\n");
   while (slice != NULL)
   {
      char* vertex = strtok(slice,"\n");
      strcpy(vertex_head, vertex);
      while (vertex != NULL)
      {
         construct_edge(graph, vertex, vertex_head);
         vertex = strtok(NULL, "\n");
      }
      construct(graph, slice);
      slice = strtok(NULL, "\n");
   }

   return 0;
}