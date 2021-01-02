# -*- coding: utf-8 -*-
import json
import pymorphy2
from flask import Flask, request, render_template
from inflect import PhraseInflector, GRAM_CHOICES
from tools import createXML

app = Flask(__name__)
app.debug = True


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/inflect", methods=['GET', 'POST'])
def inflect():
    # По умолчанию возвращаем ответ в формате JSON
    response_type = 'json'

    if request.method == 'POST':
        params = request.form
    else:
        params = request.args

    if 'phrase' not in params:
        return u'Укажите слово', 400, {'Content-Type': 'text/plain; charset=utf-8'}
    if 'forms' not in params and 'cases' not in params:
        return u'Выберите падежи или/и числа', 400, {'Content-Type': 'text/plain; charset=utf-8'}
    if 'response_type' in params:
        response_type = params['response_type']

    phrase = params['phrase']
    form_sets = params.getlist('forms') if params.getlist('forms') else params.getlist('cases')

    morph = pymorphy2.MorphAnalyzer()
    inflector = PhraseInflector(morph)

    result = {
        'input_str': phrase,
        'forms': {}
    }

    for forms_string in form_sets:
        form_set = set(forms_string.split(',')) & set(GRAM_CHOICES)
        result['forms'][forms_string] = inflector.inflect(phrase, form_set)

    formatted_result = 'None'

    if response_type == 'json':
        formatted_result = json.dumps(result, ensure_ascii=False).encode('utf8')
    elif response_type == 'xml':
        formatted_result = createXML(result)

    print(result)
    return formatted_result, 200, {'Content-Type': 'text/' + response_type + '; charset=utf-8'}


if __name__ == "__main__":
    app.run()
