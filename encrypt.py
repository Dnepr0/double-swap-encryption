from sys import argv
from math import ceil
from lib import *

def encrypt(text, key):
    """
    Шифрует текст с помощью полученного ключа методом двойной перестановки
    """
    # Преобразуем входные данные к нужному формату
    text = convert_text(text)
    key1 = convert_key(key)
    # Вычисляем размеры таблицы
    m = ceil(len(text) / len(key1))
    # Создаем таблицу (матрицу) нужного размера
    table = str_to_table(text, len(key1), m)
    # Генерируем второй ключ из первого нужной длинны
    key2 = str_to_sort_seq(create_key(key1, m))
    key1 = str_to_sort_seq(key1)
    # Получаем преобразованную строку сгенерированную по ключам
    res = ""
    for i in key1:
        for j in key2:
            if table[i][j] != "-":
                res += table[i][j]

    return res

if __name__ == '__main__':
    if len(argv) == 3:
        # Считывание входных данных
        key = argv[1]
        with open(argv[2], 'r', encoding='utf-8') as file:
            text = file.read()
        # Шифрование
        encrypted = encrypt(text, key)
        # Запись результата в файл
        with open("encrypted.txt", "w", encoding='utf-8') as file:
            file.write(encrypted)
    else:
        print("Неверный ситаксис.\nИспользуйте - encrypt.py <key> <filename>")