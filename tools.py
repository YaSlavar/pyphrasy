import xml.etree.ElementTree as ET


def createXML(response):
    """
    Создаем XML строку
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

    return ET.tostring(root, encoding='utf-8', method='xml')
