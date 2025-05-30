# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class LicenseData(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, geolimit: str=None, commercial: str=None):  # noqa: E501
        """LicenseData - a model defined in Swagger

        :param geolimit: The geolimit of this LicenseData.  # noqa: E501
        :type geolimit: str
        :param commercial: The commercial of this LicenseData.  # noqa: E501
        :type commercial: str
        """
        self.swagger_types = {
            'geolimit': str,
            'commercial': str
        }

        self.attribute_map = {
            'geolimit': 'geolimit',
            'commercial': 'commercial'
        }
        self._geolimit = geolimit
        self._commercial = commercial

    @classmethod
    def from_dict(cls, dikt) -> 'LicenseData':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The license-data of this LicenseData.  # noqa: E501
        :rtype: LicenseData
        """
        return util.deserialize_model(dikt, cls)

    @property
    def geolimit(self) -> str:
        """Gets the geolimit of this LicenseData.

        Geolimit: {local, city, country, global}  # noqa: E501

        :return: The geolimit of this LicenseData.
        :rtype: str
        """
        return self._geolimit

    @geolimit.setter
    def geolimit(self, geolimit: str):
        """Sets the geolimit of this LicenseData.

        Geolimit: {local, city, country, global}  # noqa: E501

        :param geolimit: The geolimit of this LicenseData.
        :type geolimit: str
        """
        if geolimit is None:
            raise ValueError("Invalid value for `geolimit`, must not be `None`")  # noqa: E501

        self._geolimit = geolimit

    @property
    def commercial(self) -> str:
        """Gets the commercial of this LicenseData.

        Commercial: {profit, non-profit}  # noqa: E501

        :return: The commercial of this LicenseData.
        :rtype: str
        """
        return self._commercial

    @commercial.setter
    def commercial(self, commercial: str):
        """Sets the commercial of this LicenseData.

        Commercial: {profit, non-profit}  # noqa: E501

        :param commercial: The commercial of this LicenseData.
        :type commercial: str
        """
        if commercial is None:
            raise ValueError("Invalid value for `commercial`, must not be `None`")  # noqa: E501

        self._commercial = commercial
