"""
This is the backpacks module and supports all the REST actions for the
backpacks data
Migration to SQL - Not Complete
"""

from flask import make_response, abort
from config import db
from models import Backpack, BackpackSchema
from sqlalchemy import inspect
import pymysql
import re

def read_all():
    """
    This function responds to a request for /api/backpacks
    with the complete lists of backpacks
    :return:        json string of list of backpacks
    """
    # Create the list of backpacks from our data
    backpacks = Backpack.query.all()

    # Serialize the data for the response
    backpack_schema = BackpackSchema(many=True)
    data = backpack_schema.dump(backpacks)
    return data

def read_backpack_cols():
    backpack_cols = []
    mapper = inspect(Backpack)

    for column in mapper.columns:
        backpack_cols.append({"col_name": str(column.key), "col_type": str(column.type)})
    
    return backpack_cols


def read_one(backpack_id):
    """
    This function responds to a request for /api/backpacks/{backpack_id}
    with one matching backpack from backpacks
    :param backpack_id:   Id of backpack to find
    :return:            backpack matching id
    """
    # Get the backpack requested
    backpack = Backpack.query.filter(Backpack.backpack_id == backpack_id).one_or_none()

    # Did we find a backpack?
    if backpack is not None:

        # Serialize the data for the response
        backpack_schema = BackpackSchema()
        data = backpack_schema.dump(backpack)
        return data

    # Otherwise, nope, didn't find that backpack
    else:
        abort(
            404,
            "Backpack not found for Id: {backpack_id}".format(backpack_id=backpack_id),
        )


def create(backpack):
    """
    This function creates a new backpack in the backpacks structure
    based on the passed in backpack data
    :param backpack:  backpack to create in backpacks structure
    :return:        201 on success, 406 on backpack exists
    """
    name = backpack.get("name")

    existing_backpack = (
        Backpack.query.filter(Backpack.name == name)
        .one_or_none()
    )

    # Can we insert this backpack?
    if existing_backpack is None:

        # Create a backpack instance using the schema and the passed in backpack
        schema = BackpackSchema()
        new_backpack = schema.load(backpack, session=db.session)

        # Add the backpack to the database
        db.session.add(new_backpack)
        db.session.commit()

        # Serialize and return the newly created backpack in the response
        data = schema.dump(new_backpack)

        return data, 201

    # Otherwise, nope, backpack exists already
    else:
        abort(
            409,
            "Backpack {name} exists already".format(
                name=name
            ),
        )


def update(id, backpack):
    """
    This function updates an existing backpack in the backpacks structure
    Throws an error if a backpack with the name we want to update to
    already exists in the database.
    :param id:   Id of the backpack to update in the backpacks structure
    :param backpack:      backpack to update
    :return:            updated backpack structure
    """
    # Get the backpack requested from the db into session
    update_backpack = Backpack.query.filter(
        Backpack.id == id
    ).one_or_none()

    # Try to find an existing backpack with the same name as the update
    name = backpack.get("name")

    existing_backpack = (
        Backpack.query.filter(Backpack.name == name)
        .one_or_none()
    )

    # Are we trying to find a backpack that does not exist?
    if update_backpack is None:
        abort(
            404,
            "Backpack not found for Id: {id}".format(id=id),
        )

    # Would our update create a duplicate of another backpack already existing?
    elif (
        existing_backpack is not None and existing_backpack.id != id
    ):
        abort(
            409,
            "Backpack {name} exists already".format(
                name=name
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in backpack into a db object
        schema = BackpackSchema()
        update = schema.load(backpack, session=db.session)

        # Set the id to the backpack we want to update
        update.id = update_backpack.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated backpack in the response
        data = schema.dump(update_backpack)

        return data, 200


def delete(id):
    """
    This function deletes a backpack from the backpacks structure
    :param id:   Id of the backpack to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the backpack requested
    backpack = Backpack.query.filter(Backpack.id == id).one_or_none()

    # Did we find a backpack?
    if backpack is not None:
        db.session.delete(backpack)
        db.session.commit()
        return make_response(
            "Backpack {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that backpack
    else:
        abort(
            404,
            "Backpack not found for Id: {id}".format(id=id),
        )