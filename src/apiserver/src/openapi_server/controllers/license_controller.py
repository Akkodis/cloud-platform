import connexion
import six

from openapi_server.models.license import License  # noqa: E501
from openapi_server.models.license_data import LicenseData
from openapi_server import util

from pymongo import MongoClient
from flask import current_app, g

import os

host     = os.environ['MONGODB_HOST']
username = os.environ['MONGODB_USER']
password = os.environ['MONGODB_PASSWORD']
database = os.environ['LICENSE_DB_NAME']

def get_db():
    if 'mongodb' not in g:
        client = MongoClient(host=host, username=username, password=password, authSource=database) # Update if using remote MongoDB instance
        g.mongodb = client[database]
    return g.mongodb

def delete_license(license_id):  # noqa: E501
    """Delete a specific license

     # noqa: E501

    :param license_id: 
    :type license_id: int

    :rtype: None
     """
    if len(list(get_db()['licenses'].find({'_id': license_id}))) > 0:
        get_db()['licenses'].delete_one({'_id': license_id})
        return 'License deleted', 200
    else:
        return "License not found (ID does not exist)", 404

def get_license(license_id):  # noqa: E501
    """Get license_example information

     # noqa: E501

    :param license_id: 
    :type license_id: int

    :rtype: License
    """
    if len(list(get_db()['licenses'].find({'_id': license_id}))) > 0:
        return get_db()['licenses'].find_one({'_id': license_id}), 200
    else:
        return "License not found (ID does not exist)", 404

def get_licenses():  # noqa: E501
    """List with all the licenses

     # noqa: E501


    :rtype: None
    """
    licences = list(get_db()['licenses'].find())
    licences = {
        'licenses': licences,
        'total_records': len(licences)
    }
    return licences, 200


def post_licenses(body):  # noqa: E501
    """Create a new license

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: License
    """
    if connexion.request.mimetype == "application/json":
        
        body = License.from_dict(body)  # noqa: E501

    if len(list(get_db()['licenses'].find({'_id': body.id}))) == 0:
        get_db()['licenses'].insert_one({'_id': body.id, 'license': str(body.license)})
        return "License added with success", 200
    else:
        return "License already exists with this ID", 400



def put_license(body, license_id):  # noqa: E501
    """Update license information

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param license_id: 
    :type license_id: int

    :rtype: License
    """
    if connexion.request.mimetype == "application/json":
        body = License.from_dict(body)  # noqa: E501
    if len(list(get_db()['licenses'].find({'_id': license_id}))) > 0:
        get_db()['licenses'].update_one({'_id': license_id}, {'$set': {'_id': license_id, 'license': str(body)}})
        return "License update with success", 200
    else:
        return "License not found (ID does not exist)", 404
