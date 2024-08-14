import subprocess, random, time, sys
import matplotlib.pyplot as plt
import networkx as nx

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def print_colored(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

def deserialize(data):
    try:
        def helper(values):
            if not values:
                return None
            if values[0] == 'null':
                values.pop(0)
                return None
            node = TreeNode(int(values.pop(0)))
            node.left = helper(values)
            node.right = helper(values)
            return node
        values = data.split()
        return helper(values)
    except Exception as e:
        print_colored(f"Error deserializing data: {e}", "red")
        sys.exit(1)

def is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):
    if not root:
        return True
    if root.val <= min_val or root.val >= max_val:
        return False
    return is_valid_bst(root.left, min_val, root.val) and is_valid_bst(root.right, root.val, max_val)

def in_order_traversal(root, result=None):
    if result is None:
        result = []
    if root:
        in_order_traversal(root.left, result)
        result.append(root.val)
        in_order_traversal(root.right, result)
    return result

def add_edges(graph, root, pos=None, x=0, y=0, layer=1):
    if pos is None:
        pos = {}
    if root:
        pos[root.val] = (x, y)
        if root.left:
            graph.add_edge(root.val, root.left.val)
            l = x - 1 / (2**layer)
            pos = add_edges(graph, root.left, pos=pos, x=l, y=y-1, layer=layer+1)
        if root.right:
            graph.add_edge(root.val, root.right.val)
            r = x + 1 / (2**layer)
            pos = add_edges(graph, root.right, pos=pos, x=r, y=y-1, layer=layer+1)
    return pos

def draw_tree(root):
    graph = nx.DiGraph()
    pos = add_edges(graph, root)
    if not pos:
        return
    nx.draw(graph, pos, with_labels=True, arrows=False, node_size=500, node_color='skyblue', font_size=10, font_color='black', font_weight='bold', edge_color='gray')
    plt.show()

def execute_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except FileNotFoundError:
        print_colored(f"Executable file not found: {command[0]}. Please check the path and ensure the file exists.", "red")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print_colored(f"Error executing command: {e}", "red")
        sys.exit(1)
    except Exception as e:
        print_colored(f"An unexpected error occurred: {e}", "red")
        sys.exit(1)

numbers = list(range(1, 1001))
random.shuffle(numbers)
random_numbers = numbers[:100]

random_numbers_str = list(map(str, random_numbers))
command = ['./src/build_tree'] + random_numbers_str
serialized_tree = execute_command(command)

try:
    root = deserialize(serialized_tree)
    is_valid = is_valid_bst(root)
    in_order = in_order_traversal(root)
    missing_numbers = set(random_numbers) - set(in_order)
    extra_numbers = set(in_order) - set(random_numbers)
except Exception as e:
    print_colored(f"Error deserializing data: {e}", "red")
    sys.exit(1)

bonus_part = False
if not missing_numbers and not extra_numbers and is_valid:
    print_colored("The tree is a valid BST.\n", "green")
    bonus_part = True
else:
    print_colored("The tree is not a valid BST.\n", "red")

if missing_numbers:
    print_colored("Missing numbers:", "red")
    print(f"{sorted(missing_numbers)}\n")
if extra_numbers:
    print_colored("Extra numbers:", "red")
    print(f"{sorted(extra_numbers)}")

print(f"In-order traversal: {in_order}")

draw_tree(root)

preset_numbers = [
    81, 25, 39, 10, 58, 69, 24, 67, 72, 1,
    48, 99, 6, 7, 55, 47, 61, 37, 22, 64,
    4, 45, 77, 34, 27, 73, 17, 32, 65, 14,
    12, 42, 49, 94, 43, 95, 13, 9, 21, 30,
    36, 92, 63, 97, 28, 87, 26, 52, 11, 68,
    88, 78, 53, 76, 40, 23, 38, 3, 85, 86,
    96, 66, 71, 98, 5, 2, 46, 16, 41, 100,
    54, 59, 33, 82, 75, 84, 35, 15, 8, 93,
    50, 89, 29, 60, 79, 70, 62, 83, 80, 44,
    57, 91, 20, 19, 56, 74, 31, 90, 51, 18,
]


if bonus_part:
    elapsed_times = []
    print_colored("\nPreset numbers:", "yellow")
    print(f"{preset_numbers}")
    preset_numbers_str = list(map(str, preset_numbers))
    command = ['./src/build_tree'] + preset_numbers_str
    for _ in range(100):
        try:
            start_time = time.time()
            serialized_bonus_tree = execute_command(command)
            elapsed_time = time.time() - start_time
            elapsed_times.append(elapsed_time)

        except Exception as e:
            print_colored(f"Error during bonus part execution: {e}", "red")
            sys.exit(1)

    bonus_root = deserialize(serialized_bonus_tree)
    bonus_is_valid = is_valid_bst(bonus_root)
    bonus_in_order = in_order_traversal(bonus_root)
    bonus_missing_numbers = set(preset_numbers) - set(bonus_in_order)
    bonus_extra_numbers = set(bonus_in_order) - set(preset_numbers)
    if not bonus_missing_numbers and not bonus_extra_numbers and bonus_is_valid:
        print_colored("\nThe bonus tree is a valid BST.", "green")
        average_time = sum(elapsed_times) / len(elapsed_times)
        print_colored(f"Average Execution Time for preset numbers: {average_time:.6f} seconds\n", "cyan")
    else:
        print_colored("The bonus tree is not a valid BST.", "red")
