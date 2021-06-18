"""
This is the loadouts module and supports all the REST actions for the
loadouts data
Migration to SQL - Not Complete
"""

from flask import make_response, abort
from config import db
from models import Loadout, LoadoutSchema
from sqlalchemy import inspect
import pymysql
import re

def read_all():
    """
    This function responds to a request for /api/loadouts
    with the complete lists of loadouts
    :return:        json string of list of loadouts
    """
    # Create the list of loadouts from our data
    loadouts = Loadout.query.all()

    # Serialize the data for the response
    loadout_schema = LoadoutSchema(many=True)
    data = loadout_schema.dump(loadouts)
    return data

def read_loadout_cols():
    loadout_cols = []
    mapper = inspect(Loadout)

    for column in mapper.columns:
        loadout_cols.append({"col_name": str(column.key), "col_type": str(column.type)})
    
    return loadout_cols


def read_one(loadout_id):
    """
    This function responds to a request for /api/loadouts/{loadout_id}
    with one matching loadout from loadouts
    :param loadout_id:   Id of loadout to find
    :return:            loadout matching id
    """
    # Get the loadout requested
    loadout = Loadout.query.filter(Loadout.loadout_id == loadout_id).one_or_none()

    # Did we find a loadout?
    if loadout is not None:

        # Serialize the data for the response
        loadout_schema = LoadoutSchema()
        data = loadout_schema.dump(loadout)
        return data

    # Otherwise, nope, didn't find that loadout
    else:
        abort(
            404,
            "Loadout not found for Id: {loadout_id}".format(loadout_id=loadout_id),
        )


def create(loadout):
    """
    This function creates a new loadout in the loadouts structure
    based on the passed in loadout data
    :param loadout:  loadout to create in loadouts structure
    :return:        201 on success, 406 on loadout exists
    """
    name = loadout.get("name")

    existing_loadout = (
        Loadout.query.filter(Loadout.name == name)
        .one_or_none()
    )

    # Can we insert this loadout?
    if existing_loadout is None:

        # Create a loadout instance using the schema and the passed in loadout
        schema = LoadoutSchema()
        new_loadout = schema.load(loadout, session=db.session)

        # Add the loadout to the database
        db.session.add(new_loadout)
        db.session.commit()

        # Serialize and return the newly created loadout in the response
        data = schema.dump(new_loadout)

        return data, 201

    # Otherwise, nope, loadout exists already
    else:
        abort(
            409,
            "Loadout {name} exists already".format(
                name=name
            ),
        )


def update(id, loadout):
    """
    This function updates an existing loadout in the loadouts structure
    Throws an error if a loadout with the name we want to update to
    already exists in the database.
    :param id:   Id of the loadout to update in the loadouts structure
    :param loadout:      loadout to update
    :return:            updated loadout structure
    """
    # Get the loadout requested from the db into session
    update_loadout = Loadout.query.filter(
        Loadout.id == id
    ).one_or_none()

    # Try to find an existing loadout with the same name as the update
    name = loadout.get("name")

    existing_loadout = (
        Loadout.query.filter(Loadout.name == name)
        .one_or_none()
    )

    # Are we trying to find a loadout that does not exist?
    if update_loadout is None:
        abort(
            404,
            "Loadout not found for Id: {id}".format(id=id),
        )

    # Would our update create a duplicate of another loadout already existing?
    elif (
        existing_loadout is not None and existing_loadout.id != id
    ):
        abort(
            409,
            "Loadout {name} exists already".format(
                name=name
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in loadout into a db object
        schema = LoadoutSchema()
        update = schema.load(loadout, session=db.session)

        # Set the id to the loadout we want to update
        update.id = update_loadout.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated loadout in the response
        data = schema.dump(update_loadout)

        return data, 200


def delete(id):
    """
    This function deletes a loadout from the loadouts structure
    :param id:   Id of the loadout to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the loadout requested
    loadout = Loadout.query.filter(Loadout.id == id).one_or_none()

    # Did we find a loadout?
    if loadout is not None:
        db.session.delete(loadout)
        db.session.commit()
        return make_response(
            "Loadout {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that loadout
    else:
        abort(
            404,
            "Loadout not found for Id: {id}".format(id=id),
        )