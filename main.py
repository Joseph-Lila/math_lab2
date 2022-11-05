from branch_and_bound_method import BranchAndBoundMethod


def main():
    """
    The main function.
    """
    costs = {
        (1, 1): float('inf'),
        (1, 2): 48,
        (1, 3): 27,
        (1, 4): 31,
        (1, 5): 43,
        (2, 1): 33,
        (2, 2): float('inf'),
        (2, 3): 28,
        (2, 4): 44,
        (2, 5): 43,
        (3, 1): 41,
        (3, 2): 28,
        (3, 3): float('inf'),
        (3, 4): 40,
        (3, 5): 36,
        (4, 1): 37,
        (4, 2): 35,
        (4, 3): 29,
        (4, 4): float('inf'),
        (4, 5): 46,
        (5, 1): 48,
        (5, 2): 48,
        (5, 3): 25,
        (5, 4): 29,
        (5, 5): float('inf'),
    }
    method = BranchAndBoundMethod(costs=costs)
    method.processing()


if __name__ == '__main__':
    main()
