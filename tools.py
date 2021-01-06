import xml.etree.ElementTree as ET
from io import BytesIO


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
    corrected_inflected_word_list = []

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
