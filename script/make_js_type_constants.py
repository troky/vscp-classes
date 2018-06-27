#
# VSCP (Very Simple Control Protocol)
# http://www.vscp.org
#
# The MIT License (MIT)
#
# Copyright (c) 2000-2018 Ake Hedman, Grodans Paradis AB <info@grodansparadis.com>
#
# Make c header for VSCP type definitions
#

import sys
import glob
# https://docs.python.org/3/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET

xclass = {}
order_list = [] # class list order
class_list = [] # List with class attributes
type_list = []  # List with type attributes

with open('../classes/list_class.xml', 'r') as myfile:
  data = myfile.read()

# Read classes list to get list order
class_tree = ET.parse('../classes/list_class.xml')
class_root = class_tree.getroot()
for child in class_root.iter('item'):
    order_list.append( child.attrib['name'] )

if len(order_list) == 0:
    print "No classes defined in class list!"
    sys.exit() 

print "vscp.constants.types = {\n"
print "    VSCP_TYPE_UNDEFINED: 0,\n"

for vscp_class in order_list:
    fname = '../classes/' + vscp_class
    type_tree = ET.parse(fname)
    type_root = type_tree.getroot()
    
    print "// ", type_root.attrib["token"],\
        "=",type_root.attrib["id"],\
        " - ",type_root.attrib["name"]
    events = ""
    try:
        events = type_root.attrib["events"]
    except:
        for child in type_root.iter('type'):
            print "    " + child.attrib["token"] + ": " +\
                        child.attrib["id"] + ","
    else:    
        fname = '../classes/' + events
        type_tree = ET.parse(fname)
        type_root = type_tree.getroot()
        print "// Event types is the same as ", \
                type_root.attrib["token"],"=",type_root.attrib["id"], \
                " - ",type_root.attrib["name"]
    print

print "};"
