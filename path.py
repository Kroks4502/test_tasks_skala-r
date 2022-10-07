import re
from typing import KeysView

PATTERN_NAMES_ALPHABET = re.compile(r'[0-9a-zA-Z]+')
NAMES_ALPHABET = {chr(y) for y in range(48, 58)} | {chr(y) for y in range(65, 91)} | {chr(y) for y in range(97, 123)}
MAX_LEN_PATH = 255


class IncorrectPath(Exception):
    pass


def isCorrectName(name: str) -> None:
    if not bool(re.fullmatch(PATTERN_NAMES_ALPHABET, name)):
        raise IncorrectPath(f'Некорректное имя папки или файла: {name}')


def isCorrectNameWithOutRe(name: str) -> None:
    """Функция проверки корректности имени без использования регулярных выражений."""
    for char in name:
        if char not in NAMES_ALPHABET:
            raise IncorrectPath(f'Некорректное имя папки или файла: {name}')


def isCorrectPath(path: str) -> None:
    if len(path) > MAX_LEN_PATH:
        raise IncorrectPath(f'Длина пути превышает {MAX_LEN_PATH} символов.')


def isUniqueNames(path: str, names: list | KeysView) -> None:
    if len(names) != len({*names}):
        raise IncorrectPath(f'В директории могут быть только уникальные имена. '
                            f'По пути {path} содержатся файлы со следующими именами: {names}')


def finderPath(path: str, X: dict) -> str:
    isUniqueNames(path, X.keys() if isinstance(X, dict) else X)

    biggest_path = path
    biggest_path_len = len(path)
    for key in X:
        isCorrectName(key)
        current_path = finderPath(f'{path}/{key}', X[key]) if isinstance(X, dict) else f'{path}/{key}'
        isCorrectPath(current_path)
        if (current_len := len(current_path)) > biggest_path_len:
            biggest_path = current_path
            biggest_path_len = current_len
    return biggest_path


def biggestPath(X: dict) -> str:
    try:
        biggest_path = finderPath('', X)
    except IncorrectPath as err:
        # todo: Добавить запись в лог
        print('Error:', err)
        return '/'
    return biggest_path


print(biggestPath({'dir1': {}, 'dir2': ['file1'], 'dir3': {'dir4': ['file2'], 'dir5': {'dir6': {'dir7': {}}}}}))
# /dir3/dir5/dir6/dir7

print(biggestPath({'dir1': ['file1', 'file1']}))
# /

print(biggestPath({'dir1': ['file1', 'file2', 'file3']}))
# /dir1/file1
