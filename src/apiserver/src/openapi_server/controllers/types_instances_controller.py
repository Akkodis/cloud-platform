import requests
import json
import sys


def method(mec_id, endpoint, request, type_id=None, **kwargs):
    url = 'http://apiserver.cloud-platform.svc.cluster.local:5000/api/v1/mec/' + str(mec_id) + '/nbservices'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 404:
        return "Edge server not found", 414

    json_response = json.loads(response.content)
    service_index = next((index for (index, key) in enumerate(json_response) if key["service_name"] == "edgeinstance-api" ), None)
    if service_index is None:
        return "Edge Instance API not avalaible in specified server", 415

    edgeinstance_ip = json_response[service_index]["host"]
    edgeinstance_port = json_response[service_index]["port"]
    try:
        url = 'https://' + edgeinstance_host + ':' + edgeinstance_port + '/api/v1' +  endpoint
        if type_id:
            url = url + '/' + str(type_id)
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        response = request(url, headers=headers, **kwargs)
        json_response = json.loads(response.content)
    except:
        return "Failed to establish connection with Edge Instance API", 505

    return json_response


def post_type(payload, mec_id):  # noqa: E501
    """Add a new instance type in a specific MEC

     # noqa: E501

    :param payload: Type object that needs to be added
    :type payload: dict | bytes
    :param mec_id: Specify the MEC id to get the information from a specific server
    :type mec_id: str

    :rtype: InstanceType
    """

    return method(mec_id, '/types', request.post, data=json.dumps(payload))


def get_types(mec_id):  # noqa: E501
    """Get instance types in a specific MEC

     # noqa: E501

    :param mec_id: Specify the MEC id to get the information from a specific server
    :type mec_id: str

    :rtype: InstanceType
    """
    return method(mec_id, '/types', request.get, verify=False)



def get_type(mec_id, type_id):  # noqa: E501
    """Get an instance type in a specific MEC

     # noqa: E501

    :param mec_id: Specify the MEC id to get the information from a specific server
    :type mec_id: str
    :param type_id: Specify the type id to get information about the instance type
    :type type_id: int

    :rtype: InstanceType
    """
    return method(mec_id, '/types',  request.get, type_id, verify=False)



def patch_type(payload, mec_id, type_id):  # noqa: E501
    """Update an instance type in a specific MEC

     # noqa: E501

    :param ayload: 
    :type ayload: dict | bytes
    :param mec_id: Specify the MEC id to get the information from a specific server
    :type mec_id: str
    :param type_id: Specify the type id to modify the instance type and/or the resources
    :type type_id: int

    :rtype: InstanceType
    """

    return method(mec_id, '/types', request.patch, type_id, data=json.dumps(payload))




def delete_type(mec_id, type_id):  # noqa: E501
    """Delete an instance type in a specific MEC

     # noqa: E501

    :param mec_id: Specify the MEC id to get the information from a specific server
    :type mec_id: str
    :param type_id: Specify the type id to delete the instance type
    :type type_id: int

    :rtype: InstanceType
    """
    return method(mec_id, '/types',  request.delete, type_id)


def get_instances(mec_id):  # noqa: E501
    """Get the deployed instances in a specific MEC

     # noqa: E501

    :param mec_id: Specify the MEC id to get the information from a specific server
    :type mec_id: str

    :rtype: Instance
    """
    return method(mec_id, '/instances', request.get)


def post_instance(payload, mec_id):  # noqa: E501
    """Deploy a pipeline instance in a specific MEC

     # noqa: E501

    :param payload:
    :type payload: dict | bytes
    :param mec_id: Specify the MEC id to get the information from a specific server
    :type mec_id: str

    :rtype: Instance
    """
#    if connexion.request.is_json:
#        payload = Instance.from_dict(connexion.request.get_json())  # noqa: E501

    return method(mec_id, '/instances', request.post, data=json.dumps(payload))



def get_instance(mec_id, instance_id):  # noqa: E501
    """Get a specific instance information in a specific MEC

     # noqa: E501

    :param mec_id: Specify the MEC id to get the information from a specific server
    :type mec_id: str
    :param instance_id: Specify the instance ID to get the information
    :type instance_id: str

    :rtype: Instance
    """
    return method(mec_id, '/instances', request.get, instance_id)



def delete_instance(mec_id, instance_id):  # noqa: E501
    """Delete an instance in a specific MEC

     # noqa: E501

    :param mec_id: Specify the MEC id to get the information from a specific server
    :type mec_id: str
    :param instance_id: Specify the instance ID to delete the pipeline instance
    :type instance_id: str

    :rtype: Instance
    """
    return method(mec_id, '/instances', request.delete, instance_id)
