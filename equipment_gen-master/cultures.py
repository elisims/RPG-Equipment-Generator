"""
This is the cultures module and supports all the REST actions for the
cultures data
Migration to SQL - COMPLETE
"""

from flask import make_response, abort
from config import db
from models import Culture, CultureSchema
from sqlalchemy import inspect
import pymysql
import re

def read_all():
    """
    This function responds to a request for /api/cultures
    with the complete lists of cultures
    :return:        json string of list of cultures
    """
    # Create the list of cultures from our data
    cultures = Culture.query.all()

    # Serialize the data for the response
    culture_schema = CultureSchema(many=True)
    data = culture_schema.dump(cultures)
    return data

def read_culture_cols():
    culture_cols = []
    mapper = inspect(Culture)

    for column in mapper.columns:
        culture_cols.append({"col_name": str(column.key), "col_type": str(column.type)})
    
    return culture_cols


def read_one(culture_id):
    """
    This function responds to a request for /api/cultures/{culture_id}
    with one matching culture from cultures
    :param culture_id:   Id of culture to find
    :return:            culture matching id
    """
    # Get the culture requested
    culture = Culture.query.filter(Culture.culture_id == culture_id).one_or_none()

    # Did we find a culture?
    if culture is not None:

        # Serialize the data for the response
        culture_schema = CultureSchema()
        data = culture_schema.dump(culture)
        return data

    # Otherwise, nope, didn't find that culture
    else:
        abort(
            404,
            "Culture not found for Id: {culture_id}".format(culture_id=culture_id),
        )


def create(culture):
    """
    This function creates a new culture in the cultures structure
    based on the passed in culture data
    :param culture:  culture to create in cultures structure
    :return:        201 on success, 406 on culture exists
    """
    name = culture.get("name")

    existing_culture = (
        Culture.query.filter(Culture.name == name)
        .one_or_none()
    )

    # Can we insert this culture?
    if existing_culture is None:

        # Create a culture instance using the schema and the passed in culture
        schema = CultureSchema()
        new_culture = schema.load(culture, session=db.session)

        # Add the culture to the database
        db.session.add(new_culture)
        db.session.commit()

        # Serialize and return the newly created culture in the response
        data = schema.dump(new_culture)

        return data, 201

    # Otherwise, nope, culture exists already
    else:
        abort(
            409,
            "Culture {name} exists already".format(
                name=name
            ),
        )


def update(id, culture):
    """
    This function updates an existing culture in the cultures structure
    Throws an error if a culture with the name we want to update to
    already exists in the database.
    :param id:   Id of the culture to update in the cultures structure
    :param culture:      culture to update
    :return:            updated culture structure
    """
    # Get the culture requested from the db into session
    update_culture = Culture.query.filter(
        Culture.id == id
    ).one_or_none()

    # Try to find an existing culture with the same name as the update
    name = culture.get("name")
    description = culture.get("description")

    existing_culture = (
        Culture.query.filter(Culture.name == name)
        .one_or_none()
    )

    # Are we trying to find a culture that does not exist?
    if update_culture is None:
        abort(
            404,
            "Culture not found for Id: {id}".format(id=id),
        )

    # Would our update create a duplicate of another culture already existing?
    elif (
        existing_culture is not None and existing_culture.id != id
    ):
        abort(
            409,
            "Culture {name} exists already".format(
                name=name
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in culture into a db object
        schema = CultureSchema()
        update = schema.load(culture, session=db.session)

        # Set the id to the culture we want to update
        update.id = update_culture.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated culture in the response
        data = schema.dump(update_culture)

        return data, 200


def delete(id):
    """
    This function deletes a culture from the cultures structure
    :param id:   Id of the culture to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the culture requested
    culture = Culture.query.filter(Culture.id == id).one_or_none()

    # Did we find a culture?
    if culture is not None:
        db.session.delete(culture)
        db.session.commit()
        return make_response(
            "Culture {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that culture
    else:
        abort(
            404,
            "Culture not found for Id: {id}".format(id=id),
        )