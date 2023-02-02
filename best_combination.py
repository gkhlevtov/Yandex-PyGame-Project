sequence = '1 2 3 4 5 6 7 8 9 10 11 12 13 14'  # Порядок значений
# Порядок покерных комбинаций
combinations = ['Старшая карта', 'Пара', 'Две пары', 'Сет', 'Стрит', 'Флеш', 'Фулл-хаус', 'Каре', 'Стрит-флеш']


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
    sp = [values.count(x) for x in a]
    return sorted(list(zip(a, sp)), key=lambda x: -x[1])


def max_kickers(name, lst, res):  # Определение максимальных кикеров
    k = sorted([x for x in lst if x not in res], key=lambda x: x[1])
    if name == 'Каре' or name == 'Две пары':
        return [k[-1]]
    elif name == 'Сет':
        return k[-2:]
    return k[-3:]


def comb(values, suits, f=True):  # Определение комбинации
    if f and 14 in values:  # Если в комбинации встречается туз, то рассматриваем случай как с 14, так и с 1
        comb1, comb2 = comb(values, suits, False), comb([1 if x == 14 else x for x in values], suits, False)
        if best_comb(*comb1, *comb2):
            return comb1
        return comb2
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
        res = sorted(filter(lambda x: x[1] == v4, lst))
        return 'Каре', max_kickers('Каре', lst, res) + res

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
        res = sorted(filter(lambda x: x[2] == s5, lst), key=lambda x: (x[1], x[0]))
        if len(res) == 6:
            res = res[1:]
        elif len(res) == 7:
            res = res[2:]
        return 'Флеш', res

    # Комбинация Стрит
    slst = list(map(str, sorted(set(values))))  # Отсортированный список с множеством значений
    if len(slst) >= 5:
        if (len(slst) == 5 and ' '.join(slst) in sequence) or \
                (len(slst) == 6 and (' '.join(slst[:5]) in sequence or ' '.join(slst[1:]) in sequence)) or \
                (len(slst) == 7 and (
                        ' '.join(slst[:5]) in sequence or ' '.join(slst[1:6]) in sequence or ' '.join(slst[2:])
                        in sequence)):
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
                    if len(res) == 4:
                        res.append(tlst[i])
                        break
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
        res = sorted((filter(lambda x: x[1] == v3, lst)))
        return 'Сет', max_kickers('Сет', lst, res) + res

    # Комбинация Две пары
    if count_v[0][1] == 2 and count_v[1][1] == 2:
        # Определение наибольших значений, встречающихся 2 раза
        if count_v[2][1] == 2:
            v21, v22 = sorted([count_v[0][0], count_v[1][0], count_v[2][0]], reverse=True)[:2]
        else:
            v21, v22 = sorted([count_v[0][0], count_v[1][0]], reverse=True)
        # Результат сортируем по значению в порядке невозрастания и по id в порядке возрастания
        res = sorted((filter(lambda x: x[1] == v21 or x[1] == v22, lst)), key=lambda x: (-x[1], x[0]))
        return 'Две пары', max_kickers('Две пары', lst, res) + res

    # Комбинация Пара
    if count_v[0][1] == 2:
        v2 = count_v[0][0]
        # Результат сортируем по id в порядке возрастания
        res = sorted((filter(lambda x: x[1] == v2, lst)))
        return 'Пара', max_kickers('Пара', lst, res) + res
    return 'Старшая карта', [max(lst, key=lambda x: x[1])]


kickers = 0  # Количество значимых кикеров


def best_comb(name1, comb1, name2, comb2):  # Определение лучшей комбинации
    global kickers
    kickers = 0
    if name1 != name2:
        if combinations.index(name1) > combinations.index(name2):
            return '1'
        return '0'
    name = name1
    if name == 'Стрит-флеш' or name == 'Стрит' or name == 'Старшая карта':
        if comb1[-1][1] > comb2[-1][1]:
            return '1'
        elif comb1[-1][1] == comb2[-1][1]:
            return 'draw'
        return '0'
    if name == 'Каре':
        if comb1[-1][1] > comb2[-1][1]:
            return '1'
        if comb1[-1][1] < comb2[-1][1]:
            return '0'
        kickers += 1
        if comb1[0][1] > comb2[0][1]:
            return '1'
        if comb1[0][1] < comb2[0][1]:
            return '0'
        return 'draw'
    if name == 'Сет':
        if comb1[-1][1] > comb2[-1][1]:
            return '1'
        if comb1[-1][1] < comb2[-1][1]:
            return '0'
        for i in range(1, -1, -1):
            kickers += 1
            if comb1[i][1] > comb2[i][1]:
                return '1'
            if comb1[i][1] < comb2[i][1]:
                return '0'
        return 'draw'
    if name == 'Пара':
        if comb1[-1][1] > comb2[-1][1]:
            return '1'
        if comb1[-1][1] < comb2[-1][1]:
            return '0'
        for i in range(2, -1, -1):
            kickers += 1
            if comb1[i][1] > comb2[i][1]:
                return '1'
            if comb1[i][1] < comb2[i][1]:
                return '0'
        return 'draw'
    if name == 'Фулл-хаус':
        if comb1[0][1] > comb2[0][1]:
            return '1'
        elif comb1[0][1] == comb2[0][1] and comb1[-1][1] > comb2[-1][1]:
            return '1'
        elif comb1[-1][1] == comb2[-1][1]:
            return 'draw'
        return '0'
    if name == 'Две пары':
        if comb1[1][1] > comb2[1][1]:
            return '1'
        if comb1[1][1] < comb2[1][1]:
            return '0'
        if comb1[-1][1] > comb2[-1][1]:
            return '1'
        if comb1[-1][1] < comb2[-1][1]:
            return '0'
        kickers += 1
        if comb1[0][1] > comb2[0][1]:
            return '1'
        if comb1[0][1] < comb2[0][1]:
            return '0'
        return 'draw'
    if name == 'Флеш':
        if comb1[-1][1] > comb2[-1][1]:
            return '1'
        elif comb1[-1][1] == comb2[-1][1] and comb1[-2][1] > comb2[-2][1]:
            return '1'
        elif comb1[-2][1] == comb2[-2][1] and comb1[-3][1] > comb2[-3][1]:
            return '1'
        elif comb1[-3][1] == comb2[-3][1] and comb1[-4][1] > comb2[-4][1]:
            return '1'
        elif comb1[-4][1] == comb2[-4][1] and comb1[-5][1] > comb2[-5][1]:
            return '1'
        elif comb1[-5][1] == comb2[-5][1]:
            return 'draw'
        return '0'


def output(name, c):  # Вывод комбинации и значимых кикеров при их наличии
    if name == 'Каре' or name == 'Сет' or name == 'Две пары' or name == 'Пара':
        if kickers:
            if name == 'Каре' or name == 'Две пары':
                return name, c[1:], [c[0]]
            if name == 'Сет':
                return name, c[2:], c[2 - kickers:2]
            if name == 'Пара':
                return name, c[3:], c[3 - kickers:3]

        else:
            if name == 'Каре' or name == 'Две пары':
                return name, c[1:], []
            if name == 'Сет':
                return name, c[2:], []
            if name == 'Пара':
                return name, c[3:], []

    return name, c, []
