"""
This is the damage_types module and supports all the REST actions for the
damage_types data
Migration to SQL - COMPLETE
"""

from flask import make_response, abort
from config import db
from models import DamageType, DamageTypeSchema
from sqlalchemy import inspect
import pymysql
import re

def read_all():
    """
    This function responds to a request for /api/damage_types
    with the complete lists of damage_types
    :return:        json string of list of damage_types
    """
    # Create the list of damage_types from our data
    damage_types = DamageType.query.all()

    # Serialize the data for the response
    damage_type_schema = DamageTypeSchema(many=True)
    data = damage_type_schema.dump(damage_types)
    return data

def read_damage_types_cols():
    # Returns the columns and their types of the damage types table
    damage_type_cols = []
    mapper = inspect(DamageType)

    for column in mapper.columns:
        damage_type_cols.append({"col_name": str(column.key), "col_type": str(column.type)})
    
    return damage_type_cols

def read_one(damage_type_id):
    """
    This function responds to a request for /api/damage_types/{damage_type_id}
    with one matching damage_type from damage_types
    :param damage_type_id:   Id of damage_type to find
    :return:            damage_type matching id
    """
    # Get the damage_type requested
    damage_type = DamageType.query.filter(DamageType.damage_type_id == damage_type_id).one_or_none()

    # Did we find a damage_type?
    if damage_type is not None:

        # Serialize the data for the response
        damage_type_schema = DamageTypeSchema()
        data = damage_type_schema.dump(damage_type)
        return data

    # Otherwise, nope, didn't find that damage_type
    else:
        abort(
            404,
            "DamageType not found for Id: {damage_type_id}".format(damage_type_id=damage_type_id),
        )


def create(damage_type):
    """
    This function creates a new damage_type in the damage_types structure
    based on the passed in damage_type data
    :param damage_type:  damage_type to create in damage_types structure
    :return:        201 on success, 406 on damage_type exists
    """
    name = damage_type.get("name")

    existing_damage_type = (
        DamageType.query.filter(DamageType.name == name)
        .one_or_none()
    )

    # Can we insert this damage_type?
    if existing_damage_type is None:

        # Create a damage_type instance using the schema and the passed in damage_type
        schema = DamageTypeSchema()
        new_damage_type = schema.load(damage_type, session=db.session)

        # Add the damage_type to the database
        db.session.add(new_damage_type)
        db.session.commit()

        # Serialize and return the newly created damage_type in the response
        data = schema.dump(new_damage_type)

        return data, 201

    # Otherwise, nope, damage_type exists already
    else:
        abort(
            409,
            "DamageType {name} exists already".format(
                name=name
            ),
        )


def update(id, damage_type):
    """
    This function updates an existing damage_type in the damage_types structure
    Throws an error if a damage_type with the name we want to update to
    already exists in the database.
    :param id:   Id of the damage_type to update in the damage_types structure
    :param damage_type:      damage_type to update
    :return:            updated damage_type structure
    """
    # Get the damage_type requested from the db into session
    update_damage_type = DamageType.query.filter(
        DamageType.id == id
    ).one_or_none()

    # Try to find an existing damage_type with the same name as the update
    name = damage_type.get("name")
    description = damage_type.get("description")

    existing_damage_type = (
        DamageType.query.filter(DamageType.name == name)
        .one_or_none()
    )

    # Are we trying to find a damage_type that does not exist?
    if update_damage_type is None:
        abort(
            404,
            "DamageType not found for Id: {id}".format(id=id),
        )

    # Would our update create a duplicate of another damage_type already existing?
    elif (
        existing_damage_type is not None and existing_damage_type.id != id
    ):
        abort(
            409,
            "DamageType {name} exists already".format(
                name=name
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in damage_type into a db object
        schema = DamageTypeSchema()
        update = schema.load(damage_type, session=db.session)

        # Set the id to the damage_type we want to update
        update.id = update_damage_type.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated damage_type in the response
        data = schema.dump(update_damage_type)

        return data, 200


def delete(id):
    """
    This function deletes a damage_type from the damage_types structure
    :param id:   Id of the damage_type to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the damage_type requested
    damage_type = DamageType.query.filter(DamageType.id == id).one_or_none()

    # Did we find a damage_type?
    if damage_type is not None:
        db.session.delete(damage_type)
        db.session.commit()
        return make_response(
            "DamageType {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that damage_type
    else:
        abort(
            404,
            "DamageType not found for Id: {id}".format(id=id),
        )