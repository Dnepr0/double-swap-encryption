from sys import argv
from math import ceil
from itertools import permutations
from lib import _MIN_KEY_LENGTH, _MAX_KEY_LENGTH, \
    str_to_table, create_key, str_to_seq, display_progress
from time import time
from tree import Tree

_RES_FILE_NAME = "res/hacked.txt"
_DICT_FILE_NAME = "dict/ru.txt"

def hack(text, tree):
    """
    Подбирает ключ шифрования к зашифрованому сообщению
    """
    # Перебираем возможные размеры ключа
    for n in range(_MIN_KEY_LENGTH, _MAX_KEY_LENGTH + 1):
        print("\tПодбираем ключ длины " + str(n) + " ...", end="")
        m = ceil(len(text) / n)
        # Создаем таблицу нужного размера
        table = str_to_table(text, n, m)
        # Наборы значений для перебора ключа
        key1_set = [i for i in range(n)]
        # Перебираем все возможные перестановки 
        for key1 in permutations(key1_set):
            # Вычисляем второй ключ, на основе первого
            key2 = str_to_seq(create_key(key1, m))
            # Получаем дешифровку
            res = ""
            for i in key1:
                for j in key2:
                    if table[i][j] == "-":
                        res += " "
                    else:
                        res += table[i][j]
            # Если она верна, возврашаем результат
            if is_decrypted(res, tree):
                return res
            else: 
                display_progress()

def is_decrypted(text, tree):
    """
    Определяет, является ли полученная строка расшифровкой
    """
    num = 3
    find = 0
    # Перебираем первые num слов в тексе
    for word in text.split(" ", num):
        if len(word) > 1 and len(word) < 26:
            # Если нашли совпадение
            if tree.contains(word):
                find += 1
                if find == num:
                    return True
            else:
                return False

if __name__ == '__main__':
    if len(argv) == 2:
        # Читаем текст
        with open(argv[1], 'r', encoding='utf-8') as file:
            text = file.read()
        # Читаем словарь
        with open(_DICT_FILE_NAME, 'r', encoding='utf-8') as file:
            vocabulary = file.read().split('\n')
        start_time = time()
        # Строим дерево
        tree = Tree(vocabulary)
        del vocabulary
        # Взлом перебором
        hacked = hack(text, tree)
        # Запись результата в файл
        if (hacked):
            with open(_RES_FILE_NAME, "w", encoding='utf-8') as file:
                file.write(hacked)
                print("\nПодобранный текст помещен в файл " + _RES_FILE_NAME)
        else:
            print("\nТекст не был распознан" + _RES_FILE_NAME)
        print("--- %s seconds ---" % round((time() - start_time), 2))
    else:
        print("Неверный ситаксис.\nИспользуйте - hack.py <filename>")