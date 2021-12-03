import pandas as pd
import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import product
from collections import defaultdict

indexes = [i for i in range(1, 11)]
columns = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']

def get_start_df():
    """Создает доску и все координаты"""
    massive = [[0]*10]*10
    df = pd.DataFrame(massive, index=indexes, columns=columns)
    good_space = [i for i in product(indexes, columns)]
    return df, good_space

def direction(input_point, depth=1):
    """Возвращает названия столбцов и номера строк для точки в определенном радиусе"""
    row, column = input_point[0], input_point[1]
    if row == 1:
        rows_start = indexes[indexes.index(row): indexes.index(row) + depth + 1]
    if row == 10:
        rows_start = indexes[indexes.index(row) - depth: indexes.index(row) + 1]
    if 1 < row < 10:
        rows_start = indexes[indexes.index(row) - depth: indexes.index(row) + depth + 1]

    if column == 'А':
        column_plus = columns.index(column) + depth
        return rows_start, columns[columns.index(column):column_plus + 1]
    elif column == 'К':
        column_minus = columns.index(column) - depth
        return rows_start, columns[column_minus: columns.index(column) + 1]
    else:
        column_plus = columns.index(column) + depth
        column_minus = columns.index(column) - depth
        return rows_start, columns[column_minus:column_plus + 1]

def combinations(list_rows, list_columns):
    """Возвращает координаты, находящихся на переданных столбцах и строках"""
    return_list = list()
    for i in product(list_rows, list_columns):
        return_list.append(i)
    return return_list

def paint():
    """Расстановка корабля"""
    _, good_space = get_start_df()
    busy_point_all = set()
    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    points_ships = defaultdict(list)
    while len(ships) > 0:
        d_free_row = defaultdict(list)
        d_free_col = defaultdict(list)
        point = random.choice(good_space)
        len_ship = random.choice(ships)
        rows, cols = direction(point,len_ship-1)
        points = combinations(rows, cols)

        for po in points:
            if po not in busy_point_all:
                d_free_row[po[0]].append(po[1])
                d_free_col[po[1]].append(po[0])
        count = 0
        if len(d_free_row[point[0]]) >= len_ship:
            for c in d_free_row[point[0]]:
                points_ships[len_ship].append((point[0], c))
                b_rows, b_cols = direction((point[0], c), 1)
                b_points = combinations(b_rows, b_cols)
                busy_point_all.update(set(b_points))
                count += 1
                if count == len_ship:
                    ships.remove(len_ship)
                    break
        elif len(d_free_col[point[1]]) >= len_ship:
            for r in d_free_col[point[1]]:
                points_ships[len_ship].append((r, point[1]))
                b_rows, b_cols = direction((r, point[1]), 1)
                b_points = combinations(b_rows, b_cols)
                busy_point_all.update(set(b_points))
                count += 1
                if count == len_ship:
                    ships.remove(len_ship)
                    break
    return points_ships

def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs

def plot(df1, df2, comp=None):
    """Отрисовка состояния игры"""
    if comp:
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Шахматка Компьютера", "Шахматка игрока"), specs=[[{"type": "domain"}, {"type": "domain"}]])
    else:
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Шахматка 1 игрока", "Шахматка 2 игрока"), specs=[[{"type": "domain"}, {"type": "domain"}]])

    fig.add_trace(go.Table(
        header=dict(values=df1.reset_index().columns, line_color='black'),
        cells=dict(values=df1.reset_index().T, line_color='black', fill=dict(color=['white']))), row=1, col=1)
    fig.add_trace(go.Table(
        header=dict(values=df2.reset_index().columns, line_color='black'),
        cells=dict(values=df2.reset_index().T, line_color='black', fill=dict(color=['white']))), row=1, col=2)
    return fig.show()

def get_cum_points(i_point):
    """"Поиск точек для начисления коэффициентов (для игры с компьютором)"""
    rows, cols = direction(i_point)
    comb = combinations(rows, cols)
    comb.remove(i_point)
    d_shot = defaultdict(list)
    diag = list()
    for t in comb:
        num, bukv = t[0], t[1]
        if num == i_point[0]:
            d_shot[num].append(bukv)
        if bukv == i_point[1]:
            d_shot[bukv].append(num)
        else:
            diag.append((num, bukv))
    shot_point = list()
    for k, l_v in d_shot.items():
        if isinstance(k, str):
            l_1, l_2 = l_v, [k]
        elif isinstance(k, int):
            l_1, l_2 = [k], l_v,
        for i in product(l_1, l_2):
            shot_point.append(i)
    return shot_point, d_shot, diag