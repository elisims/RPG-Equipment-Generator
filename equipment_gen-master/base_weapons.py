"""
This is the weapons module and supports all the REST actions for the
weapons data
Migration to SQL - Not Complete
"""

from flask import make_response, abort
from config import db
from models import BaseWeapon, BaseWeaponSchema, view_BaseWeapon, view_BaseWeaponSchema


def read_all():
    """
    This function responds to a request for /api/base_weapons
    with the complete lists of base weapons
    :return:        json string of list of base weapons
    """
    # Create the list of weapons from our data
    weapons = view_BaseWeapon.query.all()

    # Serialize the data for the response
    weapon_schema = view_BaseWeaponSchema(many=True)
    data = weapon_schema.dump(weapons)
    return data

def read_weapon_cols():
    base_weapons_cols = []
    
    mapper = inspect(BaseWeapon)
    # This works, returns column key (name) and type.  Tho it is stated as VARCHAR instead of TEXT
    for column in mapper.columns:
        base_weapons_cols.append({"col_name": str(column.key), "col_type": str(column.type)})

    return base_weapons_cols

def read_one(id):
    """
    This function responds to a request for /api/weapons/{id}
    with one matching weapon from weapons
    :param id:   Id of weapon to find
    :return:            weapon matching id
    """
    # Get the weapon requested
    weapon = BaseWeapon.query.filter(BaseWeapon.id == id).one_or_none()

    # Did we find a weapon?
    if weapon is not None:
        
        # Serialize the data for the response
        weapon_schema = BaseWeaponSchema()
        data = weapon_schema.dump(weapon)
        return data

    # Otherwise, nope, didn't find that weapon
    else:
        abort(
            404,
            "Weapon not found for Id: {id}".format(id=id),
        )


def create(weapon):
    """
    This function creates a new weapon in the weapons structure
    based on the passed in weapon data
    :param weapon:  weapon to create in weapons structure
    :return:        201 on success, 406 on weapon exists
    """
    # The class name must be unique in this case.  So only 1 "Hand Axe"
    name = weapon.get("name")

    existing_weapon = (
        BaseWeapon.query.filter(BaseWeapon.name == name)
        .one_or_none()
    )

    # Can we insert this weapon?
    if existing_weapon is None:

        # Create a weapon instance using the schema and the passed in weapon
        schema = BaseWeaponSchema()
        new_weapon = schema.load(weapon, session=db.session)

        # Add the weapon to the database
        db.session.add(new_weapon)
        db.session.commit()

        # Serialize and return the newly created weapon in the response
        data = schema.dump(new_weapon)

        return data, 201

    # Otherwise, nope, weapon exists already
    else:
        abort(
            409,
            "Weapon {name} exists already".format(
                name=name
            ),
        )


def update(id, weapon):
    """
    This function updates an existing weapon in the weapons structure
    Throws an error if a weapon with the name we want to update to
    already exists in the database.
    :param id:   Id of the weapon to update in the weapons structure
    :param weapon:      weapon to update
    :return:            updated weapon structure
    """
    # Get the weapon requested from the db into session
    update_weapon = BaseWeapon.query.filter(
        BaseWeapon.id == id
    ).one_or_none()

    # Try to find an existing weapon with the same name as the update
    name = weapon.get("name")
    hands = weapon.get("hands")
    base_damage_min = weapon.get("base_damage_min")
    base_damage_max = weapon.get("base_damage_max")
    damage_type_primary = weapon.get("damage_type_primary")
    damage_type_secondary = weapon.get("damage_type_secondary")
    base_weight = weapon.get("base_weight")
    base_attacks_per_second = weapon.get("base_attacks_per_second")
    base_hit_chance = weapon.get("base_hit_chance")
    description = weapon.get("description")

    existing_weapon = (
        Weapon.query.filter(Weapon.name == name)
        .one_or_none()
    )

    # Are we trying to find a weapon that does not exist?
    if update_weapon is None:
        abort(
            404,
            "Weapon not found for Id: {id}".format(id=id),
        )

    # Would our update create a duplicate of another weapon already existing?
    elif (
        existing_weapon is not None and existing_weapon.id != id
    ):
        abort(
            409,
            "Weapon {name} exists already".format(
                name=name
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in weapon into a db object
        schema = BaseWeaponSchema()
        update = schema.load(weapon, session=db.session)

        # Set the id to the weapon we want to update
        update.id = update_weapon.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated weapon in the response
        data = schema.dump(update_weapon)

        return data, 200


def delete(id):
    """
    This function deletes a weapon from the weapons structure
    :param id:   Id of the weapon to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the weapon requested
    weapon = BaseWeapon.query.filter(BaseWeapon.id == id).one_or_none()

    # Did we find a weapon?
    if weapon is not None:
        db.session.delete(weapon)
        db.session.commit()
        return make_response(
            "Base Weapon {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that weapon
    else:
        abort(
            404,
            "Base Weapon not found for Id: {id}".format(id=id),
        )