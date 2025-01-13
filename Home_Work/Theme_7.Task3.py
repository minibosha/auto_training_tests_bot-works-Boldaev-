# Скачиваем библиотеку для распознавания всех вхождений в строку
import re


class Text:
    def __init__(self, string : str):
        self._block = []

        # Находим вхождений всех переходов в строку, чтобы определить что это новая строка в блоке
        matches = re.finditer('\n', string)
        indices = [match.start() for match in matches]

        # Разделяем строки и добавляем в блок, если есть переходы на новую строку
        if indices:
            start = 0
            for i in indices:
                self._block.append(string[start:i])
                start = i
            # Добавляем последнюю строку
            self._block.append(string[i:])
            # Убираем знак перехода на новую строку
            for line in range(1, len(self._block)):
                self._block[line] = self._block[line][1:]
        # Если строка без перехода, то просто её добавляем
        else:
            self._block.append(string)

    def count_strings(self):
        return len(self._block)

    def get_string(self, index):
        return self._block[index]

    def count_words_in_string(self, index):
        return len(self._block[index].split())

    def get_word_from_string(self, index, word):
        return self._block[index].split()[word]

class EditableText(Text):
    def change_string(self, index, new_string):
        self._block[index] = new_string
        return self._block[index]

    def change_word_in_string(self, index, word, new_word):
        self._block[index].split()[word] = new_word
        return self._block[index]

    def find_word_in_text(self, word):
        found = ''
        for ind, string in enumerate(self._block):
            # Находим вхождения слова если есть
            matches = re.finditer(word, string)
            indices = [match.start() for match in matches]

            # Добавляем найденные индексы вхождений слова в строку, если есть
            if indices:
                found += f'Номера вхождения в {ind-1} строке: {indices}'

        # Проверяем что есть хотя-бы одно слово
        if found:
            return found
        else:
            return "Нету слов в тексте"

    def __repr__(self):
        return '\n'.join(self._block)


# Проверяем функции класса Text
txt = Text('Hello World!\nNo answer\nIm alone there?')
print(txt._block)
print(txt.count_strings())
print(txt.get_string(1))
print(txt.count_words_in_string(1))
print(txt.get_word_from_string(1, 1))


# Проверяем функции класса EditableText
ed_txt = EditableText('Hello World!\nNo answer\nIm alone there?')
print()
print(ed_txt.change_string(1, "No, you're not"))
print(ed_txt.change_word_in_string(2, 2, 'not alone')) # Неправильно работает, завтра исправлю ;)
print(ed_txt.find_word_in_text('not'))
print()
print(ed_txt)