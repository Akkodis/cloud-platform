# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.nb_service import NBService  # noqa: E501
from swagger_server.test import BaseTestCase


class TestNorthboundServicesController(BaseTestCase):
    """NorthboundServicesController integration test stubs"""

    def test_add_nbservice_to_mec(self):
        """Test case for add_nbservice_to_mec

        
        """
        body = NBService()
        response = self.client.open(
            '/discovery-api/mec/{mec_id}/nbservices'.format(mec_id='mec_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_nbservice_in_mec(self):
        """Test case for delete_nbservice_in_mec

        
        """
        response = self.client.open(
            '/discovery-api/mec/{mec_id}/nbservices/{service_id}'.format(mec_id='mec_id_example', service_id='service_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_nbservice_from_mec(self):
        """Test case for get_nbservice_from_mec

        
        """
        response = self.client.open(
            '/discovery-api/mec/{mec_id}/nbservices/{service_id}'.format(mec_id='mec_id_example', service_id='service_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_nbservices_from_mec(self):
        """Test case for get_nbservices_from_mec

        
        """
        response = self.client.open(
            '/discovery-api/mec/{mec_id}/nbservices'.format(mec_id='mec_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_modify_nbservice_in_mec(self):
        """Test case for modify_nbservice_in_mec

        
        """
        body = NBService()
        response = self.client.open(
            '/discovery-api/mec/{mec_id}/nbservices/{service_id}'.format(mec_id='mec_id_example', service_id='service_id_example'),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
