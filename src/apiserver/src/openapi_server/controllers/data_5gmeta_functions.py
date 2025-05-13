import connexion
import six
import os
import logging
import json
import mysql.connector

from mysql.connector import errorcode
from flask import jsonify
from types import SimpleNamespace
from openapi_server import util
from openapi_server.models.mec_instance import MECInstance  # noqa: E501
from openapi_server.models.mec_instance_list import MECInstanceList  # noqa: E501
from openapi_server.models.geolocation_tile import GeolocationTile
from openapi_server.models.geolocation_tile_list import GeolocationTileList
from openapi_server.models.sb_service import SBService


config = {
  'user': os.environ['DB_USER'],
  'password': os.environ['DB_PASSWORD'],
  'host': os.environ["DB_HOST"],
  'database': os.environ["DISCOVERY_DB_NAME"],
  'raise_on_warnings': True
}


logger = logging.getLogger(__name__)


def is_valid_mecID(mec_id):
  return isinstance(mec_id, int)


def delete_mec(cursor, mec_id, *args):
  for arg in args:
    statement = "DELETE FROM " + config['database'] + arg + " WHERE mec_id=" + mec_id
    cursor.execute(statement)
    cnx.commit()


def process_statement(function, mec_id=None,  *args):

  logger.info("DELETE MEC " + mec_id)

  if not is_valid_mecID(mec_id):
    logger.error("NOT VALID mec_id "+mec_id)
    return jsonify({'message':"not valid mec_id"}), 400

  try:
      cnx = mysql.connector.connect(**config)
  except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
          logger.error("Invalide username or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
          logger.error("Database does not exist")
      else:
          logger.debug(err)
      return jsonify({'message':"Error deleting mec_id"}), 400
  else:

      cursor = cnx.cursor()

      ret = function (cursor, mec_id, *args )

      cursor.close()

      return ret
  finally:
      cnx.close()


def delete_mec_from_db(mec_id):
  '''
  Check if a tile have some characteristics
  '''
  logger.info("DELETE MEC " + mec_id)
  return process_statement(delete_mec, mec_id,  ".`MEC-tile`", ".`nb_services`", ".MECservers ")


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
  logger.info("CHECK TILE len " + str(len(tile)) + " ", flush=True)
  return (len(tile) < 6 or len(tile) > 16 )


def get_rlist(cursor, mec_id):
  statement = "SELECT mec.id, mec.name, mt.tile as mec_tile " \
        "FROM "+config['database']+".MECservers as mec INNER JOIN "+config['database']+".`MEC-tile` as mt on mec.id = mt.mec_id " \
        "where mec.id = " + str(mec_id)

  query = (statement)

  cursor.execute(query)#, (hire_start, hire_end)
  reslist = []
  for (mecid, name, mec_tile) in cursor:
        reslist.append(GeolocationTile(len(mec_tile), mec_tile))
  logger.debug("MECLIST len " + str(len(reslist)) + " ret " + str(reslist))
  return reslist


def get_geovalidity_by_mecid(mecid):
  '''
  This method return a list of tiles for a certain MEC id
  '''
  return process_statement(get_rlist, mec_id)


def instance_by_id (mec_id, cursor):
      mecid = str(mecid)
      statement = ("SELECT * FROM "+config['database']+".MECservers where id=%s" % mecid)
      query = (statement)

      cursor.execute(query)#, (hire_start, hire_end)
      MEClist = []
      for (id, name, lat, lng, organization, resources, sb_services, props) in cursor:

          MEClist.append( MECInstance(mecid, name, lat, lng,  organization, json.JSONDecoder().decode(resources), json.JSONDecoder().decode(sb_services), json.JSONDecoder().decode(props),
            get_geovalidity_by_mecid(mecid)))

      return MEClist


def get_mecinstance_by_id(mec_id):
  '''
  This method return a MECInstance by mec_id
  '''
  return process_statement(instance_by_id, mec_id,)


def locations(cursor):
    statement = "SELECT * FROM "+config['database']+".MECservers"
      query = (statement)

      cursor.execute(query)#, (hire_start, hire_end)
      Tilelist = []
      for (mec_id, name, lat, lng, organization, resources, sb_services, props) in cursor:
          tilelisttmp=MECInstance(get_geovalidity_by_mecid(mec_id))
          for tile in tilelisttmp.mec_id:
            Tilelist.append(tile.tile_id)

      return Tilelist


def get_locations():
  '''
  This method returns a list containing all tiles available on MEC registry
  '''
  process_statement(locations)


def meclocations(cursor):
    statement = "SELECT * FROM "+config['database']+".MECservers"
      query = (statement)

      cursor.execute(query)#, (hire_start, hire_end)
      MEClist = []
      for (mec_id, name, lat, lng, organization, resources, sb_services, props) in cursor:

          MEClist.append( MECInstance(mec_id, name, lat, lng,get_geovalidity_by_mecid(mec_id)))

      return MEClist

def get_mecinstances_locations():
  '''
  This method return a MECInstance by id
  '''
  return process_statement(meclocations)


def mecfunction(cursor):
      statement = "SELECT * FROM "+config['database']+".MECservers"
      query = (statement)

      cursor.execute(query)#, (hire_start, hire_end)
      MEClist = []
      for (mec_id, name, lat, lng, organization, resources, sb_services, props) in cursor:

          MEClist.append( MECInstance(mec_id, name, lat, lng,  organization, json.JSONDecoder().decode(resources), json.JSONDecoder().decode(sb_services), json.JSONDecoder().decode(props),
            get_geovalidity_by_mecid(mec_id)))
      cursor.close()
      return MEClist

def get_mecinstances():
  '''
  This method return a MECInstance by id
  '''
  return process_statement(mecfunction)


def mectile(cursor, write):
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

      return MEClist

def get_mecinstances_by_tile(tile,write=0):
  # if write=1, functions has been called to add a tile, if not, only to read or delete
  '''
    This method return a MECInstanceList that contains the MEC in a certain tile(and nested tiles)
  '''

  logger.info("searching for tile "+str(tile))
  return process_statement (cursor, mectile)


def deletetitemec(cursor, mec_id,tile):
      statement = ("DELETE FROM "+config['database']+".`MEC-tile` WHERE mec_id=%s and tile=%s")
      vals = ( str(mec_id), tile )
      cursor.execute(statement, vals)
      cnx.commit()
      cursor.close()
      return True

def delete_tile_from_mec(mec_id, tile):
  '''
    This method detele a certain tile for the specified MEC
  '''
  return process_statement(deletetitemec, mec_id, tile)


def existsmec(cursor, mec_id):

      mec_id = str(mec_id)
      query = ("SELECT id FROM "+config['database']+".MECservers where id=%s" % mec_id)

      cursor.execute(query)#, (hire_start, hire_end)

      exist = cursor.fetchone()

      logger.info("TEST " + str(exist) + " str " + str(mec_id) , flush=True)

      return exist is None


def existsservice(cursor, service_id):
      query = ("SELECT service_id FROM "+config['database']+".nb_services where mec_id=%s and service_id=%s")
      vals = (mec_id, service_id)

      cursor.execute(query, vals)#, (hire_start, hire_end)

      exist = cursor.fetchone()

      logger.info("TEST " + str(exist) + " str " + str(service_id) , flush=True)

      return exist is None


def check_mec_id_exists(mec_id):
  '''
    Returns True if the mec_id exists
  '''
  return process_statement(existsmec, mec_id)


def check_service_id_exists(mec_id, service_id):
  '''
    Returns True if the service_id exists
  '''
  process_statement(existsservice, service_id)


def tilesmec(cursor, mec_id):
      res = []
      query = ("SELECT mec.id, mt.tile" +
                "FROM "+config['database']+".MECservers as mec INNER JOIN "+config['database']+".`MEC-tile` as mt on mec.id = mt.mec_id " +
                "where mec.id = %s;")
      vals = (mec_id)
      cursor.execute(query, vals)#, (hire_start, hire_end)

      for (mec_id, tile) in cursor:
        res.append(tile)
      return res

def get_tiles_by_mecid(mec_id):
  '''
    Returns an array of string containing the tile of a certain mec_id
  '''
  return process_statement(tilesmec, mec_id)

def addtilemec(cursor, mec_id, tile):
      statement = "INSERT INTO "+config['database']+".`MEC-tile`(mec_id, tile) VALUES( %s, %s )"
      vals =  ( str(mec_id), tile )

      print(statement)

      cursor.execute(statement, vals)
      print("CURSOR " + str(cursor) + "\n")
      cnx.commit()
      return True

def add_tile_mec(mec_id, tile):
  '''
    This method detele a certain tile for the specified MEC
  '''

  if check_is_a_tile(tile) is False:
    return False

  logger.info("Adding tile "+str(tile)+" to mec "+str(mec_id))

  return process_statement(addtilemec, mec_id, tile)


def addnewmecserver(cursor,  name="", lat="", lng="", organization="", resources="", sb_services="", props="", geolocation=""):

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


def add_new_mecserver(name="", lat="", lng="", organization="", resources="", sb_services="", props="", geolocation=""):
  '''
    This method detele a certain tile for the specified MEC
  '''
  return process_statement(addnewmecserver, name="", lat="", lng="", organization="", resources="", sb_services="", props="", geolocation="")


def addnewnbservice(cursor, mec_id, service_name, host, port, description, props ):
        statement = "INSERT INTO "+config['database']+".nb_services( mec_id, service_name, ip, port, description, props) VALUES ( %s, %s, %s, %s, %s, %s)"

        vals =  (  mec_id, service_name, ip, port, description, props )

        try:
          cursor.execute(statement, vals)
        except mysql.connector.IntegrityError as err:
          return jsonify({"message":"Service name already exists, it must be unique"}), 400
          #return "Service name already exists, it must be unique", 400

        cnx.commit()
        service_id = cursor.lastrowid
        return jsonify({ 'service_id':service_id}), 200


def add_new_nbservice( mec_id, service_name, ip, port, description, props):
    return process_statement(addnewnbservice, mec_id, service_name, ip, port, description, props)


def modifynbservice(cursor, mec_id, service_id, service_name, ip, port, description, props):
        statement = "UPDATE "+config['database']+".nb_services SET service_name=%s, ip=%s, port=%s, description=%s, props=%s WHERE mec_id=%s AND service_id=%s"
        vals =  (  service_name, ip, port, description, props, mec_id, service_id )

        try:
          cursor.execute(statement, vals)
        except mysql.connector.IntegrityError as err:
          return jsonify({"message":"Service name already exists, it must be unique"}), 400
          #return "Service name already exists, it must be unique", 400

        cnx.commit()
        return True


def deletenbservice (cursor, mec_id, service_id):
        statement = "DELETE FROM "+config['database']+".nb_services WHERE mec_id=%s AND service_id=%s"
        vals =  (  mec_id, service_id )

        cursor.execute(statement, vals)
        return True

def modify_nbservice( mec_id, service_id, service_name, ip, port, description, props):
  return process_statement(modifynbservice, mec_id, service_id, service_name, ip, port, description, props)


def delete_nbservice( mec_id, service_id):
  return process_statement(deletenbservice, mec_id, service_id)


def nbservicesget(cursor, mec_id):
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

def nbservice(cursor, mec_id, service_id):
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

        resp = jsonify(result)

        return resp

def get_nbservices( mec_id):
  return process_statement(nbservicesget, mec_id)


def get_nbservice( mec_id, service_id):
  return process_statement(nbservice, mec_id, service_id)
