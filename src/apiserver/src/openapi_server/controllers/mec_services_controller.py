import connexion
import six

from openapi_server.models.mec_instance import MECInstance
from openapi_server.models.mec_creation import MECCreation  # noqa: E501
from openapi_server.models.mec_instance_list import MECInstanceList  # noqa: E501
from openapi_server import util
from openapi_server.models.nb_service import NBService  # noqa: E501
from openapi_server.controllers.data_5gmeta_functions import * #check_is_a_tile, get_mecinstances_by_tile


def delete_mec(mec_id):  # noqa: E501
    """Delete a MEC

     # noqa: E501

    :param mec_id: MEC ID
    :type mec_id: str

    :rtype: None
    """
    if(mec_id==None):
        return jsonify({'message':'Incorrect mec_id ','mec_id':mec_id}), 400
    try:
        int(mec_id)
    except:
        return jsonify({'message':'MEC must be a number','mec_id':mec_id}), 400

    if(check_mec_id_exists(mec_id) is False):
        return jsonify({'message':'MEC does not exists','mec_id':mec_id}),404
    else:
        delete_mec_from_db(mec_id)
        return jsonify({'message':'MEC deleted','mec_id':mec_id}),200


def delete_tile_mec(mec_id, tile):  # noqa: E501
    """Delete a serving tile from a MEC instance

     # noqa: E501

    :param mec_id: MEC ID
    :type mec_id: str
    :param tile: Tile to delete
    :type tile: str

    :rtype: None
    """
    if(mec_id==None):
        return jsonify({'message':'Incorrect MEC ID','mec_id':mec_id}),400
    if(tile == None):
        return jsonify({'message':'Incorrect Tile','tile':tile}),401
#    if(check_is_a_tile(tile) == False):
#      return jsonify({'message':'Incorrect Tile','tile':tile,'mec_id':mec_id}),401
    if(check_mec_id_exists(mec_id) is False):
        return jsonify({'message':'MEC ID does not exists','tile':tile,'mec_id':mec_id}),404
 
    mecinstance=get_mecinstances_by_tile(tile)
    if(len(mecinstance) == 0):
        return jsonify({'message':'Tile does not exists','tile':tile,'mec_id':mec_id}),404
    if(int(mecinstance[0].id) == int(mec_id)):
        if( delete_tile_from_mec( mec_id, tile) ):
            return jsonify({'message':'Tile deleted','tile':tile,'mec_id':mec_id}), 200
        else:
            return jsonify({'message':'Tile not deleted','tile':tile,'mec_id':mec_id}), 401
    else:
        return jsonify({'message':'Incorrect tile or MEC ID','tile':tile,'mec_id':mec_id}), 400


def get_mecs():  # noqa: E501
    """Get all serving MEC servers

     # noqa: E501

    :rtype: MECInstanceList
    """
    return get_mecinstances()


def get_mec(mec_id):  # noqa: E501
    """Get a serving MEC server

     # noqa: E501

    :param mec_id: MEC ID
    :type mec_id: str

    :rtype: MECInstanceList
    """
    if(mec_id==None):
        return jsonify({'message':'Incorrect mec_id ','mec_id':mec_id}), 400
    try:
        int(mec_id)
    except:
        return jsonify({'message':'MEC must be a number','mec_id':mec_id}), 400

    if(check_mec_id_exists(mec_id) is False):
        return jsonify({'message':'MEC does not exists','mec_id':mec_id}),404
    else:
        return get_mecinstance_by_id(mec_id)

def get_mec_locations():  # noqa: E501
    """Get serving MEC servers with their locations

     # noqa: E501


    :rtype: MECLocationsList
    """
    return get_mecinstances_locations()


def get_tiles():  # noqa: E501
    """Get list of tiles

     # noqa: E501


    :rtype: MECInstanceList
    """
    return get_locations()

def get_mec_tile(tile):  # noqa: E501
    """Find serving MEC in a tile

     # noqa: E501

    :param tile: Tile to get serving MEC
    :type tile: str

    :rtype: MECInstanceList
    """
    return get_mecinstances_by_tile(tile)


def post_mec(body):  # noqa: E501
    """Register a MEC instance in the discovery service

     # noqa: E501

    :param body: MEC information
    :type body: dict | bytes

    :rtype: None

    return 'do some magic!'
    """
    mec_id = -1
    if connexion.request.mimetype == "application/json":

       #res = "Modified/Create MEC " + body.id + " org: " + body.organization
       #print("Res " + res + " " + str(body_json), flush=True)
       mec_id = add_new_mecserver(body['name'], body['lat'], body['lng'], body['organization'], body['resources'], body['sb_services'], body['props'], body['geolocation'])

        # for each time in the body add a tile to the MEC

    if(mec_id == -1):
      return "Error cannot add the new record.", 404 
    else: 
      return jsonify({ 'mec_id': str(mec_id) }),200


def post_tile_mec(mec_id, tile):  # noqa: E501
    """Add serving tile to a MEC intance

     # noqa: E501

    :param mec_id: MEC ID
    :type mec_id: str
    :param tile: Tile to post
    :type tile: str

    :rtype: None
    """
    if( mec_id == None or tile == None):
        return jsonify({'message':'Incorrect Tile or mec id type'}), 200

    if(check_is_a_tile(tile) == False):
        return jsonify({'message':'Incorrect Tile'}), 200
    
    if (check_mec_id_exists(mec_id)):
        print("MEC ID EXISTS", flush=True)
    else:
        print("MEC ID NOT EXISTS", flush=True)
        return jsonify({'message':'Mec id does not exists'}), 404
    returned_tiles=get_mecinstances_by_tile(tile,1)
    if(len(returned_tiles) == 0):
        if( add_tile_mec(mec_id, tile ) ):
            return jsonify({'message':'Added'}), 200
        else:
            return jsonify({'message':'Not added'}), 400
    else:
        for ctile in returned_tiles:
            for geolocation in ctile.geolocation:
                #print("compare ")
                #print(geolocation.tile_id)
                #print(tile)
                if str(tile) == (geolocation.tile_id):
                    return jsonify({'message':'Tile was added to a previous MEC'}), 400
                elif str(tile) in str(geolocation.tile_id):
                    return jsonify({'message':'Tile requested contains an existing tile'}), 400
                elif str(geolocation.tile_id) in str(tile):
                    return jsonify({'message':'Tile is defined inside a previous defined tile'}), 400
        return jsonify({'message':'Tile was added to a previous MEC'}), 400




def update_mec(body, tile):
    """Updates or create a Service in the registry with form data

    :param body: Service object that needs to be added or modified in the tile
    :type body: dict | bytes
    :param tile: Tile in which the MEC needs to be updated
    :type tile: str

    :rtype: None
    
    if connexion.request.mimetype == "application/json":
        body = MECInstance.from_dict(connexion.request.json())  # noqa: E501
    """    
    res = ""
    if connexion.request.mimetype == "application/json":
        body = MECInstance.from_dict(body)
        res = "Modified/Create MEC " + body['id'] + " org: " + body['organization'] +  " adding tile " + tile
        mec_id =int(body['id'])
        print(res, flush=True)

        if( type(mec_id) != int or tile == None):
          return jsonify({'message':"Incorrect Tile or mec Id type"}), 404
        if(check_is_a_tile(tile) == False):
            return jsonify({'message': "Incorrect Tile"}), 401
        
        if (not check_mec_id_exists(mec_id)):
            print("MEC ID NOT EXISTS", flush=True)
            mec_id = add_new_mecserver( ""+body.name, 0.0, 0.0, "")

        if( post_tile_mec(mec_id, tile ) ):
            res = "OK!"
            return jsonify({"message":"Tile added to MEC","mec_id":mec_id,"tile":tile}), 200
        else:
            return jsonify({'message': "Not deleted"}), 401

    if(res==""):
      return jsonify({'message': "error"}), 400

    else: 
      return res, 200


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

    #if connexion.request.mimetype == "application/json":
        #body = NBService.from_dict(body)  # noqa: E501z
        #body_json = connexion.request.get_json()
    #    print(body)

    return add_new_nbservice( mec_id, body['service_name'], body['host'], body['port'], body['description'], body['props'])

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

    if connexion.request.mimetype == "application/json":
        body = NBService.from_dict(body)  # noqa: E501z
        #body_json = connexion.request.get_json()

    if( modify_nbservice( mec_id, service_id, body.service_name, body.host, body.port, body.description, body.props) ):
        return jsonify({'service_id':service_id,"message":"updated"}), 200
    else:
        return jsonify({'message':"Not deleted"}), 400
