#
# VSCP (Very Simple Control Protocol)
# http://www.vscp.org
#
# The MIT License (MIT)
#
# Copyright © 2000-2020 Ake Hedman,
# Grodans Paradis AB <info@grodansparadis.com>
#
# Make records for the sqlite3 database
#

import sys
import glob
# https://docs.python.org/3/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET
import time
import datetime

xclass = {}
order_list = []  # class list order
class_list = []  # List with class attributes
type_list = []  # List with type attributes

print(" ")
print("--              !!!!!!!!!!!!!!!!!!!!  W A R N I N G  !!!!!!!!!!!!!!!!!!!!")
print("--                             This file is auto-generated")
print("--                  see https://github.com/grodansparadis/vscp-classes")
print("--                          Generated:", datetime.datetime.now())
print(" ")

# Create class table
with open('../sqlite/create_class_table.sql', 'r') as myfile:
    data = myfile.read()
print(data, ";")
print(" ")

# Create type table
with open('../sqlite/create_type_table.sql', 'r') as myfile:
    data = myfile.read()
print(data, ";")
print(" ")

# Create unit table
with open('../sqlite/create_unit_table.sql', 'r') as myfile:
    data = myfile.read()
print(data, ";")
print(" ")

# Read classes list to get list order
class_tree = ET.parse('../classes/list_class.xml')
class_root = class_tree.getroot()
for child in class_root.iter('item'):
    order_list.append(child.attrib['name'])

if len(order_list) == 0:
    print("No classes defined in class list!")
    sys.exit()

# Fill class table with data

for vscp_class in order_list:
    fname = '../classes/' + vscp_class
    type_tree = ET.parse(fname)
    type_root = type_tree.getroot()

    outstr = "INSERT INTO vscp_class (class,name,token,description) VALUES (" + \
        type_root.attrib["id"] + "," + \
        "'" + type_root.attrib["name"] + "'," + \
        "'" + type_root.attrib["token"] + "'"

    # Get description
    description = ""
    with open('../classes/' + type_root.attrib["id"] + '.md', 'r') as myfile:
        description = myfile.read()
        description = description.replace("'", "''")
        description = description.replace("\n", "\\n")
        description = description.replace("\r", "\\r")
        description = description.replace("\t", "\\t")

    outstr += ",'" + description + "');"

    print(outstr)

# Fill in type table data

for vscp_class in order_list:
    fname = '../classes/' + vscp_class
    type_tree = ET.parse(fname)
    type_root = type_tree.getroot()

    events = ""
    try:
        events = type_root.attrib["events"]
    except:
        # 'events' tag does not exist
        for child in type_root.iter('type'):

            outstr = "INSERT INTO vscp_type (type,link_to_class,token,description) VALUES (" + \
                child.attrib["id"] + "," + \
                type_root.attrib["id"] + "," + \
                "'" + type_root.attrib["token"] + "'"

            # Get description
            description = ""
            with open('../classes/' + type_root.attrib["id"] + "." + child.attrib["id"] + '.md', 'r') as myfile:
                description = myfile.read()
                description = description.replace("'", "''")
                description = description.replace("\n", "\\n")
                description = description.replace("\r", "\\r")
                description = description.replace("\t", "\\t")

            outstr += ",'" + description + "');"
            print(outstr)
    else:
        classid = type_root.attrib["id"]
        fname = '../classes/' + events
        type_tree = ET.parse(fname)
        type_root = type_tree.getroot()

        for child in type_root.iter('type'):

            outstr = "INSERT INTO vscp_type (type,link_to_class,token,description) VALUES (" + \
                child.attrib["id"] + "," + \
                classid + "," + \
                "'" + child.attrib["token"] + "'"

            # Get description
            description = ""
            with open('../classes/' + type_root.attrib["id"] + "." + child.attrib["id"] + '.md', 'r') as myfile:
                description = myfile.read()
                description = description.replace("'", "''")
                description = description.replace("\n", "\\n")
                description = description.replace("\r", "\\r")
                description = description.replace("\t", "\\t")

            outstr += ",'" + description + "');"
            print(outstr)

print(" ")

for vscp_class in order_list:

    fname = '../classes/' + vscp_class
    type_tree = ET.parse(fname)
    type_root = type_tree.getroot()

    events = ""
    try:
        events = type_root.attrib["events"]
    except:
        # 'events' tag does not exist
        for child in type_root.iter('type'):
            classid = int(type_root.attrib["id"])
            if (10 == classid or
                60 == classid or
                65 == classid or
                70 == classid or
                85 == classid or
                1040 == classid or
                    1060 == classid):

                for unit in child.iter('unit'):

                    try:
                        conversion = unit.attrib["conversion"]
                    except:
                        conversion = "val"
                    outstr = "INSERT INTO vscp_unit (link_to_class,link_to_type,nunit,name,description,conversion) VALUES (" + \
                        type_root.attrib["id"] + "," + \
                        child.attrib["id"] + "," + \
                        unit.attrib["id"] + "," + \
                        "'" + unit.attrib["name"] + "'," + \
                        "'" + unit.attrib["description"] + "'," + \
                        "'" + conversion + "');"
                    print(outstr)
    else:
        classid = type_root.attrib["id"]
        fname = '../classes/' + events
        type_tree = ET.parse(fname)
        type_root = type_tree.getroot()

        for child in type_root.iter('type'):
            classid = type_root.attrib["id"]
            if (10 == classid or
                60 == classid or
                65 == classid or
                70 == classid or
                85 == classid or
                1040 == classid or
                    1060 == classid):
                for unit in child.iter('unit'):
                    try:
                        conversion = unit.attrib["conversion"]
                    except:
                        conversion = "val"
                    outstr = "INSERT INTO vscp_unit (link_to_class,link_to_type,nunit,name,description,conversion) VALUES (" + \
                        classid + "," + \
                        child.attrib["id"] + "," + \
                        unit.attrib["id"] + "," + \
                        "'" + unit.attrib["name"] + "'," + \
                        "'" + unit.attrib["description"] + "'," + \
                        "'" + conversion + "');"
                    print(outstr)

print(" ")
