# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.license import License  # noqa: E501
from swagger_server.models.license_data import LicenseData  # noqa: E501
from swagger_server.models.license_list import LicenseList  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_delete_license(self):
        """Test case for delete_license

        Delete a specific license
        """
        response = self.client.open(
            '/license/{license_id}'.format(license_id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_license(self):
        """Test case for get_license

        Get license_example information
        """
        response = self.client.open(
            '/license/{license_id}'.format(license_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_licenses(self):
        """Test case for get_licenses

        List with all the licenses
        """
        response = self.client.open(
            '/licenses',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_licenses(self):
        """Test case for post_licenses

        Create a new license
        """
        body = License()
        response = self.client.open(
            '/licenses',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_license(self):
        """Test case for put_license

        Update license information
        """
        body = LicenseData()
        response = self.client.open(
            '/license/{license_id}'.format(license_id=56),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
