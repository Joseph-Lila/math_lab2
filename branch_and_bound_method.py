import copy
import math

from prettytable import PrettyTable

from city_tree import CityTree, print_city_tree
from custom_calculator import (calculate_negative_low_border,
                               calculate_positive_low_border)
from costs_master import (cut_matrix, get_max_elem_in_matrix_column,
                          get_max_elem_in_matrix_row,
                          get_min_elem_in_matrix_column,
                          get_min_elem_in_matrix_row, show_costs_via_table, sub_all_rows_by_their_min,
                          sub_all_columns_by_their_min)
from pretty_print import out_blue, out_red, out_purple


class BranchAndBoundMethod:
    def __init__(self, costs: dict):
        self.__tree = CityTree(city_number='ROOT')
        self.__cur_node = self.__tree
        self.__costs = costs
        self.__trip = []
        self.__n = int(math.sqrt(len(self.__costs)))
        self.__q = float('inf')
        out_red("РАЗ. ДВА. ТРИ. ВПЕРЕД!")

    @property
    def costs(self) -> dict:
        return self.__costs

    def processing(self):
        step_cnt = 1
        self.main_step(step_cnt)
        while math.sqrt(len(self.__cur_node.resolved_costs)) != 2 \
                and math.sqrt(len(self.__cur_node.resolved_costs)) != 2 \
                and (self.__cur_node.total_cost < self.__q or self.__cur_node.total_cost < self.__q):
            step_cnt += 1
            self.main_step(step_cnt)
        if self.__q <= self.__cur_node.total_cost or self.__q <= self.__cur_node.total_cost:
            out_purple("Торговец-бродяга ушел в бесконечность!!!")
        else:
            self.chose_needed_costs()
            self.__q = self.__cur_node.total_cost

    def main_step(self, step_cnt):
        out_red(" " * 5 + "*" * 3 + " " * 3 + f"Выполнение шага {step_cnt}" + " " * 3 + "*" * 3)
        # if cur_node is an uninitiated root
        if self.__cur_node.resolved_costs is None:
            self.__cur_node.total_cost, self.__cur_node.resolved_costs = self.__resolve_costs()
        new_costs, popped_i, popped_j, sum_popped_city = self.__visit_city(self.__cur_node.resolved_costs)
        low_border, resolved_costs = self.__resolve_costs(costs=new_costs)
        self.__extend_cur_node(low_border, resolved_costs, popped_i, popped_j, sum_popped_city)
        print_city_tree(self.__tree)

    def chose_needed_costs(self):
        out_red(" " * 5 + "*" * 3 + " " * 3 + f"Матрица имеет размерность 2х2" + " " * 3 + "*" * 3)
        my_trip = sorted(self.__trip)
        remainder = self.__cur_node.resolved_costs
        elements_to_del = []
        for key, value in remainder.items():
            if value == float('inf'):
                elements_to_del.append(key)
        for elem in elements_to_del:
            remainder.pop(elem)
        found = False
        for elem_i, elem_j in remainder.keys():
            if found:
                break
            for another_elem_i, another_elem_j in remainder.keys():
                if (elem_i, elem_j) != (another_elem_i, another_elem_j):
                    if elem_i == another_elem_j or elem_j == another_elem_i:
                        self.__short_extension_for_current_node(
                            remainder[(elem_i, elem_j)],
                            {(another_elem_i, another_elem_j): remainder[(another_elem_i, another_elem_j)]},
                            elem_i, elem_j)
                        self.__short_extension_for_current_node(
                            remainder[(another_elem_i, another_elem_j)],
                            {(elem_i, elem_j): remainder[(elem_i, elem_j)]},
                            another_elem_i, another_elem_j)
                        found = True
                        break

    def __short_extension_for_current_node(self, low_border, resolved_costs, popped_i, popped_j):
        self.__cur_node.right = CityTree(
            city_number=f"{popped_i},{popped_j}",
            total_cost=self.__cur_node.total_cost + low_border,
            resolved_costs=copy.deepcopy(resolved_costs),
            parent=self.__cur_node
        )
        self.__cur_node = self.__cur_node.right
        self.__trip.insert(0, (popped_i, popped_j))
        out_red(f"Тур для торговца-бродяги: {self.__trip}")
        print_city_tree(self.__tree)

    def __resolve_costs(self, costs=None):
        low_border, rows_constants, columns_constants = self.__define_low_border(costs=costs)
        out_blue(f"Оценка НГЦФ = {low_border}")
        out_blue(f"Константы приведения строк: {rows_constants}")
        out_blue(f"Константы приведения столбцев: {columns_constants}")
        show_costs_via_table(self.__costs if costs is None else costs, "приведенная матрица")
        return low_border, copy.deepcopy(self.__costs if costs is None else costs)

    def __visit_city(self, costs):
        popped_i, popped_j, sum_popped_city = self.make_s_table(costs)
        out_blue(f"Запрещаем последующий выбор ({popped_i};{popped_j}).")
        new_costs = cut_matrix(costs, popped_i, popped_j)
        if (popped_j, popped_i) in new_costs:
            new_costs[(popped_j, popped_i)] = float('inf')
        show_costs_via_table(new_costs, "новая матрица")
        return new_costs, popped_i, popped_j, sum_popped_city

    def __extend_cur_node(self, low_border, resolved_costs, popped_i, popped_j, sum_popped_city):
        negative_low_border = calculate_negative_low_border(self.__cur_node.total_cost, sum_popped_city)
        positive_low_border = calculate_positive_low_border(self.__cur_node.total_cost, low_border)
        if negative_low_border < positive_low_border:
            self.__cur_node.right = CityTree(
                city_number=f"!{popped_i},{popped_j}",
                total_cost=negative_low_border,
                resolved_costs=copy.deepcopy(resolved_costs),
                parent=self.__cur_node
            )
            self.__cur_node.left = CityTree(
                city_number=f"{popped_i},{popped_j}",
                total_cost=positive_low_border,
                resolved_costs=copy.deepcopy(resolved_costs),
                parent=self.__cur_node
            )
            self.__trip.insert(0, (-popped_i, -popped_j))
        else:
            self.__cur_node.left = CityTree(
                city_number=f"!{popped_i},{popped_j}",
                total_cost=negative_low_border,
                resolved_costs=copy.deepcopy(resolved_costs),
                parent=self.__cur_node
            )
            self.__cur_node.right = CityTree(
                city_number=f"{popped_i},{popped_j}",
                total_cost=positive_low_border,
                resolved_costs=copy.deepcopy(resolved_costs),
                parent=self.__cur_node
            )
            self.__trip.insert(0, (popped_i, popped_j))
        self.__cur_node = self.__cur_node.right
        out_blue(f"НГЦФ для негативного узла: {negative_low_border}")
        out_blue(f"НГЦФ для позитивного узла: {positive_low_border}")
        out_red(f"Тур для торговца-бродяги: {self.__trip}")

    def __define_low_border(self, costs=None):
        rows_constants = sub_all_rows_by_their_min(self.__costs if costs is None else costs)
        columns_constants = sub_all_columns_by_their_min(self.__costs if costs is None else costs)
        return sum(rows_constants) + sum(columns_constants), rows_constants, columns_constants

    @staticmethod
    def make_s_table(costs, title=None):
        zeros = [key for key, value in costs.items() if value == 0]
        table = PrettyTable()
        table.title = title if title else "S-таблица"
        table.field_names = ["Для S={(i,j)}"] + [str(pair) for pair in zeros]
        di = [get_min_elem_in_matrix_row(costs, i, [j]) for i, j in zeros]
        dj = [get_min_elem_in_matrix_column(costs, j, [i]) for i, j in zeros]
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
