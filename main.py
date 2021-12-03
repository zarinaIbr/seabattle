from IPython.display import clear_output
import time
from preparation import split, paint, get_start_df, plot
from game import get_game_data_1, get_game_data_2

def main(user='user'):
    """Выберите режим игры- user or computer"""
    stop1, stop2 = False, False
    ranen1, ubit1 = [], []
    ranen2, ubit2 = [], []
    output_df_1, _ = get_start_df()
    output_df_2, _ = get_start_df()
    new_points_1, new_points_2 = dict(), dict()
    ouput_points_1 = paint()
    ouput_points_2 = paint()
    for k, v in ouput_points_1.items():
        new_points_1[k] = split(v, k)
    for k, v in ouput_points_2.items():
        new_points_2[k] = split(v, k)
    df1, df2 = output_df_1, output_df_2
    if user == 'user':
        while True:
            while stop1 is False:
                plot(df1, df2)
                user1 = str(input('Пользователь №1, Введите мишень через пробел: '))
                point1 = tuple([int(user1.split()[0]), user1.split()[1]])
                df2, ranen1, ubit1, flag1 = get_game_data_1(point1, new_points_2, output_df_2, ranen1, ubit1)
                time.sleep(1)
                clear_output(wait=True)
                if flag1:
                    break
            while stop2 is False:
                plot(df1, df2)
                user2 = str(input('Пользователь №2, Введите мишень через пробел: '))
                point2 = tuple([int(user2.split()[0]), user2.split()[1]])
                df1, ranen2, ubit2, flag2 = get_game_data_1(point2, new_points_1, output_df_1, ranen2, ubit2)
                if flag2:
                    break

            if len(set(ubit1)) == 20:
                print('Пользователь 1 выиграл')
                break
            if len(set(ubit2)) == 20:
                print('Пользователь 2 выиграл')
                break

    elif user == 'computer':
        points_const = {i: 1 for i in [x for b in ouput_points_2.values() for x in b]}
        while True:
            while stop1 is False:
                print('Компьютор выбирает мишень')
                df2, ranen1, ubit1, points_const, flag1 = get_game_data_2(new_points_2, output_df_2, ranen1, ubit1, points_const)
                if flag1:
                    break
            while stop2 is False:
                plot(df1, df2, comp=True)
                user2 = str(input('Пользователь, введите мишень через пробел: '))
                point2 = tuple([int(user2.split()[0]), user2.split()[1]])
                df1, ranen2, ubit2, flag2 = get_game_data_1(point2, new_points_1, output_df_1, ranen2, ubit2)
                time.sleep(1)
                clear_output(wait=True)
                if flag2:
                    break

            if len(set(ubit1)) == 20:
                print('Компьютор выиграл')
                break
            if len(set(ubit2)) == 20:
                print('Пользователь выиграл')
                break
