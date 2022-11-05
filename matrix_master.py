import copy


def show_matrix(matrix, title=None):
    print(f"{title.upper() if title else 'МАТРИЦА'} :")
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            print('{0:8.2f}'.format(matrix[i][j]), end=" ")
        print()
    print()


def cut_matrix(matrix, row_ind, column_ind):
    new_matrix = copy.deepcopy(matrix)
    del (new_matrix[row_ind])
    for i in range(len(new_matrix)):
        del (new_matrix[i][column_ind])
    return new_matrix


def get_max_elem_in_matrix_row(matrix, row_ind, extract_indexes=None):
    matrix = copy.deepcopy(matrix)
    collection: list = matrix[row_ind]
    if extract_indexes is not None:
        for ind in extract_indexes:
            collection.pop(ind)
    return max(collection)


def get_min_elem_in_matrix_row(matrix, row_ind, extract_indexes=None):
    matrix = copy.deepcopy(matrix)
    collection: list = matrix[row_ind]
    if extract_indexes is not None:
        for ind in extract_indexes:
            collection.pop(ind)
    return min(collection)


def get_min_elem_in_matrix_column(matrix, column_ind, extract_indexes=None):
    matrix = copy.deepcopy(matrix)
    collection: list = [matrix[0][column_ind]]
    for i in range(1, len(matrix)):
        collection.append(matrix[i][column_ind])
    if extract_indexes is not None:
        for ind in extract_indexes:
            collection.pop(ind)
    return min(collection)


def get_max_elem_in_matrix_column(matrix, column_ind, extract_indexes=None):
        matrix = copy.deepcopy(matrix)
        collection: list = [matrix[0][column_ind]]
        for i in range(1, len(matrix)):
            collection.append(matrix[i][column_ind])
        if extract_indexes is not None:
            for ind in extract_indexes:
                collection.pop(ind)
        return max(collection)