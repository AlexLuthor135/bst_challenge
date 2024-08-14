#include "bst.h"

//Prints the tree in preorder traversal format as an input for a program.
void serialize(t_tree* root)
{
    if (root == NULL)
    {
        printf("null ");
        return ;
    }
    printf("%d ", root->val);
    serialize(root->left);
    serialize(root->right);
}

int main(int argc, char **argv) {
    if (argc < 100)
        return(printf("Error\n"), 1);
    t_tree* root = NULL;
    build_tree(&root, argv);
    serialize(root);
    return (0);
}
