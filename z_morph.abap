FUNCTION ZHTTP_CLIENT_TEST.
*"----------------------------------------------------------------------
*"*"Локальный интерфейс:
*"   Формы склонения
*"   nomn - именительный
*"   gent - родительный
*"   datv - дательный
*"   accs - винительный
*"   ablt - творительный
*"   loct - предложный
*"   voct - звательный
*"   gen2 - второй родительный (частичный)
*"   acc2 - второй винительный
*"   loc2 - второй предложный (местный)
*"  IMPORTING
*"     REFERENCE(INPUT_STR) TYPE  ZMORPH_STR
*"     REFERENCE(INPUT_FORMS) TYPE  ZMORPH_STR
*"  EXPORTING
*"     REFERENCE(EXPORT_STRUCT) TYPE  ZMORPH_S_RESULT
*"     REFERENCE(EXPORT_STR) TYPE  ZMORPH_STR
*"  EXCEPTIONS
*"      NOT_RESPONSE
*"      ERR_XML_TRANSFORMATION
*"----------------------------------------------------------------------

  DATA: lv_http_dest TYPE rfcdest VALUE 'ZMORPH_REST_API'," http соединение в sm59
        lo_client TYPE REF TO if_http_client,
        lo_request TYPE REF TO if_http_request,
        lv_http_subrc TYPE sy-subrc,
        lv_xml_xstring TYPE XSTRING.

  DATA : rest_table OCCURS 0 WITH HEADER LINE,
         lo_conversion TYPE REF TO cl_abap_conv_in_ce,
         lv_response TYPE string.

  DATA : ls_morph TYPE ZMORPH_S_RESULT,
         ls_forms TYPE ZMORPH_FORMS.

  " Создание соеднинения с API
  cl_http_client=>create_by_destination(
    EXPORTING DESTINATION = lv_http_dest
    IMPORTING CLIENT = lo_client
  ).

  " Метод запроса GET
  CALL METHOD lo_client->request->set_method(
    if_http_request=>co_request_method_get
  ).

  lo_request = lo_client->request.

  " Искомая фраза
  CALL METHOD lo_request->SET_FORM_FIELD
    EXPORTING
      NAME  = 'phrase'
      VALUE = INPUT_STR.


  " Параметры преобразований (склонения)
  CALL METHOD lo_request->SET_FORM_FIELD
    EXPORTING
      NAME  = 'forms'
      VALUE = INPUT_FORMS.

  " Формат ответа (xml|json)
  CALL METHOD lo_request->SET_FORM_FIELD
    EXPORTING
      NAME  = 'response_type'
      VALUE = 'xml'.

  " Отправка запроса
  CALL METHOD lo_client->send
    EXCEPTIONS
      http_communication_failure = 1
      http_invalid_state         = 2
      http_processing_failed     = 3
      http_invalid_timeout       = 4
      OTHERS                     = 5.

  IF sy-subrc <> 0.

  ENDIF.

  " Обработка ответа
  CALL METHOD lo_client->receive
    EXCEPTIONS
      http_communication_failure = 1
      http_invalid_state         = 2
      http_processing_failed     = 3
      OTHERS                     = 4.


  IF sy-subrc = 0.
    lo_client->response->get_status(
      IMPORTING code = lv_http_subrc
    ).

    IF lv_http_subrc <> 200.
      " Не получен ответ
      RAISE NOT_RESPONSE.
    ELSE.
      " Получение тела ответа
      CLEAR: lv_xml_xstring.
      lv_xml_xstring = lo_client->response->get_data( ).

      " Завершение соединения
      lo_client->CLOSE( ).

      " Преобразование полученных данных в строку
      lo_conversion = cl_abap_conv_in_ce=>create( input = lv_xml_xstring ).
      lo_conversion->read(
        IMPORTING data = lv_response
      ).

      IF lv_response IS NOT INITIAL.
        " Преобразование XML в ABAP структуру
        CALL TRANSFORMATION Z_MORPH_XML_TEST
          SOURCE XML lv_response
          RESULT response = ls_morph.

        IF sy-subrc <> 0.
          " Не удалось преобразовать XML ответ
          RAISE ERR_XML_TRANSFORMATION.
        ENDIF.
      ENDIF.

    ENDIF.
  ENDIF.

  " Получение строки ответа
  IF ls_morph IS NOT INITIAL.
    READ TABLE ls_morph-forms INTO ls_forms INDEX 1.
    IF sy-subrc = 0.
      EXPORT_STR = ls_forms-value.
    ENDIF.
  ENDIF.

  " Получение структуры ответа
  EXPORT_STRUCT = ls_morph.

ENDFUNCTION.