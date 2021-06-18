"""
This is the owners module and supports all the REST actions for the
owners data
Migration to SQL - COMPLETE
"""

from flask import make_response, abort
from config import db
from models import Owner, OwnerSchema, view_Owner, viewOwnerSchema
from sqlalchemy import inspect
import pymysql
import re


def read_all():
    """
    This function responds to a request for /api/owners
    with the complete lists of owners
    :return:        json string of list of owners
    """
    # Create the list of owners from our data
    owners = view_Owner.query.all()

    # Serialize the data for the response
    owner_schema = viewOwnerSchema(many=True)
    data = owner_schema.dump(owners)
    return data

def read_owner_cols():
    owners_cols = []
    
    mapper = inspect(Owner)
    # This works, returns column key (name) and type.  Tho it is stated as VARCHAR instead of TEXT
    for column in mapper.columns:
        owners_cols.append({"col_name": str(column.key), "col_type": str(column.type)})

    return owners_cols



def read_one(owner_id):
    """
    This function responds to a request for /api/owners/{owner_id}
    with one matching owner from owners
    :param owner_id:   Id of owner to find
    :return:            owner matching id
    """
    # Get the owner requested
    owner = view_Owner.query.filter(view_Owner.owner_id == owner_id).one_or_none()

    # Did we find a owner?
    if owner is not None:

        # Serialize the data for the response
        owner_schema = view_OwnerSchema()
        data = owner_schema.dump(owner)
        return data

    # Otherwise, nope, didn't find that owner
    else:
        abort(
            404,
            "owner not found for Id: {owner_id}".format(owner_id=owner_id),
        )


def create(owner):
    """
    This function creates a new owner in the owners structure
    based on the passed in owner data
    :param owner:  owner to create in owners structure
    :return:        201 on success, 406 on owner exists
    """
    name = owner.get("name")

    existing_owner = (
        Owner.query.filter(Owner.name == name)
        .one_or_none()
    )

    # Can we insert this owner?
    if existing_owner is None:

        # Create a owner instance using the schema and the passed in owner
        schema = OwnerSchema()
        new_owner = schema.load(owner, session=db.session)

        # Add the owner to the database
        db.session.add(new_owner)
        db.session.commit()

        # Serialize and return the newly created owner in the response
        data = schema.dump(new_owner)

        return data, 201

    # Otherwise, nope, owner exists already
    else:
        abort(
            409,
            "owner {name} exists already".format(
                name=name
            ),
        )


def update(id, owner):
    """
    This function updates an existing owner in the owners structure
    Throws an error if a owner with the name we want to update to
    already exists in the database.
    :param id:   Id of the owner to update in the owners structure
    :param owner:      owner to update
    :return:            updated owner structure
    """
    # Get the owner requested from the db into session
    update_owner = Owner.query.filter(
        Owner.id == id
    ).one_or_none()

    # Try to find an existing owner with the same name as the update
    name = owner.get("name")

    existing_owner = (
        Owner.query.filter(Owner.name == name)
        .one_or_none()
    )

    # Are we trying to find a owner that does not exist?
    if update_owner is None:
        abort(
            404,
            "owner not found for Id: {id}".format(id=id),
        )

    # Would our update create a duplicate of another owner already existing?
    elif (
        existing_owner is not None and existing_owner.id != id
    ):
        abort(
            409,
            "owner {name} exists already".format(
                name=name
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in owner into a db object
        schema = viewOwnerSchema()
        update = schema.load(owner, session=db.session)

        # Set the id to the owner we want to update
        update.id = update_owner.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated owner in the response
        data = schema.dump(update_owner)

        return data, 200


def delete(id):
    """
    This function deletes a owner from the owners structure
    :param id:   Id of the owner to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the owner requested
    owner = Owner.query.filter(Owner.id == id).one_or_none()

    # Did we find a owner?
    if owner is not None:
        db.session.delete(owner)
        db.session.commit()
        return make_response(
            "owner {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that owner
    else:
        abort(
            404,
            "owner not found for Id: {id}".format(id=id),
        )