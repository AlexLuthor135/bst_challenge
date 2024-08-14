#!/bin/bash

C_PROGRAM="./src/build_tree.c"
C_CHALLENGE="build_tree_challenge.c"
EXECUTABLE="./src/build_tree"
PYTHON_SCRIPT="./src/verify_bst.py"

gcc -Wall -Wextra -Werror -o $EXECUTABLE $C_PROGRAM $C_CHALLENGE

if [ $? -eq 0 ]; then
    echo "Compilation successful."

    python3 ./$PYTHON_SCRIPT
else
    echo "Compilation failed."
fi
