import json
import pymorphy2
from inflect import PhraseInflector, GRAM_CHOICES
from tools import create_XML, change_case
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import RedirectResponse, Response
from typing import List, Optional
import uvicorn

app = FastAPI(title="pyphrasy")


def inflect(phrase: str = 'Тестовое слово',
            forms: Optional[List[str]] = Query(['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']),
            response_type: Optional[str] = 'json'):
    """
    Склонение фраз
    - **phrase**: Фраза для склонения
    - **forms**: Формы склонения
        - **nomn** - именительный
        - **gent** - родительный
        - **datv** - дательный
        - **accs** - винительный
        - **ablt** - творительный
        - **loct** - предложный
        - **voct** - звательный
        - **gen2** - второй родительный (частичный)
        - **acc2** - второй винительный
        - **loc2** - второй предложный (местный)

    - **response_type**: Формат ответа json|xml
    :rtype: Response
    """
    # Приведение строки формата ответа к нижнему регистру, если она задана
    if response_type:
        response_type = response_type.lower()

    # Если параметры заданы неверно, возврат ошибки
    if not phrase:
        raise HTTPException(status_code=400, detail="u'Укажите слово'")
    if not forms:
        raise HTTPException(status_code=400, detail="u'Выберите падежи или/и числа")
    if 'xml' not in response_type and 'json' not in response_type:
        raise HTTPException(status_code=400, detail="u'Неверно задан вормат отрета response_type = json|xml'")

    # Инициализация объектов
    morph = pymorphy2.MorphAnalyzer()
    inflector = PhraseInflector(morph)

    # Инициализация словаря результата
    result = {
        'input_str': phrase,
        'forms': {}
    }

    # Цикл по граммемам
    for forms_string in forms:
        # Получение граммемы
        form_set = set(forms_string.split(',')) & set(GRAM_CHOICES)
        # Преобразование фразы
        inflected_phrase = inflector.inflect(phrase, form_set)
        # Исправление регистра преобразованной фразы
        corrected_inflected_phrase = change_case(phrase, inflected_phrase)
        # Заполнение словаря результатов
        result['forms'][forms_string] = corrected_inflected_phrase

    # Формирование результируещей строки
    if response_type == 'json':
        formatted_result = json.dumps(result, ensure_ascii=False).encode('utf8')
        return Response(content=formatted_result, media_type="application/json")
    elif response_type == 'xml':
        formatted_result = create_XML(result)
        return Response(content=formatted_result, media_type="application/xml")


@app.get("/", tags=["index"])
def index() -> RedirectResponse:
    """
    Документация к API
    """
    return RedirectResponse("/docs")


@app.get("/inflect", tags=["inflect"], response_description="Inflected phrases")
def inflect_get(phrase: str = 'Тестовое слово',
                forms: Optional[List[str]] = Query(['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']),
                response_type: Optional[str] = 'json') -> Response:
    """
    Склонение фраз
    - **phrase**: Фраза для склонения
    - **forms**: Формы склонения
        - **nomn** - именительный
        - **gent** - родительный
        - **datv** - дательный
        - **accs** - винительный
        - **ablt** - творительный
        - **loct** - предложный
        - **voct** - звательный
        - **gen2** - второй родительный (частичный)
        - **acc2** - второй винительный
        - **loc2** - второй предложный (местный)

    - **response_type**: Формат ответа json|xml
    """
    return inflect(phrase, forms, response_type)


@app.post("/inflect", tags=["inflect"], response_description="Inflected phrases")
def inflect_post(phrase: str = 'Тестовое слово',
                 forms: Optional[List[str]] = Query(['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']),
                 response_type: Optional[str] = 'json') -> Response:
    """
    Склонение фраз
    - **phrase**: Фраза для склонения
    - **forms**: Формы склонения
        - **nomn** - именительный
        - **gent** - родительный
        - **datv** - дательный
        - **accs** - винительный
        - **ablt** - творительный
        - **loct** - предложный
        - **voct** - звательный
        - **gen2** - второй родительный (частичный)
        - **acc2** - второй винительный
        - **loc2** - второй предложный (местный)

    - **response_type**: Формат ответа json|xml
    """
    return inflect(phrase, forms, response_type)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
