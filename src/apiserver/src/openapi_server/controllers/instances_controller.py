import requests
import json
#import connexion
#import six

#from openapi_server.models.instance import Instance  # noqa: E501
#from openapi_server import util


edgeinstance_ip = "your-mec-fqdn"

def get_instances(mec_id):  # noqa: E501
    """Get the deployed instances in a specific MEC

     # noqa: E501

    :param mec_id: Specify the MEC id to get the information from a specific server
    :type mec_id: str

    :rtype: Instance
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
        url = 'http://' + edgeinstance_ip + '/edgeinstance-api/' + '/instances'
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        json_response = json.loads(response.content)
    except:
        return "Failed to establish connection with Edge Instance API", 505

    return json_response

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

        url = 'https://' + edgeinstance_ip + '/edgeinstance-api/' + '/instances'
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        json_response = json.loads(response.content)
    except:
        return "Failed to establish connection with Edge Instance API", 505

    return json_response



def get_instance(mec_id, instance_id):  # noqa: E501
    """Get a specific instance information in a specific MEC

     # noqa: E501

    :param mec_id: Specify the MEC id to get the information from a specific server
    :type mec_id: str
    :param instance_id: Specify the instance ID to get the information
    :type instance_id: str

    :rtype: Instance
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
        url = 'http://' + edgeinstance_ip + '/edgeinstance-api/' + '/instances'
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        json_response = json.loads(response.content)
    except:
        return "Failed to establish connection with Edge Instance API", 505

    return json_response


def delete_instance(mec_id, instance_id):  # noqa: E501
    """Delete an instance in a specific MEC

     # noqa: E501

    :param mec_id: Specify the MEC id to get the information from a specific server
    :type mec_id: str
    :param instance_id: Specify the instance ID to delete the pipeline instance
    :type instance_id: str

    :rtype: Instance
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
        url = 'http://' + edgeinstance_ip + '/edgeinstance-api/' + '/instances'
        headers = {"accept": "application/json"}
        response = requests.delete(url, headers=headers)
        json_response = json.loads(response.content)
    except:
        return "Failed to establish connection with Edge Instance API", 505

    return json_response
