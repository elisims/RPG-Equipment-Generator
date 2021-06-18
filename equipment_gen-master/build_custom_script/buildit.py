import sys
import os
import sqlite3

"""
A list of parameters used in modeling this
    ModelName,          e.g. DamageTypes
    singular,           e.g. damage_type 
    plural,             e.g. damage_types - should match db table
    additional_params,  e.g. name = db.Column(db.String(32)) - Name and String(32) will be 
                                                                replaced depending on type
    title,              e.g. Damage Types - Title of the webpage
    page_description    e.g. "A few words to describe this" - The description of the webpage
"""

def table_exists(table):
    print("Checking for", table, "in database")
    conn = sqlite3.connect('../db/equipment.db')
    c = conn.cursor()
    # Get the count of tables with the name
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=? ", (table,))
    # If the count is 1, then table exists
    if c.fetchone()[0]==1: 
        print("Found")
        return True
    else:
        print("Not found")
        return False
                
    # Commit the changes to db			
    conn.commit()
    # Close the connection
    conn.close()

def get_row_type(param_name, table):
    print("Checking type of",param_name,"in", table)
    conn = sqlite3.connect('../db/equipment.db')
    c = conn.cursor()
    try:
        c.execute("SELECT %s FROM %s" % (param_name, table))
        print("Found")

        c.execute('PRAGMA TABLE_INFO(%s)' % (table))
        s = c.fetchall()
        # print("columns:",s)
        for i in s:
            # print(i[1], i[2])
            # x = {"col_name": i[1], "col_type": i[2]}
            if i[1] == param_name:
                print(i[1], i[2])
                return i[2]
        
        return null
    except:
        print("Not found")
        return False

def param_exists(param_name, table):
    print("Check if",param_name,"Exists in", table)
    conn = sqlite3.connect('../db/equipment.db')
    c = conn.cursor()
    try:
        c.execute("SELECT %s FROM %s" % (param_name, table))
        print("Found")
        return True
    except:
        print("Not found")
        return False
        

def gen_param(param_name, param_type, max="64"):
    string = ""
    if max == "":
        max = "64"
    if param_type == "str":
        string = param_name + " = db.Column(db.String("+max+"))"
    elif param_type == "int":
        string = param_name + " = db.Column(db.Integer)"
    elif param_type == "float":
        string = param_name + " = db.Column(db.Float)"
    return string
"""
    hands = db.Column(db.Integer)
    base_hit_chance = db.Column(db.Float)
    description = db.Column(db.String(64))
"""
table_exists("booga")
param_exists("name","cultures")
get_row_type("id","cultures")
ModelName = ""
singular = ""
plural = ""
additional_params = []
title = ""
page_description = ""

# Ask the user for inputs as listed above
    # For plural, make sure table exists
    # For additional_params (if any) make sure the value
    #  exists in the table, and if String, make sure given
    #  maximum is valid
print("Starting file-creator")
while True:
    plural = input("What is the table name?\n>")
    if table_exists(plural):
        break
    else:
        print("Table does not exist in database, please enter an existing table:")
        continue

# # Check table valid here #
singular = input("What is the singular version of the table name?\n>")
ModelName = input("What should the model name be? Use the format: ModelName\n>")
title = input("What is the webpage's title?\n>")
page_description = input("What is the description of the page?\n>")


more_params = True
print("\nBesides id, name, and description")
while more_params:
    user_in = input("Are there additional parameters in the table?\n(y/n)>")
    if user_in.upper() == "Y":
        more_params = True
    elif user_in.upper() == "N":
        more_params = False
        break
    else:
        print("Invalid input")
        continue
    
    while True:
        param = input("Please enter the parameter name\nname:>")
        param_type = input("What type is it? \n(str, int, float):>")
        param_max = input("What is the maximum for this value?\n(Default 64):>")
        new_param = gen_param(param, param_type, param_max)
        if new_param == "":
            print("Invalid inputs, please try again")
            continue
        else:
            additional_params.append(new_param)
            break

print("Additional parameters:", additional_params)

# List of files to modify

# Duplicate these files with [plural].* as name

# Place files in folder called [singular]

# For each duplicated file in [singular] folder replace the following: