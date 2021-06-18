"""
This is the armor_slots module and supports all the REST actions for the
armor_slots data
Migration to SQL - Not Complete
"""

from flask import make_response, abort
from config import db
from models import ArmorSlot, ArmorSlotSchema
from sqlalchemy import inspect
import pymysql
import re

def read_all():
    """
    This function responds to a request for /api/armor_slots
    with the complete lists of armor_slots
    :return:        json string of list of armor_slots
    """
    # Create the list of armor_slots from our data
    armor_slots = ArmorSlot.query.all()

    # Serialize the data for the response
    armor_slot_schema = ArmorSlotSchema(many=True)
    data = armor_slot_schema.dump(armor_slots)
    return data

def read_armor_slot_cols():
    armor_slot_cols = []
    mapper = inspect(ArmorSlot)

    for column in mapper.columns:
        armor_slot_cols.append({"col_name": str(column.key), "col_type": str(column.type)})
    
    return armor_slot_cols


def read_one(armor_slot_id):
    """
    This function responds to a request for /api/armor_slots/{armor_slot_id}
    with one matching armor_slot from armor_slots
    :param armor_slot_id:   Id of armor_slot to find
    :return:            armor_slot matching id
    """
    # Get the armor_slot requested
    armor_slot = ArmorSlot.query.filter(ArmorSlot.armor_slot_id == armor_slot_id).one_or_none()

    # Did we find a armor_slot?
    if armor_slot is not None:

        # Serialize the data for the response
        armor_slot_schema = ArmorSlotSchema()
        data = armor_slot_schema.dump(armor_slot)
        return data

    # Otherwise, nope, didn't find that armor_slot
    else:
        abort(
            404,
            "ArmorSlot not found for Id: {armor_slot_id}".format(armor_slot_id=armor_slot_id),
        )


def create(armor_slot):
    """
    This function creates a new armor_slot in the armor_slots structure
    based on the passed in armor_slot data
    :param armor_slot:  armor_slot to create in armor_slots structure
    :return:        201 on success, 406 on armor_slot exists
    """
    name = armor_slot.get("name")

    existing_armor_slot = (
        ArmorSlot.query.filter(ArmorSlot.name == name)
        .one_or_none()
    )

    # Can we insert this armor_slot?
    if existing_armor_slot is None:

        # Create a armor_slot instance using the schema and the passed in armor_slot
        schema = ArmorSlotSchema()
        new_armor_slot = schema.load(armor_slot, session=db.session)

        # Add the armor_slot to the database
        db.session.add(new_armor_slot)
        db.session.commit()

        # Serialize and return the newly created armor_slot in the response
        data = schema.dump(new_armor_slot)

        return data, 201

    # Otherwise, nope, armor_slot exists already
    else:
        abort(
            409,
            "ArmorSlot {name} exists already".format(
                name=name
            ),
        )


def update(id, armor_slot):
    """
    This function updates an existing armor_slot in the armor_slots structure
    Throws an error if a armor_slot with the name we want to update to
    already exists in the database.
    :param id:   Id of the armor_slot to update in the armor_slots structure
    :param armor_slot:      armor_slot to update
    :return:            updated armor_slot structure
    """
    # Get the armor_slot requested from the db into session
    update_armor_slot = ArmorSlot.query.filter(
        ArmorSlot.id == id
    ).one_or_none()

    # Try to find an existing armor_slot with the same name as the update
    name = armor_slot.get("name")

    existing_armor_slot = (
        ArmorSlot.query.filter(ArmorSlot.name == name)
        .one_or_none()
    )

    # Are we trying to find a armor_slot that does not exist?
    if update_armor_slot is None:
        abort(
            404,
            "ArmorSlot not found for Id: {id}".format(id=id),
        )

    # Would our update create a duplicate of another armor_slot already existing?
    elif (
        existing_armor_slot is not None and existing_armor_slot.id != id
    ):
        abort(
            409,
            "ArmorSlot {name} exists already".format(
                name=name
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in armor_slot into a db object
        schema = ArmorSlotSchema()
        update = schema.load(armor_slot, session=db.session)

        # Set the id to the armor_slot we want to update
        update.id = update_armor_slot.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated armor_slot in the response
        data = schema.dump(update_armor_slot)

        return data, 200


def delete(id):
    """
    This function deletes a armor_slot from the armor_slots structure
    :param id:   Id of the armor_slot to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the armor_slot requested
    armor_slot = ArmorSlot.query.filter(ArmorSlot.id == id).one_or_none()

    # Did we find a armor_slot?
    if armor_slot is not None:
        db.session.delete(armor_slot)
        db.session.commit()
        return make_response(
            "ArmorSlot {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that armor_slot
    else:
        abort(
            404,
            "ArmorSlot not found for Id: {id}".format(id=id),
        )