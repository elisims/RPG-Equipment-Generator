"""
This is the status_effects module and supports all the REST actions for the
status_effects data
Migration to SQL - COMPLETE
"""

from flask import make_response, abort
from config import db
from models import StatusEffect, StatusEffectSchema
from sqlalchemy import inspect
import pymysql
import re

def read_all():
    """
    This function responds to a request for /api/status_effects
    with the complete lists of status_effects
    :return:        json string of list of status_effects
    """
    # Create the list of status_effects from our data
    status_effects = StatusEffect.query.all()

    # Serialize the data for the response
    status_effect_schema = StatusEffectSchema(many=True)
    data = status_effect_schema.dump(status_effects)
    return data

def read_status_effect_cols():
    status_effect_cols = []
    
    mapper = inspect(Owner)
    # This works, returns column key (name) and type.  Tho it is stated as VARCHAR instead of TEXT
    for column in mapper.columns:
        status_effect_cols.append({"col_name": str(column.key), "col_type": str(column.type)})

    return status_effect_cols


def read_one(status_effect_id):
    """
    This function responds to a request for /api/status_effects/{status_effect_id}
    with one matching status_effect from status_effects
    :param status_effect_id:   Id of status_effect to find
    :return:            status_effect matching id
    """
    # Get the status_effect requested
    status_effect = StatusEffect.query.filter(StatusEffect.status_effect_id == status_effect_id).one_or_none()

    # Did we find a status_effect?
    if status_effect is not None:

        # Serialize the data for the response
        status_effect_schema = StatusEffectSchema()
        data = status_effect_schema.dump(status_effect)
        return data

    # Otherwise, nope, didn't find that status_effect
    else:
        abort(
            404,
            "status_effect not found for Id: {status_effect_id}".format(status_effect_id=status_effect_id),
        )


def create(status_effect):
    """
    This function creates a new status_effect in the status_effects structure
    based on the passed in status_effect data
    :param status_effect:  status_effect to create in status_effects structure
    :return:        201 on success, 406 on status_effect exists
    """
    name = status_effect.get("name")

    existing_status_effect = (
        StatusEffect.query.filter(StatusEffect.name == name)
        .one_or_none()
    )

    # Can we insert this status_effect?
    if existing_status_effect is None:

        # Create a status_effect instance using the schema and the passed in status_effect
        schema = StatusEffectSchema()
        new_status_effect = schema.load(status_effect, session=db.session)

        # Add the status_effect to the database
        db.session.add(new_status_effect)
        db.session.commit()

        # Serialize and return the newly created status_effect in the response
        data = schema.dump(new_status_effect)

        return data, 201

    # Otherwise, nope, status_effect exists already
    else:
        abort(
            409,
            "status_effect {name} exists already".format(
                name=name
            ),
        )


def update(id, status_effect):
    """
    This function updates an existing status_effect in the status_effects structure
    Throws an error if a status_effect with the name we want to update to
    already exists in the database.
    :param id:   Id of the status_effect to update in the status_effects structure
    :param status_effect:      status_effect to update
    :return:            updated status_effect structure
    """
    # Get the status_effect requested from the db into session
    update_status_effect = StatusEffect.query.filter(
        StatusEffect.id == id
    ).one_or_none()

    # Try to find an existing status_effect with the same name as the update
    name = status_effect.get("name")
    description = status_effect.get("description")

    existing_status_effect = (
        StatusEffect.query.filter(StatusEffect.name == name)
        .one_or_none()
    )

    # Are we trying to find a status_effect that does not exist?
    if update_status_effect is None:
        abort(
            404,
            "status_effect not found for Id: {id}".format(id=id),
        )

    # Would our update create a duplicate of another status_effect already existing?
    elif (
        existing_status_effect is not None and existing_status_effect.id != id
    ):
        abort(
            409,
            "status_effect {name} exists already".format(
                name=name
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in status_effect into a db object
        schema = StatusEffectSchema()
        update = schema.load(status_effect, session=db.session)

        # Set the id to the status_effect we want to update
        update.id = update_status_effect.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated status_effect in the response
        data = schema.dump(update_status_effect)

        return data, 200


def delete(id):
    """
    This function deletes a status_effect from the status_effects structure
    :param id:   Id of the status_effect to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the status_effect requested
    status_effect = StatusEffect.query.filter(StatusEffect.id == id).one_or_none()

    # Did we find a status_effect?
    if status_effect is not None:
        db.session.delete(status_effect)
        db.session.commit()
        return make_response(
            "status_effect {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that status_effect
    else:
        abort(
            404,
            "status_effect not found for Id: {id}".format(id=id),
        )