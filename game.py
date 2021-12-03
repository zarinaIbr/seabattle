from preparation import get_cum_points
import random

def get_game_data_1(input_point, new_points, df, ranen, ubit):
    """Алгоритм для игры с пользователем"""
    flag = True
    if input_point in ranen or input_point in ubit:
        print('Эта точка уже была задета')
        return df, ranen, ubit, flag

    for k, ll_v in new_points.items():
        for num, chip in enumerate(ll_v):
            for num_p, point in enumerate(chip):
                if input_point == point:
                    if len(chip) > 1:
                        s = set()
                        s.add(input_point)
                        if any(p not in ranen for p in set(chip).difference(s)):
                            df.loc[input_point[0], input_point[1]] = 'Р'
                            print('Ранен')
                            ranen.append(input_point)
                        elif all(p in ranen for p in set(chip).difference(s)) or all \
                                (p in ubit for p in set(chip).difference(s)):
                            for p in chip:
                                df.loc[p[0], p[1]] = 'У'
                                print('Убит')
                                ubit.append(p)
                        flag = False
                        break
                    elif len(chip) == 1:
                        df.loc[input_point[0], input_point[1]] = 'У'
                        print('Убит')
                        ubit.append(input_point)
                        flag = False
                        break
            if flag is False:
                break
        if flag is False:
            break
    if flag == True:
        print('Мимо')
    return df, ranen, ubit, flag

def get_game_data_2(new_points, df, ranen, ubit, const):
    """Алгоритм для игры с компьютором"""
    if const is not None:
        if all(v == 1 for v in const.values()):
            input_point = random.choice([i for i in const.keys()])
        elif 0.5 not in [v for v in const.values()]:
            input_point = random.choice([p for p, v in const.items() if v == 1])
        else:
            input_point = random.choice([p for p, v in const.items() if v == 0.5])
    flag = True
    if input_point in ranen or input_point in ubit:
        print('Эта точка уже была задета')
        return df, ranen, ubit, const, flag

    for k, ll_v in new_points.items():
        for num, chip in enumerate(ll_v):
            for num_p, point in enumerate(chip):
                if input_point == point:
                    if len(chip) > 1:
                        s = set()
                        s.add(input_point)
                        if any(p not in ranen for p in set(chip).difference(s)):
                            df.loc[input_point[0], input_point[1]] = 'Р'
                            print(input_point, 'Ранен')
                            ranen.append(input_point)
                            const[input_point] = 0  #
                            shot_p, shot_d, diag_p = get_cum_points(input_point)
                            for d_p in diag_p:
                                const[d_p] = 0
                            for p_shot in shot_p:
                                const[p_shot] = 0.5
                            flag = False
                            break
                        elif all(p in ranen for p in set(chip).difference(s)) or all(
                                p in ubit for p in set(chip).difference(s)):
                            for p in chip:
                                df.loc[p[0], p[1]] = 'У'
                                print(p, 'Убит')
                                ubit.append(p)
                                const[p] = 0
                                shot_p, shot_d, diag_p = get_cum_points(p)
                                for d_p in diag_p:
                                    const[d_p] = 0
                                for p_shot in shot_p:
                                    const[p_shot] = 0
                            flag = False
                            break
                    elif len(chip) == 1:
                        df.loc[input_point[0], input_point[1]] = 'У'
                        print(input_point, 'Убит')
                        ubit.append(input_point)
                        const[input_point] = 0
                        shot_p, shot_d, diag_p = get_cum_points(input_point)
                        for d_p in diag_p:
                            const[d_p] = 0
                        for p_shot in shot_p:
                            const[p_shot] = 0
                        flag = False
                        break
            if flag is False:
                break
        if flag is False:
            break
    if flag == True:
        print(input_point, 'Мимо')
        const[input_point] = 0
    return df, ranen, ubit, const, flag


