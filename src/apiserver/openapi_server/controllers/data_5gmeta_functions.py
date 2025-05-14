import connexion
import six
import os

from openapi_server.models.mec_instance import MECInstance  # noqa: E501
from openapi_server.models.mec_instance_list import MECInstanceList  # noqa: E501
from openapi_server import util

from openapi_server.models.geolocation_tile import GeolocationTile
from openapi_server.models.geolocation_tile_list import GeolocationTileList
from openapi_server.models.sb_service import SBService

import mysql.connector
from mysql.connector import errorcode
from flask import jsonify
import json
from types import SimpleNamespace

config = {
  'user': 'root',
  'password': os.environ["DB_PASSWORD"],
  'host': os.environ["DB_HOST"],
  'database': os.environ["DISCOVERY_DB_NAME"],
  'raise_on_warnings': True
}


################ FUNCTIONS ####### 

def delete_mec_from_db(mec_id):
  '''
  Check if a tile have some characteristics
  '''
  print ("DELETE MEC " + mec_id)
  
  try:
    int(mec_id)
  except:
    print("NOT VALID mec_id "+mec_id)
    return jsonify({'message':"not valid mec_id"}), 400

  try:
      cnx = mysql.connector.connect(**config)
  except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
          print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
          print("Database does not exist")
      else:
          print(err)
      return jsonify({'message':"Error deleting mec_id"}), 400
  else:
      
      cursor = cnx.cursor()
      statement = "DELETE FROM "+config['database']+".`MEC-tile` WHERE mec_id="+mec_id
      
      cursor.execute(statement)
      cnx.commit()

      statement = "DELETE FROM "+config['database']+".`nb_services` WHERE mec_id="+mec_id
      
      cursor.execute(statement)
      cnx.commit()      
      
      statement = "DELETE FROM "+config['database']+".MECservers WHERE id="+mec_id
      
      cursor.execute(statement)
      cnx.commit()

      cursor.close()

      return True
  finally:
      cnx.close()


def check_contains_only(test_str, only_chars):
  '''
  Check if @test_str contains only the chars contained into @only_char
  '''
  under_test = set(only_chars)
  if set(test_str) <= under_test:
      # it's good
      return True
  else:
      # it's bad
      return False
  return False


def check_is_a_tile(tile):
  '''
  Check if a tile have some characteristics
  '''
  print ("CHECK TILE len " + str(len(tile)) + " ", flush=True)
  if(len(tile) < 6 or len(tile) > 16 ):
    return False

def get_geovalidity_by_mecid(id):
  '''
  This method return a list of tiles for a certain MEC id
  '''
  if (type(id) != int):
    return None
  try:
      cnx = mysql.connector.connect(**config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    return jsonify({'message':"Something went wrong with the database"}), 400
  else:  
      cursor = cnx.cursor()

      statement = "SELECT mec.id, mec.name, mt.tile as mec_tile " \
        "FROM "+config['database']+".MECservers as mec INNER JOIN "+config['database']+".`MEC-tile` as mt on mec.id = mt.mec_id " \
        "where mec.id = " + str(id)
      
      query = (statement)
      
      cursor.execute(query)#, (hire_start, hire_end)
      reslist = []
      for (id, name, mec_tile) in cursor:
          reslist.append(GeolocationTile(len(mec_tile), mec_tile))
      
      cursor.close()
      cnx.close()
      print("MECLIST len " + str(len(reslist)) + " ret " + str(reslist))

      return reslist


def get_mecinstance_by_id(id):
  '''
  This method return a MECInstance by id
  '''
  try:
      cnx = mysql.connector.connect(**config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    return jsonify({'message':"Something went wrong with the database"}), 400
    
  else:  
      cursor = cnx.cursor()

      id = str(id)
      statement = ("SELECT * FROM "+config['database']+".MECservers where id=%s" % id)
      query = (statement)
      
      cursor.execute(query)#, (hire_start, hire_end)
      MEClist = []
      for (id, name, lat, lng, organization, resources, sb_services, props) in cursor:
          
          MEClist.append( MECInstance(id, name, lat, lng,  organization, json.JSONDecoder().decode(resources), json.JSONDecoder().decode(sb_services), json.JSONDecoder().decode(props),      
            get_geovalidity_by_mecid(id)))
      cursor.close()
      return MEClist
  finally:
    cnx.close()


def get_locations():
  '''
  This method returns a list containing all tiles available on MEC registry
  '''
  try:
      cnx = mysql.connector.connect(**config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    return jsonify({'message':"Something went wrong with the database"}), 400
    
  else:  
      cursor = cnx.cursor()

      statement = "SELECT * FROM "+config['database']+".MECservers"
      query = (statement)
      
      cursor.execute(query)#, (hire_start, hire_end)
      Tilelist = []
      for (id, name, lat, lng, organization, resources, sb_services, props) in cursor:
          tilelisttmp=MECInstance(get_geovalidity_by_mecid(id))
          for tile in tilelisttmp.id:
            Tilelist.append(tile.tile_id)
      cursor.close()
      return Tilelist
  finally:
    cnx.close()


def get_mecinstances_locations():
  '''
  This method return a MECInstance by id
  '''
  try:
      cnx = mysql.connector.connect(**config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    return jsonify({'message':"Something went wrong with the database"}), 400
    
  else:  
      cursor = cnx.cursor()

      statement = "SELECT * FROM "+config['database']+".MECservers"
      query = (statement)
      
      cursor.execute(query)#, (hire_start, hire_end)
      MEClist = []
      for (id, name, lat, lng, organization, resources, sb_services, props) in cursor:
          
          MEClist.append( MECInstance(id, name, lat, lng,get_geovalidity_by_mecid(id)))
      cursor.close()
      return MEClist
  finally:
    cnx.close()

def get_mecinstances():
  '''
  This method return a MECInstance by id
  '''
  try:
      cnx = mysql.connector.connect(**config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    return jsonify({'message':"Something went wrong with the database"}), 400
    
  else:  
      cursor = cnx.cursor()

      statement = "SELECT * FROM "+config['database']+".MECservers"
      query = (statement)
      
      cursor.execute(query)#, (hire_start, hire_end)
      MEClist = []
      for (id, name, lat, lng, organization, resources, sb_services, props) in cursor:
          
          MEClist.append( MECInstance(id, name, lat, lng,  organization, json.JSONDecoder().decode(resources), json.JSONDecoder().decode(sb_services), json.JSONDecoder().decode(props),      
            get_geovalidity_by_mecid(id)))
      cursor.close()
      return MEClist
  finally:
    cnx.close()


def get_mecinstances_by_tile(tile,write=0):
  # if write=1, functions has been called to add a tile, if not, only to read or delete
  '''
    This method return a MECInstanceList that contains the MEC in a certain tile(and nested tiles)
  '''

  print("searching for tile "+str(tile))
  print("searching for tile "+str(tile))
  print("searching for tile "+str(tile))
  try:
      cnx = mysql.connector.connect(**config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    return jsonify({'message':"Something went wrong with the database"}), 400

  else:  
      cursor = cnx.cursor()
      lentile=len(tile)
      MEClist = []

      #statement = "SELECT mec.id, mec.name, mec.lat, mec.lng, mec.organization, mec.resources, mec.sb_services, mec.props " \
      #          "FROM "+config['database']+".MECservers as mec INNER JOIN "+config['database']+".`MEC-tile` as mt on mec.id = mt.mec_id " \
      #          "where mt.tile LIKE left('"+tile+"',"+str(lentile)+")" \
      #          "GROUP BY mec.id;"
      if write == 1:
        statement = "SELECT mec.id, mec.name, mec.lat, mec.lng, mec.organization, mec.resources, mec.sb_services, mec.props " \
                  "FROM "+config['database']+".MECservers as mec INNER JOIN "+config['database']+".`MEC-tile` as mt on mec.id = mt.mec_id " \
                  "where mt.tile LIKE '"+tile+"%'" \
                  "GROUP BY mec.id;"
        print("statement 1")
        print(statement)                
        query = (statement)
        cursor.execute(query)#, (hire_start, hire_end)
        for (id, name, lat, lng, organization, resources, sb_services, props) in cursor:

            MEClist.append( MECInstance(id, name, lat, lng,  organization, json.JSONDecoder().decode(resources), json.JSONDecoder().decode(sb_services), json.JSONDecoder().decode(props),      
              get_geovalidity_by_mecid(id)))
      #cursor.close()
      if len(MEClist)==0:
        statement = "SELECT mec.id, mec.name, mec.lat, mec.lng, mec.organization, mec.resources, mec.sb_services, mec.props " \
                "FROM "+config['database']+".MECservers as mec INNER JOIN "+config['database']+".`MEC-tile` as mt on mec.id = mt.mec_id " \
                "where mt.tile LIKE left('"+tile+"',length(mt.tile))" \
                "GROUP BY mec.id;"
        query = (statement)
        cursor.execute(query)#, (hire_start, hire_end)
        print("statement2")
        print(statement)
        for (id, name, lat, lng, organization, resources, sb_services, props) in cursor:
          
          MEClist.append( MECInstance(id, name, lat, lng,  organization, json.JSONDecoder().decode(resources), json.JSONDecoder().decode(sb_services), json.JSONDecoder().decode(props),      
            get_geovalidity_by_mecid(id)))
          
        if len(MEClist)==0:
          statement = "SELECT mec.id, mec.name, mec.lat, mec.lng, mec.organization, mec.resources, mec.sb_services, mec.props " \
              "FROM "+config['database']+".MECservers as mec INNER JOIN "+config['database']+".`MEC-tile` as mt on mec.id = mt.mec_id " \
              "where mt.tile LIKE '"+tile+"%'" \
              "GROUP BY mec.id;"
          query = (statement)
          cursor.execute(query)
          print("statement3")
          print(statement)
          for (id, name, lat, lng, organization, resources, sb_services, props) in cursor:
        
            MEClist.append( MECInstance(id, name, lat, lng,  organization, json.JSONDecoder().decode(resources), json.JSONDecoder().decode(sb_services), json.JSONDecoder().decode(props),      
              get_geovalidity_by_mecid(id)))
      cursor.close()
      return MEClist
  finally:
    cnx.close()


def delete_tile_from_mec(mec_id, tile):
  '''
    This method detele a certain tile for the specified MEC
  '''
  try:
      cnx = mysql.connector.connect(**config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    return jsonify({'message':"Something went wrong with the database"}), 400

  else:  
      cursor = cnx.cursor()

      statement = ("DELETE FROM "+config['database']+".`MEC-tile` WHERE mec_id=%s and tile=%s")
      vals = ( str(mec_id), tile )
      cursor.execute(statement, vals) 
      cnx.commit()
      cursor.close()
      return True
  finally:
    cnx.close()


def check_mec_id_exists(mec_id):
  '''
    Returns True if the mec_id exists
  '''
  try:
      cnx = mysql.connector.connect(**config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    return jsonify({'message':"Something went wrong with the database"}), 400
  else:  
      cursor = cnx.cursor()
      id = str(mec_id)
      query = ("SELECT id FROM "+config['database']+".MECservers where id=%s" % id)
      
      cursor.execute(query)#, (hire_start, hire_end)
      
      exist = cursor.fetchone()

      print("TEST " + str(exist) + " str " + str(mec_id) , flush=True)
      cursor.close()
      if exist is None:
        return False
      else:
        return True
  finally:
      cnx.close()

def check_service_id_exists(mec_id, service_id):
  '''
    Returns True if the service_id exists
  '''
  try:
      cnx = mysql.connector.connect(**config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    return jsonify({'message':"Something went wrong with the database"}), 400
  else:  
      cursor = cnx.cursor()
      query = ("SELECT service_id FROM "+config['database']+".nb_services where mec_id=%s and service_id=%s")
      vals = (mec_id, service_id)
      
      cursor.execute(query, vals)#, (hire_start, hire_end)
      
      exist = cursor.fetchone()

      print("TEST " + str(exist) + " str " + str(service_id) , flush=True)
      cursor.close()
      if exist is None:
        return False
      else:
        return True
  finally:
      cnx.close()
      
      
def get_tiles_by_mecid(mec_id):
  '''
    Returns an array of string containing the tile of a certain mec_id
  '''
  res = []

  try:
      cnx = mysql.connector.connect(**config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    return jsonify({'message':"Something went wrong with the database"}), 400
  else:  
      cursor = cnx.cursor()

      query = ("SELECT mec.id, mt.tile" +
                "FROM "+config['database']+".MECservers as mec INNER JOIN "+config['database']+".`MEC-tile` as mt on mec.id = mt.mec_id " +
                "where mec.id = %s;")
      vals = (mec_id)
      cursor.execute(query, vals)#, (hire_start, hire_end)
      
      for (mec_id, tile) in cursor:
        res.append(tile)    
      cursor.close()
      return res
  finally:
    cnx.close()


def add_tile_mec(mec_id, tile):
  '''
    This method detele a certain tile for the specified MEC
  '''
  print("Adding tile "+str(tile)+" to mec "+str(mec_id))
  if check_is_a_tile(tile) is False:
     return False
  try:
      cnx = mysql.connector.connect(**config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    return False
  else:  
      cursor = cnx.cursor()

      statement = "INSERT INTO "+config['database']+".`MEC-tile`(mec_id, tile) VALUES( %s, %s )"
      vals =  ( str(mec_id), tile )

      print(statement)
    
      cursor.execute(statement, vals) 
      print("CURSOR " + str(cursor) + "\n")
      cnx.commit()
      cursor.close()
      cnx.close()
      return True


def add_new_mecserver(name="", lat="", lng="", organization="", resources="", sb_services="", props="", geolocation=""):
  '''
    This method detele a certain tile for the specified MEC
  '''
  try:
      cnx = mysql.connector.connect(**config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    return -1
  else:  
      cursor = cnx.cursor()
      
      statement = "INSERT INTO "+config['database']+".MECservers( name, lat, lng, organization, resources, sb_services, props) VALUES ( %s, %s, %s, %s, %s, %s, %s)"

      vals =  (  name, lat, lng, organization, json.JSONEncoder().encode(resources), json.JSONEncoder().encode(sb_services), json.JSONEncoder().encode(props) )
      # "DELETE FROM "+config['database']+".`MEC-tile` WHERE mec_id = '%s' and tile = '%s'" % mec_id, tile)
      
      cursor.execute(statement, vals) 
      cnx.commit()
      mec_id = cursor.lastrowid

      #mec_id = cnx.insert_id()
      cursor.close()
      cnx.close()

      for tile in geolocation:
        add_tile_mec(mec_id, tile["tile-id"])

      return mec_id
    
    
def add_new_nbservice( mec_id, service_name, host, port, description, props):
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return jsonify({'message':"Something went wrong with the database"}), 400
    else:  
        cursor = cnx.cursor()
        
        statement = "INSERT INTO "+config['database']+".nb_services( mec_id, service_name, host, port, description, props) VALUES ( %s, %s, %s, %s, %s, %s)"

        vals =  (  mec_id, service_name, host, port, description, props )
        
        try:
          cursor.execute(statement, vals)
        except mysql.connector.IntegrityError as err:
          return jsonify({"message":"Service name already exists, it must be unique"}), 400
          #return "Service name already exists, it must be unique", 400
        
        cnx.commit()
        service_id = cursor.lastrowid
        cursor.close()
        cnx.close()
        return jsonify({ 'service_id':service_id}), 200

def modify_nbservice( mec_id, service_id, service_name, host, port, description, props):
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return jsonify({'message':"Something went wrong with the database"}), 400

    else:  
        cursor = cnx.cursor()
        
        statement = "UPDATE "+config['database']+".nb_services SET service_name=%s, host=%s, port=%s, description=%s, props=%s WHERE mec_id=%s AND service_id=%s"
        vals =  (  service_name, host, port, description, props, mec_id, service_id )
        
        try:
          cursor.execute(statement, vals)
        except mysql.connector.IntegrityError as err:
          return jsonify({"message":"Service name already exists, it must be unique"}), 400
          #return "Service name already exists, it must be unique", 400
        
        cnx.commit()
        cursor.close()
        return True
    finally:
        cnx.close()

def delete_nbservice( mec_id, service_id):
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return jsonify({'message':"Something went wrong with the database"}), 400
    else:  
        cursor = cnx.cursor()
        
        statement = "DELETE FROM "+config['database']+".nb_services WHERE mec_id=%s AND service_id=%s"
        vals =  (  mec_id, service_id )
        
        cursor.execute(statement, vals)
        cursor.close()
        cnx.commit()
        return True
    finally:
        cnx.close()

def get_nbservices( mec_id):
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return jsonify({'message':"Something went wrong with the database"}), 400
    else:  
        cursor = cnx.cursor()
        
        statement = "SELECT * FROM "+config['database']+".nb_services WHERE mec_id=%s"
        vals =  (  mec_id,)
        
        cursor.execute(statement, vals)
        columns = cursor.description
        result = []
        for value in cursor.fetchall():
          tmp = {}
          for (index,column) in enumerate(value):
            tmp[columns[index][0]] = column
          result.append(tmp)
        cursor.close()
        resp = jsonify(result)
        cnx.commit()
        return resp
    finally:
        cnx.close()

def get_nbservice( mec_id, service_id):
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return jsonify({'message':"Something went wrong with the database"}), 400
    else:  
        cursor = cnx.cursor()
        
        statement = "SELECT * FROM "+config['database']+".nb_services WHERE mec_id=%s AND service_id=%s"
        vals =  (  mec_id, service_id )
        
        cursor.execute(statement, vals)
        columns = cursor.description
        result = []
        for value in cursor.fetchall():
          tmp = {}
          for (index,column) in enumerate(value):
            tmp[columns[index][0]] = column
          result.append(tmp)
        cursor.close()
        resp = jsonify(result)
        cnx.commit()
        return resp
    finally:
        cnx.close()
        
  
###################################################

