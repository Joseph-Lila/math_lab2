class CityTree:
    def __init__(self, city_number=None, parent=None, total_cost=None, resolved_matrix=None):
        self.left = None
        self.right = None
        self.parent = parent
        self.city_number = city_number
        self.total_cost = total_cost
        self.resolved_matrix = resolved_matrix


class Trunk:
    def __init__(self, prev=None, str=None):
        self.prev = prev
        self.str = str


def show_trunks(p):
    if p is None:
        return
    show_trunks(p.prev)
    print(p.str, end='')


def print_city_tree(root, prev=None, is_left=False):
    if root is None:
        return

    prev_str = '     '
    trunk = Trunk(prev, prev_str)
    print_city_tree(root.right, trunk, True)

    if prev is None:
        trunk.str = '-----'
    elif is_left:
        trunk.str = '.----'
        prev_str = '    |'
    else:
        trunk.str = '`----'
        prev.str = prev_str

    show_trunks(trunk)
    print(' ' + f"< {root.city_number:>4} ({root.total_cost:>3}) >")
    if prev:
        prev.str = prev_str
    trunk.str = '    |'
    print_city_tree(root.left, trunk, False)
