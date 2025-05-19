# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.mec_creation import MECCreation  # noqa: E501
from swagger_server.models.mec_instance_list import MECInstanceList  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSouthboundServicesController(BaseTestCase):
    """SouthboundServicesController integration test stubs"""

    def test_delete_mec(self):
        """Test case for delete_mec

        Delete a MEC
        """
        response = self.client.open(
            '/discovery-api/mec/{mec_id}'.format(mec_id='mec_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_tile_mec(self):
        """Test case for delete_tile_mec

        Delete a serving tile from a MEC instance
        """
        response = self.client.open(
            '/discovery-api/mec/{mec_id}/tile/{tile}'.format(mec_id='mec_id_example', tile='tile_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_mec(self):
        """Test case for get_mec

        Get all serving MEC servers
        """
        response = self.client.open(
            '/discovery-api/mec/{mec_id}'.format(mec_id='mec_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_mec_tile(self):
        """Test case for get_mec_tile

        Find serving MEC in a tile
        """
        response = self.client.open(
            '/discovery-api/mec/{tile}'.format(tile='tile_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_mec(self):
        """Test case for post_mec

        Register a MEC instance in the discovery service
        """
        body = MECCreation()
        response = self.client.open(
            '/discovery-api/mec',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_tile_mec(self):
        """Test case for post_tile_mec

        Add serving tile to a MEC intance
        """
        response = self.client.open(
            '/discovery-api/mec/{mec_id}/tile/{tile}'.format(mec_id='mec_id_example', tile='tile_example'),
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
