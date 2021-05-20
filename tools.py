import xml.etree.ElementTree as ET
from io import BytesIO
import re


def create_XML(response: dict) -> str:
    """
    Создание XML строки
    :param response: Словарь результата
    :return: Строка в формате XML
    """
    root = ET.Element("response")

    input_str = ET.SubElement(root, "input_str")
    input_str.text = response['input_str']

    forms = ET.Element("forms")
    root.append(forms)

    for form_name, form_value in response['forms'].items():
        form = ET.Element("form")
        forms.append(form)

        append_form_key = ET.SubElement(form, 'key')
        append_form_key.text = form_name

        append_form_value = ET.SubElement(form, 'value')
        append_form_value.text = form_value

    et = ET.ElementTree(root)
    byte_obj = BytesIO()
    et.write(byte_obj, encoding='utf-8', xml_declaration=True)

    return byte_obj.getvalue().decode("utf-8")


def change_case(source_str: str, inflected_str: str) -> str:
    """
    Восстановление регистра фразы
    :param source_str: Исходная строка
    :param inflected_str: Преобразованная строка
    :return: Преобразованная строка с восстановленным регистром
    """
    # Фраза в кавычках
    PATTERN = r'(["|«][\w\d \t\v\r\n\f]*["|»])'

    corrected_inflected_word_list = []

    # Замена преобразованного словосочетания в кавычках на словосочетание из исходной фразы
    inflected_str_by_pattern = re.split(PATTERN, inflected_str)
    marked_srt_by_pattern = re.findall(PATTERN, source_str)

    formatted_str = ''
    index_marked_phrase_in_str = 0
    try:
        for phrase in inflected_str_by_pattern:
            # Если подстрока в кавычках
            if re.search(PATTERN, phrase):
                # Замена подстрокой из исходной строки
                phrase = marked_srt_by_pattern[index_marked_phrase_in_str]
                index_marked_phrase_in_str += 1

            formatted_str += phrase
        inflected_str = formatted_str
    except IndexError as err:
        pass

    # Получение списка слов исходной и преобразованной строк
    source_str_word_list = source_str.split(' ')
    inflected_str_word_list = inflected_str.split(' ')

    for source_word, inflected_word in zip(source_str_word_list, inflected_str_word_list):
        corrected_inflected_word = ''

        # Вычисление максимальной длины и выравнивание длины строк, так как при
        # разной длине строк при использовании zip() результирующий кортеж получается равный
        # длине самого короткого слова. Недостающие символы при выравнивании строк заменяются
        # пустым символом ' ', который является символом нижнего регистра
        max_word_len = max(len(source_word), len(inflected_word))
        if len(source_word) < max_word_len:
            delta_len = max_word_len - len(source_word)
            source_word += ' ' * delta_len
        elif len(inflected_word) < max_word_len:
            delta_len = max_word_len - len(inflected_word)
            inflected_word += ' ' * delta_len

        for source_word_letter, inflected_word_letter in zip(source_word, inflected_word):
            # Проверка на регистр по символам исходной строки
            if source_word_letter.isupper():
                inflected_word_letter = inflected_word_letter.upper()

            corrected_inflected_word += inflected_word_letter
        corrected_inflected_word_list.append(corrected_inflected_word)

    return ' '.join(corrected_inflected_word_list)


if __name__ == '__main__':
    res = change_case('Государственное бюджетное учреждение города Москвы "Московская ярмарка"',
                      'Государственного бюджетного учреждения города Москвы "Московского ярмарки"')

    # res = change_case('ааа "ббб" ввв "ггг" "" ддд «еее»',
    #                   'аааааа "бббббб" вввввв "ггггггг" "" ддддддд «ееееееее»')

    print(res)
