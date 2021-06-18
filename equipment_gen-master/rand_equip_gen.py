# Generate random equipment
import random
from config import db
from sqlalchemy import inspect
from  sqlalchemy.sql.expression import func, select
from sqlalchemy.sql import exists
from models import *
import pymysql
import re
import json


# return_random_item is called by outside functions
def return_random_item(item_type=None):

    
    slot = {"id":2,"name":"chest"} # Arbitrary slot to define slot variable
    # base_armor = 1
    if not item_type:
        item_type=random.choice(["armor","weapon"])
        # print("Random choice:", item_type)
    
    ret_item = {}
    ret_item['item_type'] = item_type

    # Generate random armor
    if item_type=="armor":
        # If the item_type is "armor", pick a slot
        # slots are pulled from DB armor_slots and there
        # are two weapon slots (two 1h or one 2h)
        slot = {"id":2,"name":"chest"}      # "Random" slot - Do more here later
        tf = None
        attempts = 20 #
        # Loop to check if there are any armor types that are associated with 
        # a randomly chosen slot
        rand_slot = None
        while not tf and attempts > 0:
            # pick a random slot from the armor_slots table
            rand_slot = ArmorSlot.query.order_by(func.rand()).first()

            # 
            q = ArmorSlot.query\
                .filter(exists().where(BaseArmor.slot==rand_slot.id)).first()
            try:
                tf = q.id
            except:
                tf = None
            # print("TF:",tf)
            # print("rand_slot:", rand_slot.name)
            # print("Attempts:",attempts)
            attempts = attempts - 1

        # if yes - store the chosen slot as the variable
        
        if not tf:
            print("Failed in 20 attempts, try again later")
            return {}

        slot['id'] = rand_slot.id
        slot['name'] = rand_slot.name

    
        # print("SLOT ID:",slot['id'])
        slot_id = slot['id']
        # ret_item['slot_id'] = slot_id
        # If it's armor, pick  base_armor whose armor 
        # slot has the given slot above.
        q = BaseArmor.query.filter(BaseArmor.slot==slot_id).order_by(func.rand()).first()
        if q  == None:
            # print("No Base armor found in database")
            return {}
        # print("Base_armor id:",q.id)
        ret_item['base_armor_id'] = q.id

        # Generate the unique_armor from the base_armor:
            # Does it have an owner? if yes, set the owner and culture
        has_owner = bool(random.getrandbits(1))
        # print("Has Owner?", has_owner)
        if has_owner:
            owner_query = Owner.query.order_by(func.rand()).first()
            if owner_query == None:
                # print("No owners in db, skipping")
                ret_item['culture_id'] = None
                ret_item['owner_id'] = None
            else:
                # print("Owner id chosen:", owner_query.id)
                ret_item['owner_id'] = owner_query.id
                # Get culture associated with owner
                # print("Owner culture id:", owner_query.culture)
                ret_item['culture_id'] = owner_query.culture
            # Else does it have a culture? if yes choose rand culture
        else:
            ret_item['owner_id'] = None
            has_culture = bool(random.getrandbits(1))
            # print("Has Culture?", has_culture)
            if has_culture:
                culture_query = Culture.query.order_by(func.rand()).first()
                if culture_query == None:
                    # print("No cultures in db, skipping")
                    ret_item['culture_id'] = None
                else:
                    # print("Culture id chosen:", culture_query.id)
                    ret_item['culture_id'] = culture_query.id
            else:
                ret_item['culture_id'] = None

        # Has nickname? Generate nickname
        has_nickname = bool(random.getrandbits(1))
        # print("Has nickname?", has_nickname)
        if has_nickname:
            nickname_query = Nickname.query.order_by(func.rand()).first()
            if nickname_query == None:
                # print("No nicknames in db, skipping")
                ret_item['nickname'] = None
            else:
                # print("Nickname name chosen:", nickname_query.name)
                ret_item['nickname'] = nickname_query.name
        else:
            ret_item['nickname'] = None
        
        # Generate a description
        description = "A custom description.  We'll do this later"
        # print("Description:", description)
        ret_item['description'] = description
        # choose a level
        level = random.randrange(50)
        # print("Level:", level)
        ret_item['level'] = level
        # increase defense by 0-100% (convert to int)
        def_increase = random.randrange(100)
        # print("Increased defense by", def_increase)
        ret_item['added_defense'] = def_increase
    
    # Generate weapon
    else:
        # print("Generating Weapon")

        # If it's weapon, pick  base_weapon 
        q = BaseWeapon.query.order_by(func.rand()).first()
        if q  == None:
            # print("No weapon bases found! Exiting")
            return {}

        # print("Base_weapon id:",q.id)
        ret_item['base_weapon_id'] = q.id

        # Generate the unique_weapon from the base_weapon:
            # Does it have an owner? if yes, set the owner and culture
        has_owner = bool(random.getrandbits(1))
        # print("Has Owner?", has_owner)
        if has_owner:
            owner_query = Owner.query.order_by(func.rand()).first()
            if owner_query == None:
                # print("No owners in db, skipping")
                ret_item['culture_id'] = None
                ret_item['owner_id'] = None
            else:
                # print("Owner id chosen:", owner_query.id)
                ret_item['owner_id'] = owner_query.id
                # Get culture associated with owner
                # print("Owner culture id:", owner_query.culture)
                ret_item['culture_id'] = owner_query.culture
            # Else does it have a culture? if yes choose rand culture
        else:
            ret_item['owner_id'] = None
            has_culture = bool(random.getrandbits(1))
            # print("Has Culture?", has_culture)
            if has_culture:
                culture_query = Culture.query.order_by(func.rand()).first()
                if culture_query == None:
                    # print("No cultures in db, skipping")
                    ret_item['culture_id'] = None
                else:
                    # print("Culture id chosen:", culture_query.id)
                    ret_item['culture_id'] = culture_query.id
            else:
                ret_item['culture_id'] = None
        
        # Has element type? Generate element type
        has_element = bool(random.getrandbits(1))
        # print("Has Element?", has_element)
        if has_element:
            element_query = ElementType.query.order_by(func.rand()).first()
            if element_query == None:
                # print("No elements in db, skipping")
                ret_item['element_id'] = None
            else:
                # print("Element id chosen:", element_query.id)
                # Get status effect associated with element
                # print("Element status effect id:", element_query.status_effect)
                ret_item['element_id'] = element_query.id
        else:
            ret_item['element_id'] = None

        # Has nickname? Generate nickname
        has_nickname = bool(random.getrandbits(1))
        # print("Has nickname?", has_nickname)
        if has_nickname:
            nickname_query = Nickname.query.order_by(func.rand()).first()
            if nickname_query == None:
                # print("No nicknames in db, skipping")
                ret_item['nickname'] = None
            else:
                # print("Nickname name chosen:", nickname_query.name)
                ret_item['nickname'] = nickname_query.name
        else:
            ret_item['nickname'] = None
        # Generate a description
        description = "A custom description.  We'll do this later"
        # print("Description:", description)
        ret_item['description'] = description
        # choose a level
        level = random.randrange(50)
        # print("Level:", level)
        ret_item['level'] = level
        # increase damage by 0-100% (convert to int)
        damage_increase = random.randrange(100)
        # print("Increased damage by", damage_increase)
        ret_item['added_damage'] = damage_increase
    
    # print("ret_item:", ret_item)
    return ret_item

# print(return_random_item())