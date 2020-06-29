
This is the original class and type specification for VSCP. Documents and source files are generated from this info. The 'scripts' folder holds scripts to generate different output.

The folder **classes** holds class definitions as xml files with the following structure

```xml
<class id="0"
    name="VSCP Protocol Functionality"
    token="CLASS1.PROTOCOL"
    alternative-token="other token"
    events="n">

<type id="12"
    name="Enter boot loader mode."
    token="" />

</class>
```

**\<events\>** used when this class have the same events as anohter class n.

**\<alternative-token\>** used to set an alternative token.

0.md hoilds class description in Markdown format
0.n.md holds description for types of this class.

Links to other classes should have this format

    [CLASS1.INFORMATION, Type=9 (HEARTBEAT)](./class1.information.md#type9)

### Render templates 

A structure

```xml
<render>
    <vscpworks template="......." />
</render>
```

holds one or more mustache named templates used to display information about an events dynamic data content. The first template defined is **vscpworks**. This template is used to display HTML based info about an event. The event is used as argument when the mustache expression is parsed. Meaning all parts of the event can be used. So for example {{vscpData[0]}} is data byte 0, vscpClass is the class, vscpGuid is the GUID and so on.

A typical example is this visualization for CLASS1.MEASUREMENT

```xml
<vscpworks template="&lt;b&gt;Unit: &lt;/b&gt; = {{unitstr}} [{{unit}}]&lt;br&gt; &lt;b&gt;Sensorindex: &lt;/b&gt; = {{sensorindex}}&lt;br&gt; &lt;b&gt;Value: &lt;/b&gt; = {{val}}{{symbol-utf8}}&lt;br&gt;"
/>
```


### Measurements
The measurement class (10) has a **\<unit\>** token that is used to describe units. Attributes are

* **name** Name for the unit.
* **description** Description of the unit.
* **symbol-ascii** Symbol in ASCII format
* **symbol-utf8** Symbol in UTF8 format
* **conversion** Conversion code to convert a value of the specific unit to a value of unit 0. Javascript [mustache](https://github.com/janl/mustache.js/) format is used as pseudo code for the conversion and value is specified as **{{val}}** in this code. [mathjs]() is used to parse the expression after mustache parser is run.
Set to **{{val}}** if a conversion is not possible.

This is how this looks for the temperature measurement type

```xml
<type id="6" name="Temperature" token="VSCP_TYPE_MEASUREMENT_TEMPERATURE" >
        <units>
            <unit id="0" 
                    name="kelvin"
                    description="Degrees Kelvin"
                    symbol-ascii="K"
                    symbol-utf8="K"
                    conversion="{{val}}"/>
            <unit id="1" 
                    name="celsius"
                    description="Degrees Celsius"
                    symbol-ascii="C"
                    symbol-utf8="°C"        
                    conversion="{{val}} + 273.15 "/>
            <unit id="2" 
                    name="fahrenheit"
                    description="Degrees Fahrenheit"
                    symbol-ascii="F"
                    symbol-utf8="°F" 
                    conversion="({{val}} + 459.67) * 5/9"/>
        </units>
</type>
```

Note that unit can be in the interval 0-255 as class=10 is used to describe also Level II measurement classes. For Level I classes only unit 0-3 is valid of course.

----

## Folders

* **classes** - VSCP class and type definitions.
* **scripts** - Python scripts that generate output
* **cheaders** - templates for c-headers.
* **python** - Templates for Python.
* **javascript** - Templates for JavaScript.
* **db** - Templates for VSCP database.
* **json** -- Templates for JSON file.

## Scripts

### make_c_class_header.py
Make the vscp_class.h header file.

#### Usage
    make_c_class_header.py >path/vscp_class.h

----


### make_c_type_header.py
Make vscp_type.h header file.

#### Usage
    make_c_type_header.py >path/vscp_ctype.h

----

### make_python_class_header.py
Make the vscp_class.py header file.

#### Usage
    make_python_class_header.py >path/vscp_class.py

----


### make_python_type_header.py
Make vscp_type.py header file.

#### Usage
    make_python_type_header.py >path/vscp_type.py

----

### make_vscphelper_hashclass.py
Make m_hashclass definitions for vscphelper.cpp.

#### Usage
     make_vscphelper_hashclass.py >path/vscp_ctype.h

----


### make_vscphelper_hashtype.py
Make m_hashtype definitions for vscphelper.cpp.

#### Usage
    make_vscphelper_hashtype.py path/vscp_hash_type.h

----


### make_sqlite_db.py
Generate sql for creation of sqlite db.

#### Usage
    make_sqlite_db.py path/dbfile.sql

----


### make_mysql_db.py
Generate sql for creation of mysql db.

#### Usage
    make_mysql_db.py path/dbfile.sql

----


### make_json.py
Make JSON/JSONP data. Use arg "jsonp" for JSONP.

#### Usage
    make_json.py >path/events.json
    or
    make_json.py jsonp >path/events.jsonp

----



### make_xml.py
Make XML data.

#### Usage
     make_xml.py >path/events.xml

----


### make_docs_sidebar.py
Make sidebar content for specification document.

#### Usage
     make_docs_sidebar.py >path/sidebar.md

----


### make_docs.py
Generate documentation for specification document.

#### Usage
    make_docs.py -v -o <output-folder> -h
    ---------------------------------------------
    -h/--help    - This text.
    -v/--verbose - Print output also to screen.
    -o/--outdir  - Folder to write output files to.
                   defaults to current folder.

----

### make_js_class_constants.py
Make class constants for the Javascript library.

#### Usage
    make_js_class_constants.py >path/output

----


### make_js_type_constants.py
Make type constants for the Javascript library.

#### Usage
    make_js_type_constants.py >path/output

----

### make_nodejs_class_constants.py
Make class constants module for node.js.

#### Usage
    make_nodejs_class_constants.py >path/output

----


### make_nodejs_type_constants.py
Make type constants module for the node.js.

#### Usage
    make_nodejs_type_constants.py >path/output


### xml2json.py
Convert XML file to JSON

#### Usage
    _xmltojson.py ../classes/../classes/class_10_measurement.xml >outfile.json

* -v - Verbose
* -h - Help

In Python one can now use statements like the following to access information

```python
# - Class token
print( o['class']['@token'])

# - All types
print( o['class']['type'])

# - Name for Type=6
print( o['class']['type'][6]
['@name'])

# - Unit =  Degrees celsius
print( o['class']['type'][6]['units']['unit'][1])  

# - # UTF8 symbol for degrees celsius
print( o['class']['type'][6]
['units']['unit'][1]['@symbol-utf8'])  

# - Conversion formula to unit = 0
print( o['class']['type'][6]['units']['unit'][1]['@conversion'])
```

for conversions a mustache template is used where {{val}} is the floating point value.

etc..

----

### dowork.sh
This is an internal bash script that is used on our internal development system to generate files for different projects and site.

#### Usage
    dowork.sh <ftp-server> <user> <password>

----

### Format

It is possible to specify how user level software should render the data part of an event. It is possible to define many renderings but one is always available for VSCP Works. A typical event definition looks like this

```xml
<type  id="51"
    name="Request new security token"
    token="VSCP_TYPE_CONTROL_REQUEST_SECURITY_TOKEN" >
    <render>
        <vscpworks 
            variables="  
                opt: function() { return e.vscpData[0]; },
                zone: function() { return e.vscpData[1]; },
                subzone: function() { return e.vscpData[2]; },
            "
            template="     
                {{lbl-start}}Opt : {{lbl-end}} {{val-start}}{{opt}}{{val-end}}{{newline}}               
                {{lbl-start}}Zone : {{lbl-end}} {{val-start}}{{zone}}{{val-end}}{{newline}}
                {{lbl-start}}Subzone : {{lbl-end}} {{val-start}}{{subzone}}{{val-end}}{{newline}}
                {{newline}}
            "
        />
    </render>
</type>
```
The rendering for VSCP Works is defined here. Each rendering definition consist of two parts. 

The first part is a variable substitution and define part that have access to the current event as the object *e* and therefore all it's data. As a variable also can be defined as a function you can assign values using functions which do calculations on the dynamic data that is provided by the environnement. A function here has access to standard Javascript functionality and the node-vscp package functionality or similar.

The second part is the actual rendering on mustache format. A defined variable should be written as {{variablename}} and will be substituted with the variable as of above.

There are some special substitution's available


| Expression | Will be replaced with |
| ---------- | --------------------- |
| __{{lbl-start}}__ | Start of label (set to bold/color...) |
| __{{lbl-end}}__ | End of label (Restet bold/color...) |
| __{{val-start}}__ | Start of value (set to bold/color...) |
| __{{val-end}}__ | End of value (Restet bold/color...) | 
| __{{newline}}__ | New line |
| __{{ident}}__ | Default ident (what is default is defined by application) |
| __{{unit}}__ | Unit as numerical (if defined) |
| __{{unitstr}}__ | Unit name |
| __{{unit_description}}__ | Unit description |
| __{{unit_comment}}__  | Unit comment |
| __{{unit_ascii}}__  |  Unit in ASCII. Use if the environment cant handel Unicode.  |
| __{{unit_utf8}}__  | Unit in UTF8. Use in Unicode aware environments. |

This is another example of variable definitions

```json
variables="
   crc8:             : function() { return e.vscpData[0]; }
   time_epoch        : function() { return e.vscpData[1]&lt;&lt;24 +
   				         e.vscpData[2]&lt;&lt;16 +
   				         e.vscpData[3]&lt;&lt;8 +
   				         e.vscpData[4]] }
"
```

and another

```json
variables="  
                    opt: function() { return e.vscpData[0]; },
                    zone: function() { return e.vscpData[1]; },
                    subzone: function() { return e.vscpData[2]; },
                    password: function() {
                        var rval = &quot;&quot;;
                        for ( i=3;i&lt;e.vscpData.length;i++) {
                            rval += String.fromCharCode(e.vscpData[i]);
                        }
                        return rval;
                    }
                "
```

Note that some characters has to be coded as they are reserved in XML. For completeness they are listed here

| Character | Encode as |
| :-------: | :-------: |
| < | &amp;lt;   |
| > | &amp;gt;   |
| & | &amp;amp;  |
| " | &amp;quot; |
| ' | &amp;apos; |


Technically variables are evaluated using the [math.js](https://mathjs.org/) package. The (mustache.js)[https://github.com/janl/mustache.js/] package is then used to obtain render information.

