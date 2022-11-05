import copy
import math

from prettytable import PrettyTable

from city_tree import CityTree, print_city_tree
from custom_calculator import (calculate_negative_low_border,
                               calculate_positive_low_border)
from matrix_master import (cut_matrix, get_max_elem_in_matrix_column,
                           get_max_elem_in_matrix_row,
                           get_min_elem_in_matrix_column,
                           get_min_elem_in_matrix_row, show_matrix)
from pretty_print import out_blue, out_red


class BranchAndBoundMethod:
    def __init__(self, costs: dict):
        self.__tree = CityTree(city_number='ROOT')
        self.__cur_node = self.__tree
        self.__costs = costs
        self.__n = int(math.sqrt(len(self.__costs)))
        self.__q = float('inf')
        self.__cities = [chr(i) for i in range(ord('A'), ord('A') + self.__n)]
        self.__matrix = [
            [float('inf') for j in range(self.__n)]
            for i in range(self.__n)
        ]
        self.__init_matrix()
        out_red("РАЗ. ДВА. ТРИ. ВПЕРЕД!")

    @property
    def costs(self) -> dict:
        return self.__costs

    def processing(self):
        step_cnt = 1
        self.main_step(step_cnt)
        while len(self.__cur_node.left.resolved_matrix) != 2:
            step_cnt += 1
            self.__cur_node = self.__cur_node.left \
                if self.__cur_node.left.total_cost < self.__cur_node.right.total_cost else self.__cur_node.right
            self.main_step(step_cnt)

    def main_step(self, step_cnt):
        out_red(" " * 5 + "*" * 3 + " " * 3 + f"Выполнение шага {step_cnt}" + " " * 3 + "*" * 3)
        # if cur_node is an uninitiated root
        if self.__cur_node.resolved_matrix is None:
            self.__cur_node.total_cost, self.__cur_node.resolved_matrix = self.__resolve_matrix(self.__matrix)
        new_matrix, popped_i, popped_j, sum_popped_city = self.__visit_city(self.__cur_node.resolved_matrix)
        low_border, resolved_matrix = self.__resolve_matrix(new_matrix)
        self.__extend_cur_node(low_border, resolved_matrix, popped_i, popped_j, sum_popped_city)
        print_city_tree(self.__tree)

    def __resolve_matrix(self, matrix):
        low_border, rows_constants, columns_constants, resolved_matrix = self.__define_low_border(matrix)
        out_blue(f"Оценка НГЦФ = {low_border}")
        out_blue(f"Константы приведения строк: {rows_constants}")
        out_blue(f"Константы приведения столбцев: {columns_constants}")
        show_matrix(resolved_matrix, "приведенная матрица")
        return low_border, resolved_matrix

    def __visit_city(self, resolved_matrix):
        popped_i, popped_j, sum_popped_city = self.make_s_table(resolved_matrix)
        out_blue(f"Запрещаем последующий выбор ({popped_i};{popped_j}).")
        self.__matrix[popped_i - 1][popped_j - 1] = float('inf')
        show_matrix(self.__matrix, "измененная матрица")
        new_matrix = cut_matrix(resolved_matrix, popped_i - 1, popped_j - 1)
        show_matrix(new_matrix, "обрезанная матрица")
        return new_matrix, popped_i, popped_j, sum_popped_city

    def __extend_cur_node(self, low_border, resolved_matrix, popped_i, popped_j, sum_popped_city):
        negative_low_border = calculate_negative_low_border(self.__cur_node.total_cost, sum_popped_city)
        positive_low_border = calculate_positive_low_border(self.__cur_node.total_cost, low_border)
        if negative_low_border <= positive_low_border:
            self.__cur_node.right = CityTree(
                city_number=f"!{popped_i},{popped_j}",
                total_cost=negative_low_border,
                resolved_matrix=resolved_matrix,
                parent=self.__cur_node
            )
            self.__cur_node.left = CityTree(
                city_number=f"{popped_i},{popped_j}",
                total_cost=positive_low_border,
                resolved_matrix=resolved_matrix,
                parent=self.__cur_node
            )
        else:
            self.__cur_node.left = CityTree(
                city_number=f"!{popped_i},{popped_j}",
                total_cost=negative_low_border,
                resolved_matrix=resolved_matrix,
                parent=self.__cur_node
            )
            self.__cur_node.right = CityTree(
                city_number=f"{popped_i},{popped_j}",
                total_cost=positive_low_border,
                resolved_matrix=resolved_matrix,
                parent=self.__cur_node
            )
        out_blue(f"НГЦФ для негативного узла: {negative_low_border}")
        out_blue(f"НГЦФ для позитивного узла: {positive_low_border}")

    @staticmethod
    def __define_low_border(matrix):
        resolved_matrix = copy.deepcopy(matrix)
        rows_constants = []
        columns_constants = []
        # resolve rows
        for i in range(len(resolved_matrix)):
            min_value = get_min_elem_in_matrix_row(resolved_matrix, i)
            rows_constants.append(min_value)
            for j in range(len(resolved_matrix[i])):
                resolved_matrix[i][j] -= min_value
        # resolve columns
        j = 0
        while j < len(resolved_matrix[0]):
            min_value = get_min_elem_in_matrix_column(resolved_matrix, j)
            columns_constants.append(min_value)
            for i in range(len(resolved_matrix)):
                resolved_matrix[i][j] -= min_value
            j += 1
        return sum(rows_constants) + sum(columns_constants), rows_constants, columns_constants, resolved_matrix

    @staticmethod
    def make_s_table(matrix, title=None):
        zeros = [(i + 1, j + 1) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j] == 0]
        table = PrettyTable()
        table.title = title if title else "S-таблица"
        table.field_names = ["Для S={(i,j)}"] + [str(pair) for pair in zeros]
        di = [get_min_elem_in_matrix_row(matrix, i - 1, [j - 1]) for i, j in zeros]
        dj = [get_min_elem_in_matrix_column(matrix, j - 1, [i - 1]) for i, j in zeros]
        Eij = [di[i] + dj[i] for i in range(len(zeros))]
        argmax = max(Eij)
        argmax_eij = ['' if elem != argmax else argmax for elem in Eij]
        table.add_rows(
            [
                ["di"] + di,
                ["dj"] + dj,
                ["Eij"] + Eij,
                ["argmax Eij"] + argmax_eij,
            ]
        )
        print(table)
        max_ind = Eij.index(argmax)
        popped_i, popped_j = zeros[max_ind]
        return popped_i, popped_j, argmax

    def __init_matrix(self):
        for cost in self.__costs:
            self.__matrix[cost[0] - 1][cost[1] - 1] = self.costs[cost]
