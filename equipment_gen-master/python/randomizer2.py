# Generate random equipment
import random
from config import db
from sqlalchemy import inspect
import pymysql
import re

all_items = {}

wep_order=['owners','cultures','base_weapons','element_types']


def get_db_names():
    try:
        conn = sqlite3.connect('./db/equipment.db')
    except:
        try:
            conn = sqlite3.connect('../db/equipment.db')
        except:
            print("Could not connect to database")
            return
    c = conn.cursor()
    c.execute('SELECT name from sqlite_master where type="table"')
    s = c.fetchall()
    for i in s:
        if i[0] == 'sqlite_sequence':
            continue
        else:
            all_items[i[0]] = []
    return s
    
def populate_all_items():
    # This is temp, fix this
    try:
        conn = sqlite3.connect('./db/equipment.db')
    except:
        try:
            conn = sqlite3.connect('../db/equipment.db')
        except:
            print("Could not connect to database")
            return
    c = conn.cursor()

    for i in all_items:
        try:
            c.execute('SELECT name from %s' % (i))
            s = c.fetchall()
            for x in s:
                all_items[i].append(x[0])
        except:
            print(i,"had no values in DB, Skipping")

def single_to_plural(string):
    rx = (".*s$")
    newStr = string
    if re.match(rx, string):
        newStr = string + '\''
    else:
        newStr = string + '\'s'
    return newStr

def get_weapon_parts():
    weapon = []
    for val in order:
        # Random number in range of array
        r = random.randrange(0, len(all_items[val]))
        weapon.append(all_items[val][r])
    return weapon

def array_to_string(arr):
    string = ""
    for index, item in enumerate(arr):
        if index == 0:
            string += single_to_plural(item) + " "
        elif index == 2:
            string += item + " of "
        else:
            string += item + " "
    return string

def return_random_item():
    get_db_names()
    populate_all_items()
    weapon_arr = get_weapon_parts()
    weapon_str = array_to_string(weapon_arr)
    return weapon_str
