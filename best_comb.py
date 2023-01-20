sequence = '1 2 3 4 5 6 7 8 9 10 11 12 13 14'  # Порядок значений


def suit5(suits):  # Проверка на наличие масти, встречающейся 5 раз
    suits = ''.join(sorted(suits))
    if 'HHHHH' in suits:
        return 'H'
    if 'SSSSS' in suits:
        return 'S'
    if 'CCCCC' in suits:
        return 'C'
    if 'DDDDD' in suits:
        return 'D'
    return False


def count_values(values):  # Частотность значений
    a = list(set(values))
    b = [values.count(x) for x in a]
    return sorted(list(zip(a, b)), key=lambda x: -x[1])


def comb(values, suits):  # Определение комбинации
    s5 = suit5(suits)  # Масть, встречающаяся 5 раз
    count_v = count_values(values)  # Список частотности значений

    # Преобразование входных данных в список кортежей типа "(<id>, <значение>, <масть>)"
    inp = list(zip(list(range(8)), values, suits))

    # Сортировка списка по масти в лексикографическом порядке, по значению в порядке невозрастания
    lst = sorted(inp, key=lambda x: (x[2], -x[1]))

    # Комбинация Стрит-флеш
    if s5:
        for i in range(3):
            f = True
            for j in range(i, i + 4):
                # Проверка на порядок значений и одинаковую масть
                if lst[j][1] - 1 != lst[j + 1][1] or lst[j][2] != s5 or lst[j + 1][2] != s5:
                    f = False
                    break
            if f:
                return 'Стрит-флеш', lst[i:i + 5][::-1]

    # Комбинация Каре
    if count_v[0][1] == 4:
        v4 = count_v[0][0]  # Значение, встречающееся 4 раза
        # Результат сортируем по id в порядке возрастания
        return 'Каре', sorted(filter(lambda x: x[1] == v4, lst))

    # Комбинация Фулл-хаус
    if count_v[0][1] == 3 and count_v[1][1] == 2:
        v3 = count_v[0][0]  # Значение, встречающееся 3 раза
        # Определение наибольшего значения, встречающегося 2 раза
        if count_v[2][1] == 2 and count_v[2][0] > count_v[1][0]:
            v2 = count_v[2][0]
        else:
            v2 = count_v[1][0]
        # Результат сортируем по значению в порядке невозрастания и по id в порядке возрастания
        return 'Фулл-хаус', sorted((filter(lambda x: x[1] == v3 or x[1] == v2, lst)), key=lambda x: (-x[1], x[0]))

    # Комбинация Флеш
    if s5:
        # Результат сортируем по значению и id в порядке возрастания
        return 'Флеш', sorted(filter(lambda x: x[2] == s5, lst), key=lambda x: (x[1], x[0]))

    # Комбинация Стрит
    slst = list(map(str, sorted(set(values))))  # отсортированный список с множеством значений
    print(slst)
    if len(slst) >= 5:
        if (len(slst) == 5 and ' '.join(slst) in sequence) or \
                (len(slst) == 6 and (' '.join(slst)[:5] in sequence or ' '.join(slst)[1:] in sequence)) or \
                (len(slst) == 7 and (
                        ' '.join(slst)[:5] in sequence or ' '.join(slst)[1:6] in sequence or ' '.join(slst)[
                                                                                             2:] in sequence)):
            # Временный список, отсортированный по значению в порядке невозрастания и по id в порядке возрастания
            tlst = sorted(lst, key=lambda x: (-x[1], x[0]))
            res = []
            for i in range(len(tlst) - 1):
                # Проверка на порядок значений
                if tlst[i][1] - 1 == tlst[i + 1][1]:
                    res.append(tlst[i])
                elif tlst[i][1] == tlst[i + 1][1]:
                    continue
                else:
                    res.clear()
            if len(res) == 4:
                res.append(tlst[-1])
            if len(res) == 5:
                return 'Стрит', res[::-1]

    # Комбинация Сет
    if count_v[0][1] == 3:
        # Определение наибольшего значения, встречающегося 3 раза
        if count_v[1][1] == 3 and count_v[1][0] > count_v[0][0]:
            v3 = count_v[1][0]
        else:
            v3 = count_v[0][0]
        # Результат сортируем по id в порядке возрастания
        return 'Сет', sorted((filter(lambda x: x[1] == v3, lst)))

    # Комбинация Две пары
    if count_v[0][1] == 2 and count_v[1][1] == 2:
        # Определение наибольших значений, встречающихся 2 раза
        if count_v[2][1] == 2:
            v21, v22 = sorted([count_v[0][0], count_v[1][0], count_v[2][0]], reverse=True)[:2]
        else:
            v21, v22 = sorted([count_v[0][0], count_v[1][0]], reverse=True)
        # Результат сортируем по значению в порядке невозрастания и по id в порядке возрастания
        return 'Две пары', sorted((filter(lambda x: x[1] == v21 or x[1] == v22, lst)), key=lambda x: (-x[1], x[0]))

    # Комбинация Пара
    if count_v[0][1] == 2:
        v2 = count_v[0][0]
        # Результат сортируем по id в порядке возрастания
        return 'Пара', sorted((filter(lambda x: x[1] == v2, lst)))
    return 'Старшая карта', [max(lst, key=lambda x: x[1])]


def best_comb(name, comb1, comb2):  # Определение лучшей комбинации
    if name == 'Стрит-флеш' or name == 'Каре' or name == 'Сет' or name == 'Пара' or name == 'Старшая карта':
        return comb1[-1][1] >= comb2[-1][1]
    if name == 'Фулл-хаус' or name == 'Две пары':
        if comb1[0][1] > comb2[0][1]:
            return True
        elif comb1[0][1] == comb2[0][1] and comb1[-1][1] >= comb2[-1][1]:
            return True
        return False
    if name == 'Флеш' or name == 'Стрит':
        if comb1[-1][1] > comb2[-1][1]:
            return True
        elif comb1[-1][1] == comb2[-1][1] and comb1[-2][1] > comb2[-2][1]:
            return True
        elif comb1[-2][1] == comb2[-2][1] and comb1[-3][1] > comb2[-3][1]:
            return True
        elif comb1[-3][1] == comb2[-3][1] and comb1[-4][1] > comb2[-4][1]:
            return True
        elif comb1[-4][1] == comb2[-4][1] and comb1[-5][1] >= comb2[-5][1]:
            return True
        return False


if __name__ == '__main__':
    n, c1 = comb(list(map(int, input().split())), input().split())

    # c2 = comb(list(map(int, input().split())), input().split())[1]
    # print(best_comb(n, c1, c2))

    print(n)
    print(c1)

'''
Два Стрит-флеша
1 2 3 4 5 6 7
H H H H H H H
3 4 5 6 7 8 9
D D D D D D D
'''
