# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from openapi_server.models.instance_type import InstanceType  # noqa: E501
from openapi_server.test import BaseTestCase


class TestTypesController(BaseTestCase):
    """TypesController integration test stubs"""

    def test_delete_type(self):
        """Test case for delete_type

        Delete an instance type in a specific MEC
        """
        response = self.client.open(
            '/cloudinstance-api/mecs/{mec_id}/types/{type_id}'.format(mec_id='mec_id_example', type_id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_type(self):
        """Test case for get_type

        Get instance types in a specific MEC
        """
        response = self.client.open(
            '/cloudinstance-api/mecs/{mec_id}/types'.format(mec_id='mec_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_type_item(self):
        """Test case for get_type_item

        Get an instance type in a specific MEC
        """
        response = self.client.open(
            '/cloudinstance-api/mecs/{mec_id}/types/{type_id}'.format(mec_id='mec_id_example', type_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_patch_type(self):
        """Test case for patch_type

        Update an instance type in a specific MEC
        """
        body = InstanceType()
        response = self.client.open(
            '/cloudinstance-api/mecs/{mec_id}/types/{type_id}'.format(mec_id='mec_id_example', type_id=56),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_type(self):
        """Test case for post_type

        Add a new instance type in a specific MEC
        """
        body = InstanceType()
        response = self.client.open(
            '/cloudinstance-api/mecs/{mec_id}/types'.format(mec_id='mec_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
