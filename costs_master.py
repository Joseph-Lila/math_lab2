from prettytable import PrettyTable


def show_costs_via_table(costs, title=None):
    table = PrettyTable()
    table.title = title.upper() if title else "ТАБЛИЦА КОЭФФИЦИЕНТОВ"
    rows = sorted(get_row_indexes(costs))
    columns = sorted(get_column_indexes(costs))
    rows_for_table = [[column] + [costs[(row, column)] for row in rows] for column in columns]
    table.field_names = [" "] + rows
    table.add_rows(rows_for_table)
    print(table)


def sub_for_row(costs, row_ind, value):
    for i, j in costs:
        if i == row_ind:
            costs[(i, j)] -= value


def sub_for_column(costs, column_ind, value):
    for i, j in costs:
        if j == column_ind:
            costs[(i, j)] -= value


def sub_all_rows_by_their_min(costs):
    rows = get_row_indexes(costs)
    min_elements = []
    for row in rows:
        min_elem = get_min_elem_in_matrix_row(costs, row)
        sub_for_row(costs, row, min_elem)
        min_elements.append(min_elem)
    return min_elements


def sub_all_columns_by_their_min(costs):
    columns = get_column_indexes(costs)
    min_elements = []
    for column in columns:
        min_elem = get_min_elem_in_matrix_column(costs, column)
        sub_for_column(costs, column, min_elem)
        min_elements.append(min_elem)
    return min_elements


def get_row_indexes(costs):
    indexes = []
    for i, j in sorted(costs):
        if i not in indexes:
            indexes.append(i)
    return indexes


def get_column_indexes(costs):
    indexes = []
    for i, j in sorted(costs):
        if j not in indexes:
            indexes.append(j)
    return indexes


def cut_matrix(costs, row_ind, column_ind):
    keys_to_pop = []
    for i, j in costs:
        if i == row_ind or j == column_ind:
            keys_to_pop.append((i, j))
    for key in keys_to_pop:
        costs.pop(key)
    return costs


def get_max_elem_in_matrix_row(costs, row_ind, extract_indexes=None):
    collection: list = [costs[(i, j)] for i, j in costs if i == row_ind]
    if extract_indexes is not None:
        for ind in extract_indexes:
            collection.pop(ind)
    return max(collection)


def get_min_elem_in_matrix_row(costs, row_ind, extract_indexes=None):
    collection: list = [costs[(i, j)] for i, j in costs if i == row_ind] \
        if extract_indexes is None \
        else [costs[(i, j)] for i, j in costs if i == row_ind and j not in extract_indexes]
    return min(collection)


def get_min_elem_in_matrix_column(costs, column_ind, extract_indexes=None):
    collection: list = [costs[(i, j)] for i, j in costs if j == column_ind] \
        if extract_indexes is None \
        else [costs[(i, j)] for i, j in costs if j == column_ind and i not in extract_indexes]
    return min(collection)


def get_max_elem_in_matrix_column(costs, column_ind, extract_indexes=None):
    collection: list = [costs[(i, j)] for i, j in costs if j == column_ind]
    if extract_indexes is not None:
        for ind in extract_indexes:
            collection.pop(ind)
    return max(collection)
