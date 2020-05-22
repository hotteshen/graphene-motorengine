.. image:: https://travis-ci.org/graphql-python/graphene-motorengine.svg?branch=master
    :target: https://travis-ci.org/graphql-python/graphene-motorengine
.. image:: https://coveralls.io/repos/github/graphql-python/graphene-motorengine/badge.svg?branch=master
    :target: https://coveralls.io/github/graphql-python/graphene-motorengine?branch=master
.. image:: https://badge.fury.io/py/graphene-motorengine.svg
    :target: https://badge.fury.io/py/graphene-motorengine
.. image:: https://img.shields.io/pypi/pyversions/graphene-motorengine.svg
    :target: https://pypi.python.org/pypi/graphene-motorengine/

Graphene-Mongo
==============

A `Mongoengine <https://mongoengine-odm.readthedocs.io/>`__ integration for `Graphene <http://graphene-python.org/>`__.

Installation
------------

For installing graphene-motorengine, just run this command in your shell

.. code:: bash

    pip install graphene-motorengine

Examples
--------

Here is a simple Mongoengine model as `models.py`:

.. code:: python

    from mongoengine import Document
    from mongoengine.fields import StringField

    class User(Document):
        meta = {'collection': 'user'}
        first_name = StringField(required=True)
        last_name = StringField(required=True)


To create a GraphQL schema for it you simply have to write the following:

.. code:: python

    import graphene

    from graphene_motorengine import MongoengineObjectType

    from .models import User as UserModel

    class User(MongoengineObjectType):
        class Meta:
            model = UserModel

    class Query(graphene.ObjectType):
        users = graphene.List(User)

        def resolve_users(self, info):
            return list(UserModel.objects.all())

    schema = graphene.Schema(query=Query)

Then you can simply query the schema:

.. code:: python

    query = '''
        query {
            users {
                firstName,
                lastName
            }
        }
    '''
    result = schema.execute(query)

To learn more check out the `Flask MongoEngine example <https://github.com/graphql-python/graphene-motorengine/tree/master/examples/flask_mongoengine>`__

