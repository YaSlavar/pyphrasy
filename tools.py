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
        append_form = ET.SubElement(forms, form_name)
        append_form.text = form_value

    return ET.tostring(root, encoding='utf-8', method='xml')
