# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.geolocation_tile_list import GeolocationTileList  # noqa: F401,E501
from openapi_server import util


class MECLocation(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: str=None, name: str=None, lat: str=None, lng: str=None, organization: str=None, geolocation: List[GeolocationTileList]=None):  # noqa: E501
        """MECLocation - a model defined in Swagger

        :param id: The id of this MECLocation.  # noqa: E501
        :type id: str
        :param name: The name of this MECLocation.  # noqa: E501
        :type name: str
        :param lat: The lat of this MECLocation.  # noqa: E501
        :type lat: str
        :param lng: The lng of this MECLocation.  # noqa: E501
        :type lng: str
        :param organization: The organization of this MECLocation.  # noqa: E501
        :type organization: str
        :param geolocation: The geolocation of this MECLocation.  # noqa: E501
        :type geolocation: List[GeolocationTileList]
        """
        self.swagger_types = {
            'id': str,
            'name': str,
            'lat': str,
            'lng': str,
            'organization': str,
            'geolocation': List[GeolocationTileList]
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'lat': 'lat',
            'lng': 'lng',
            'organization': 'organization',
            'geolocation': 'geolocation'
        }
        self._id = id
        self._name = name
        self._lat = lat
        self._lng = lng
        self._organization = organization
        self._geolocation = geolocation

    @classmethod
    def from_dict(cls, dikt) -> 'MECLocation':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The MECLocation of this MECLocation.  # noqa: E501
        :rtype: MECLocation
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """Gets the id of this MECLocation.


        :return: The id of this MECLocation.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this MECLocation.


        :param id: The id of this MECLocation.
        :type id: str
        """

        self._id = id

    @property
    def name(self) -> str:
        """Gets the name of this MECLocation.


        :return: The name of this MECLocation.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this MECLocation.


        :param name: The name of this MECLocation.
        :type name: str
        """

        self._name = name

    @property
    def lat(self) -> str:
        """Gets the lat of this MECLocation.


        :return: The lat of this MECLocation.
        :rtype: str
        """
        return self._lat

    @lat.setter
    def lat(self, lat: str):
        """Sets the lat of this MECLocation.


        :param lat: The lat of this MECLocation.
        :type lat: str
        """

        self._lat = lat

    @property
    def lng(self) -> str:
        """Gets the lng of this MECLocation.


        :return: The lng of this MECLocation.
        :rtype: str
        """
        return self._lng

    @lng.setter
    def lng(self, lng: str):
        """Sets the lng of this MECLocation.


        :param lng: The lng of this MECLocation.
        :type lng: str
        """

        self._lng = lng

    @property
    def organization(self) -> str:
        """Gets the organization of this MECLocation.


        :return: The organization of this MECLocation.
        :rtype: str
        """
        return self._organization

    @organization.setter
    def organization(self, organization: str):
        """Sets the organization of this MECLocation.


        :param organization: The organization of this MECLocation.
        :type organization: str
        """

        self._organization = organization

    @property
    def geolocation(self) -> List[GeolocationTileList]:
        """Gets the geolocation of this MECLocation.


        :return: The geolocation of this MECLocation.
        :rtype: List[GeolocationTileList]
        """
        return self._geolocation

    @geolocation.setter
    def geolocation(self, geolocation: List[GeolocationTileList]):
        """Sets the geolocation of this MECLocation.


        :param geolocation: The geolocation of this MECLocation.
        :type geolocation: List[GeolocationTileList]
        """

        self._geolocation = geolocation
