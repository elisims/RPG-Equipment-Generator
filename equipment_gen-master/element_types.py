"""
This is the element_types module and supports all the REST actions for the
element_types data
Migration to SQL - COMPLETE
"""

from flask import make_response, abort
from config import db
from models import ElementType, ElementTypeSchema, view_ElementType, viewElementTypeSchema
from sqlalchemy import inspect
import pymysql
import re

def read_all():
    """
    This function responds to a request for /api/element_types
    with the complete lists of element_types
    :return:        json string of list of element_types
    """
    # Create the list of element_types from our data
    element_types = view_ElementType.query.all()

    # Serialize the data for the response
    element_type_schema = viewElementTypeSchema(many=True)
    data = element_type_schema.dump(element_types)
    return data

def read_element_type_cols():
    
    element_type_cols = []
    mapper = inspect(ElementType)

    for column in mapper.columns:
        element_type_cols.append({"col_name": str(column.key), "col_type": str(column.type)})
    
    return element_type_cols


def read_one(element_type_id):
    """
    This function responds to a request for /api/element_types/{element_type_id}
    with one matching element_type from element_types
    :param element_type_id:   Id of element_type to find
    :return:            element_type matching id
    """
    # Get the element_type requested
    element_type = view_ElementType.query.filter(ElementType.element_type_id == element_type_id).one_or_none()

    # Did we find a element_type?
    if element_type is not None:

        # Serialize the data for the response
        element_type_schema = view_ElementTypeSchema()
        data = element_type_schema.dump(element_type)
        return data

    # Otherwise, nope, didn't find that element_type
    else:
        abort(
            404,
            "element_type not found for Id: {element_type_id}".format(element_type_id=element_type_id),
        )


def create(element_type):
    """
    This function creates a new element_type in the element_types structure
    based on the passed in element_type data
    :param element_type:  element_type to create in element_types structure
    :return:        201 on success, 406 on element_type exists
    """
    name = element_type.get("name")

    existing_element_type = (
        ElementType.query.filter(ElementType.name == name)
        .one_or_none()
    )

    # Can we insert this element_type?
    if existing_element_type is None:

        # Create a element_type instance using the schema and the passed in element_type
        schema = ElementTypeSchema()
        new_element_type = schema.load(element_type, session=db.session)

        # Add the element_type to the database
        db.session.add(new_element_type)
        db.session.commit()

        # Serialize and return the newly created element_type in the response
        data = schema.dump(new_element_type)

        return data, 201

    # Otherwise, nope, element_type exists already
    else:
        abort(
            409,
            "element_type {name} exists already".format(
                name=name
            ),
        )


def update(id, element_type):
    """
    This function updates an existing element_type in the element_types structure
    Throws an error if a element_type with the name we want to update to
    already exists in the database.
    :param id:   Id of the element_type to update in the element_types structure
    :param element_type:      element_type to update
    :return:            updated element_type structure
    """
    # Get the element_type requested from the db into session
    update_element_type = ElementType.query.filter(
        ElementType.id == id
    ).one_or_none()

    # Try to find an existing element_type with the same name as the update
    name = element_type.get("name")
    description = element_type.get("description")

    existing_element_type = (
        ElementType.query.filter(ElementType.name == name)
        .one_or_none()
    )

    # Are we trying to find a element_type that does not exist?
    if update_element_type is None:
        abort(
            404,
            "element_type not found for Id: {id}".format(id=id),
        )

    # Would our update create a duplicate of another element_type already existing?
    elif (
        existing_element_type is not None and existing_element_type.id != id
    ):
        abort(
            409,
            "element_type {name} exists already".format(
                name=name
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in element_type into a db object
        schema = viewElementTypeSchema()
        update = schema.load(element_type, session=db.session)

        # Set the id to the element_type we want to update
        update.id = update_element_type.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated element_type in the response
        data = schema.dump(update_element_type)

        return data, 200


def delete(id):
    """
    This function deletes a element_type from the element_types structure
    :param id:   Id of the element_type to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the element_type requested
    element_type = ElementType.query.filter(ElementType.id == id).one_or_none()

    # Did we find a element_type?
    if element_type is not None:
        db.session.delete(element_type)
        db.session.commit()
        return make_response(
            "element_type {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that element_type
    else:
        abort(
            404,
            "element_type not found for Id: {id}".format(id=id),
        )