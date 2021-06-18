"""
This is the [plural] module and supports all the REST actions for the
[plural] data
"""

from flask import make_response, abort
from config import db
from models import [ModelName], [ModelName]Schema
import sqlite3

def read_all():
    """
    This function responds to a request for /api/[plural]
    with the complete lists of [plural]
    :return:        json string of list of [plural]
    """
    print("Reading All")
    # Create the list of [plural] from our data
    [plural] = [ModelName].query.all()

    # Serialize the data for the response
    [singular]_schema = [ModelName]Schema(many=True)
    data = [singular]_schema.dump([plural])
    print("done")
    return data

def read_[singular]_cols():
    conn = sqlite3.connect('db/equipment.db')

    c = conn.cursor()

    c.execute('PRAGMA TABLE_INFO([plural])')
    s = c.fetchall()

    cols = []
    for i in s:
        print(i[1], i[2])
        x = {"col_name": i[1], "col_type": i[2]}
        cols.append(x)
    
    return cols


def read_one([singular]_id):
    """
    This function responds to a request for /api/[plural]/{[singular]_id}
    with one matching [singular] from [plural]
    :param [singular]_id:   Id of [singular] to find
    :return:            [singular] matching id
    """
    # Get the [singular] requested
    [singular] = [ModelName].query.filter([ModelName].[singular]_id == [singular]_id).one_or_none()

    # Did we find a [singular]?
    if [singular] is not None:

        # Serialize the data for the response
        [singular]_schema = [ModelName]Schema()
        data = [singular]_schema.dump([singular])
        return data

    # Otherwise, nope, didn't find that [singular]
    else:
        abort(
            404,
            "[singular] not found for Id: {[singular]_id}".format([singular]_id=[singular]_id),
        )


def create([singular]):
    """
    This function creates a new [singular] in the [plural] structure
    based on the passed in [singular] data
    :param [singular]:  [singular] to create in [plural] structure
    :return:        201 on success, 406 on [singular] exists
    """
    name = [singular].get("name")

    existing_[singular] = (
        [ModelName].query.filter([ModelName].name == name)
        .one_or_none()
    )

    # Can we insert this [singular]?
    if existing_[singular] is None:

        # Create a [singular] instance using the schema and the passed in [singular]
        schema = [ModelName]Schema()
        new_[singular] = schema.load([singular], session=db.session)

        # Add the [singular] to the database
        db.session.add(new_[singular])
        db.session.commit()

        # Serialize and return the newly created [singular] in the response
        data = schema.dump(new_[singular])

        return data, 201

    # Otherwise, nope, [singular] exists already
    else:
        abort(
            409,
            "[singular] {name} exists already".format(
                name=name
            ),
        )


def update(id, [singular]):
    """
    This function updates an existing [singular] in the [plural] structure
    Throws an error if a [singular] with the name we want to update to
    already exists in the database.
    :param id:   Id of the [singular] to update in the [plural] structure
    :param [singular]:      [singular] to update
    :return:            updated [singular] structure
    """
    # Get the [singular] requested from the db into session
    update_[singular] = [ModelName].query.filter(
        [ModelName].id == id
    ).one_or_none()

    # Try to find an existing [singular] with the same name as the update
    name = [singular].get("name")
    description = [singular].get("description")

    existing_[singular] = (
        [ModelName].query.filter([ModelName].name == name)
        .one_or_none()
    )

    # Are we trying to find a [singular] that does not exist?
    if update_[singular] is None:
        abort(
            404,
            "[singular] not found for Id: {id}".format(id=id),
        )

    # Would our update create a duplicate of another [singular] already existing?
    elif (
        existing_[singular] is not None and existing_[singular].id != id
    ):
        abort(
            409,
            "[singular] {name} exists already".format(
                name=name
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in [singular] into a db object
        schema = [ModelName]Schema()
        update = schema.load([singular], session=db.session)

        # Set the id to the [singular] we want to update
        update.id = update_[singular].id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated [singular] in the response
        data = schema.dump(update_[singular])

        return data, 200


def delete(id):
    """
    This function deletes a [singular] from the [plural] structure
    :param id:   Id of the [singular] to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the [singular] requested
    [singular] = [ModelName].query.filter([ModelName].id == id).one_or_none()

    # Did we find a [singular]?
    if [singular] is not None:
        db.session.delete([singular])
        db.session.commit()
        return make_response(
            "[singular] {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that [singular]
    else:
        abort(
            404,
            "[singular] not found for Id: {id}".format(id=id),
        )