"""
This is the armor_types module and supports all the REST actions for the
armor_types data
Migration to SQL - Not Complete
"""

from flask import make_response, abort
from config import db
from models import ArmorType, ArmorTypeSchema
from sqlalchemy import inspect
import pymysql
import re

def read_all():
    """
    This function responds to a request for /api/armor_types
    with the complete lists of armor_types
    :return:        json string of list of armor_types
    """
    # Create the list of armor_types from our data
    armor_types = ArmorType.query.all()

    # Serialize the data for the response
    armor_type_schema = ArmorTypeSchema(many=True)
    data = armor_type_schema.dump(armor_types)
    return data

def read_armor_type_cols():
    armor_type_cols = []
    mapper = inspect(ArmorType)

    for column in mapper.columns:
        armor_type_cols.append({"col_name": str(column.key), "col_type": str(column.type)})
    
    return armor_type_cols


def read_one(armor_type_id):
    """
    This function responds to a request for /api/armor_types/{armor_type_id}
    with one matching armor_type from armor_types
    :param armor_type_id:   Id of armor_type to find
    :return:            armor_type matching id
    """
    # Get the armor_type requested
    armor_type = ArmorType.query.filter(ArmorType.armor_type_id == armor_type_id).one_or_none()

    # Did we find a armor_type?
    if armor_type is not None:

        # Serialize the data for the response
        armor_type_schema = ArmorTypeSchema()
        data = armor_type_schema.dump(armor_type)
        return data

    # Otherwise, nope, didn't find that armor_type
    else:
        abort(
            404,
            "ArmorType not found for Id: {armor_type_id}".format(armor_type_id=armor_type_id),
        )


def create(armor_type):
    """
    This function creates a new armor_type in the armor_types structure
    based on the passed in armor_type data
    :param armor_type:  armor_type to create in armor_types structure
    :return:        201 on success, 406 on armor_type exists
    """
    name = armor_type.get("name")

    existing_armor_type = (
        ArmorType.query.filter(ArmorType.name == name)
        .one_or_none()
    )

    # Can we insert this armor_type?
    if existing_armor_type is None:

        # Create a armor_type instance using the schema and the passed in armor_type
        schema = ArmorTypeSchema()
        new_armor_type = schema.load(armor_type, session=db.session)

        # Add the armor_type to the database
        db.session.add(new_armor_type)
        db.session.commit()

        # Serialize and return the newly created armor_type in the response
        data = schema.dump(new_armor_type)

        return data, 201

    # Otherwise, nope, armor_type exists already
    else:
        abort(
            409,
            "ArmorType {name} exists already".format(
                name=name
            ),
        )


def update(id, armor_type):
    """
    This function updates an existing armor_type in the armor_types structure
    Throws an error if a armor_type with the name we want to update to
    already exists in the database.
    :param id:   Id of the armor_type to update in the armor_types structure
    :param armor_type:      armor_type to update
    :return:            updated armor_type structure
    """
    # Get the armor_type requested from the db into session
    update_armor_type = ArmorType.query.filter(
        ArmorType.id == id
    ).one_or_none()

    # Try to find an existing armor_type with the same name as the update
    name = armor_type.get("name")

    existing_armor_type = (
        ArmorType.query.filter(ArmorType.name == name)
        .one_or_none()
    )

    # Are we trying to find a armor_type that does not exist?
    if update_armor_type is None:
        abort(
            404,
            "ArmorType not found for Id: {id}".format(id=id),
        )

    # Would our update create a duplicate of another armor_type already existing?
    elif (
        existing_armor_type is not None and existing_armor_type.id != id
    ):
        abort(
            409,
            "ArmorType {name} exists already".format(
                name=name
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in armor_type into a db object
        schema = ArmorTypeSchema()
        update = schema.load(armor_type, session=db.session)

        # Set the id to the armor_type we want to update
        update.id = update_armor_type.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated armor_type in the response
        data = schema.dump(update_armor_type)

        return data, 200


def delete(id):
    """
    This function deletes a armor_type from the armor_types structure
    :param id:   Id of the armor_type to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the armor_type requested
    armor_type = ArmorType.query.filter(ArmorType.id == id).one_or_none()

    # Did we find a armor_type?
    if armor_type is not None:
        db.session.delete(armor_type)
        db.session.commit()
        return make_response(
            "ArmorType {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that armor_type
    else:
        abort(
            404,
            "ArmorType not found for Id: {id}".format(id=id),
        )