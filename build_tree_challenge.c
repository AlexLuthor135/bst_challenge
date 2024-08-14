#include "./src/bst.h"

t_tree* newNode(int value)
{
    t_tree* node = (t_tree*)malloc(sizeof(t_tree));
    node->val = value;
    node->left = node->right = NULL;
    return (node);
}

void build_branches(t_tree *root, int value)
{
    t_tree *prev;
    while (root)
    {
        prev = root;
        if (value < root->val)
            root = root->left;
        else
            root = root->right;
    }
    if (value < prev->val)
        prev->left = newNode(value);
    else
        prev->right = newNode(value);
}

void build_tree(t_tree **root, char **argv)
{
    int i = 1;
    while (argv[i])
    {
        if ((*root) == NULL)
            (*root) = newNode(atoi(argv[i]));
        else
            build_branches(*root, atoi(argv[i]));
        i++;
    }
}