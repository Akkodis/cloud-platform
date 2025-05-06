import requests
import json
import sys
#import connexion
#import six

#from openapi_server.models.instance_type import InstanceType  # noqa: E501
#from openapi_server import util

edgeinstance_ip = "your-mec-fqdn"

def post_type(payload, mec_id):  # noqa: E501
    """Add a new instance type in a specific MEC

     # noqa: E501

    :param payload: Type object that needs to be added
    :type payload: dict | bytes
    :param mec_id: Specify the MEC id to get the information from a specific server
    :type mec_id: str

    :rtype: InstanceType
    """
#    if connexion.request.is_json:
#        payload = InstanceType.from_dict(connexion.request.get_json())  # noqa: E501

    url = 'http://discovery-api.cloud-platform.svc.cluster.local:8080/discovery-api/mec/' + str(mec_id) + '/nbservices'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 404:
        return "Edge server not found", 414

    json_response = json.loads(response.content)
    service_index = next((index for (index, key) in enumerate(json_response) if key["service_name"] == "edgeinstance-api" ), None)
    if service_index is None:
        return "Edge Instance API not avalaible in specified server", 415

   # edgeinstance_ip = json_response[service_index]["ip"]
    edgeinstance_port = json_response[service_index]["port"]
    try:
        url = 'https://' + edgeinstance_ip + '/edgeinstance-api' + '/types'
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        json_response = json.loads(response.content)
    except:
        return "Failed to establish connection with Edge Instance API", 505

    return json_response


def get_types(mec_id):  # noqa: E501
    """Get instance types in a specific MEC

     # noqa: E501

    :param mec_id: Specify the MEC id to get the information from a specific server
    :type mec_id: str

    :rtype: InstanceType
    """
    url = 'http://discovery-api.cloud-platform.svc.cluster.local:8080/discovery-api/mec/' + str(mec_id) + '/nbservices'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        return "Edge server not found", 414

    json_response = json.loads(response.content)
    service_index = next((index for (index, key) in enumerate(json_response) if key["service_name"] == "edgeinstance-api" ), None)
    if service_index is None:
        return "Edge Instance API not avalaible in specified server", 415

    #edgeinstance_ip = json_response[service_index]["ip"]
    edgeinstance_port = json_response[service_index]["port"]
    try:
        url = 'https://' + edgeinstance_ip + '/edgeinstance-api' + '/types'
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers, verify=False)
        json_response = json.loads(response.content)
    except:
        return "Failed to establish connection with Edge Instance API", 505

    return json_response


def get_type(mec_id, type_id):  # noqa: E501
    """Get an instance type in a specific MEC

     # noqa: E501

    :param mec_id: Specify the MEC id to get the information from a specific server
    :type mec_id: str
    :param type_id: Specify the type id to get information about the instance type
    :type type_id: int

    :rtype: InstanceType
    """
    url = 'http://discovery-api.cloud-platform.svc.cluster.local:8080/discovery-api/mec/' + str(mec_id) + '/nbservices'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        return "Edge server not found", 414

    json_response = json.loads(response.content)
    service_index = next((index for (index, key) in enumerate(json_response) if key["service_name"] == "edgeinstance-api" ), None)
    if service_index is None:
        return "Edge Instance API not avalaible in specified server", 415

    #edgeinstance_ip = json_response[service_index]["ip"]
    edgeinstance_port = json_response[service_index]["port"]
    try:
        url = 'https://' + edgeinstance_ip + '/edgeinstance-api' + '/types/' + str(type_id)
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        json_response = json.loads(response.content ,)
    except:
        return "Failed to establish connection with Edge Instance API", 505

    return json_response


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
    url = 'http://discovery-api.cloud-platform.svc.cluster.local:8080/discovery-api/mec/' + str(mec_id) + '/nbservices'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        return "Edge server not found", 414

    json_response = json.loads(response.content)
    service_index = next((index for (index, key) in enumerate(json_response) if key["service_name"] == "edgeinstance-api" ), None)
    if service_index is None:
        return "Edge Instance API not avalaible in specified server", 415

    #edgeinstance_ip = json_response[service_index]["ip"]
    edgeinstance_port = json_response[service_index]["port"]
    try:
        url = 'https://' + edgeinstance_ip + '/edgeinstance-api' + '/types/' + str(type_id)
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        response = requests.patch(url, data=json.dumps(payload), headers=headers)
        json_response = json.loads(response.content)
        print(json_response, file=sys.stderr)
    except:
        return "Failed to establish connection with Edge Instance API", 505

    return json_response


def delete_type(mec_id, type_id):  # noqa: E501
    """Delete an instance type in a specific MEC

     # noqa: E501

    :param mec_id: Specify the MEC id to get the information from a specific server
    :type mec_id: str
    :param type_id: Specify the type id to delete the instance type
    :type type_id: int

    :rtype: InstanceType
    """
    url = 'http://discovery-api.cloud-platform.svc.cluster.local:8080/discovery-api/mec/' + str(mec_id) + '/nbservices'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 404:
        return "Edge server not found", 414

    json_response = json.loads(response.content)
    service_index = next((index for (index, key) in enumerate(json_response) if key["service_name"] == "edgeinstance-api" ), None)
    if service_index is None:
        return "Edge Instance API not avalaible in specified server", 415

    #edgeinstance_ip = json_response[service_index]["ip"]
    edgeinstance_port = json_response[service_index]["port"]
    try:
        url = 'https://' + edgeinstance_ip + '/edgeinstance-api' + '/types/' + str(type_id)
        headers = {"accept": "application/json"}
        response = requests.delete(url, headers=headers)
        json_response = json.loads(response.content)
        print(json_response, file=sys.stderr)
    except:
        return "Failed to establish connection with Edge Instance API", 505

    return json_response
