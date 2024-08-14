#include <stdio.h>
#include <stdlib.h>

typedef struct	s_tree {
	int	    val;
	struct	s_tree	*left;
	struct	s_tree	*right;
}t_tree;

void build_tree(t_tree **root, char **argv);
void serialize(t_tree* root);