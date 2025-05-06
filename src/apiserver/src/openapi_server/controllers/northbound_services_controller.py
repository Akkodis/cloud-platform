import connexion
import six

from openapi_server.models.nb_service import NBService  # noqa: E501
from openapi_server import util

from openapi_server.controllers.data_5gmeta_functions import * #check_is_a_tile, get_mecinstances_by_tile


def add_nbservice_to_mec(mec_id, body=None):  # noqa: E501
    """add_nbservice_to_mec

    Add a northbound service information to a MEC # noqa: E501

    :param mec_id: MEC ID
    :type mec_id: str
    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if (check_mec_id_exists(mec_id)):
        print("MEC ID EXISTS", flush=True)
    else:
        print("MEC ID NOT EXISTS", flush=True)
        return jsonify({'message':"MEC ID NOT EXISTS"}), 404

    if connexion.request.is_json:
        body = NBService.from_dict(connexion.request.get_json())  # noqa: E501z
        body_json = connexion.request.get_json()

    return add_new_nbservice( mec_id, body.service_name, body.ip, body.port, body.description, body.props)


def delete_nbservice_in_mec(mec_id, service_id):  # noqa: E501
    """delete_nbservice_in_mec

    Delete a northbound service in a MEC # noqa: E501

    :param mec_id: MEC ID
    :type mec_id: str
    :param service_id: Service ID
    :type service_id: str

    :rtype: None
    """
    if (check_mec_id_exists(mec_id)):
        print("MEC ID EXISTS", flush=True)
    else:
        print("MEC ID NOT EXISTS", flush=True)
        return jsonify({'message':"MEC ID NOT EXISTS"}), 404

    if (check_service_id_exists(mec_id, service_id)):
        print("SERVICE ID EXISTS", flush=True)
    else:
        print("SERVICE ID NOT EXISTS IN SPECIFIED MEC ID", flush=True)
        return jsonify({"message":"SERVICE ID NOT EXISTS IN SPECIFIED MEC ID","mec_id":mec_id,"service_id":service_id}), 404

    if( delete_nbservice(mec_id, service_id ) ):
        return jsonify({"message":"Service deleted","mec_id":mec_id,"service_id":service_id}), 200
    else:
        return jsonify({"message":"Service could not be deleted","mec_id":mec_id,"service_id":service_id}), 400


def get_nbservice_from_mec(mec_id, service_id):  # noqa: E501
    """get_nbservice_from_mec

    Get a northbound service from a MEC # noqa: E501

    :param mec_id: MEC ID
    :type mec_id: str
    :param service_id: Service ID
    :type service_id: str

    :rtype: NBService
    """
    if (check_mec_id_exists(mec_id)):
        print("MEC ID EXISTS", flush=True)
    else:
        print("MEC ID NOT EXISTS", flush=True)
        return jsonify({'message':"MEC ID NOT EXISTS"}), 404

    if (check_service_id_exists(mec_id, service_id)):
        print("SERVICE ID EXISTS", flush=True)
    else:
        print("SERVICE ID NOT EXISTS IN SPECIFIED MEC ID", flush=True)
        return jsonify({"message":"SERVICE ID NOT EXISTS IN SPECIFIED MEC ID","mec_id":mec_id,"service_id":service_id}), 404

    return get_nbservice(mec_id, service_id)


def get_nbservices_from_mec(mec_id):  # noqa: E501
    """get_nbservices_from_mec

    Get a northbound service information from a MEC # noqa: E501

    :param mec_id: MEC ID
    :type mec_id: str

    :rtype: NBService
    """
    if (check_mec_id_exists(mec_id)):
        print("MEC ID EXISTS", flush=True)
    else:
        print("MEC ID NOT EXISTS", flush=True)
        return jsonify({'message':"MEC ID NOT EXISTS"}), 404

    return get_nbservices(mec_id)


def modify_nbservice_in_mec(mec_id, service_id, body=None):  # noqa: E501
    """modify_nbservice_in_mec

    Modify a northbound service in a MEC # noqa: E501

    :param mec_id: MEC ID
    :type mec_id: str
    :param service_id: Service ID
    :type service_id: str
    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if (check_mec_id_exists(mec_id)):
        print("MEC ID EXISTS", flush=True)
    else:
        print("MEC ID NOT EXISTS", flush=True)
        return jsonify({'message':"MEC ID NOT EXISTS"}), 404

    if (check_service_id_exists(mec_id, service_id)):
        print("SERVICE ID EXISTS", flush=True)
    else:
        print("SERVICE ID NOT EXISTS IN SPECIFIED MEC ID", flush=True)
        return jsonify({"message":"SERVICE ID NOT EXISTS IN SPECIFIED MEC ID","mec_id":mec_id,"service_id":service_id}), 404

    if connexion.request.is_json:
        body = NBService.from_dict(connexion.request.get_json())  # noqa: E501z
        body_json = connexion.request.get_json()

    if( modify_nbservice( mec_id, service_id, body.service_name, body.ip, body.port, body.description, body.props) ):
        return jsonify({'service_id':service_id,"message":"updated"}), 200
    else:
        return jsonify({'message':"Not deleted"}), 400
