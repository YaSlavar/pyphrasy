<?sap.transform simple?>
<tt:transform xmlns:tt="http://www.sap.com/transformation-templates" xmlns:ddic="http://www.sap.com/abapxml/types/dictionary" xmlns:def="http://www.sap.com/abapxml/types/defined">
  <tt:root name="RESPONSE" type="ddic:ZMORPH_INFLECT"/>
  <tt:template>
    <response>
      <input_str tt:value-ref="RESPONSE.INPUT_STR"/>
      <forms>
      <tt:loop ref="RESPONSE.FORMS">
        <form>
          <key tt:value-ref="KEY"/>
          <value tt:value-ref="VALUE"/>
        </form>
      </tt:loop>
     </forms>
    </response>
  </tt:template>
</tt:transform>