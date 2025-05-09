
# Some sample code for the cosumere can be find 
# here https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/json_consumer.py

from confluent_kafka import Consumer, KafkaException
import sys
import getopt
import json
import logging
from pprint import pformat

from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka.cimpl import TopicPartition
import sys
import base64
import requests
import time

#from proton.handlers import MessagingHandler
import proton
import random
import string

# https://stackoverflow.com/questions/2511222/efficiently-generate-a-16-character-alphanumeric-string
def generateRandomGroupId (length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

#if len(sys.argv) != 5:
#    print("Usage: python3 cits-consumer.py topic platformaddress bootstrap_port registry_port ")
#    exit()

#topic=str(sys.argv[1])
#platformaddress=str(sys.argv[2])
#bootstrap_port=str(sys.argv[3])
#schema_registry_port=str(sys.argv[4])


tile = "031333123201"
instance_type = "small" #small
platformaddress = "<ip>"
bootstrap_port = "31090"
schema_registry_port = "31081"
platform_user = "<user>"
platform_password = "<password>"
group_id = "group1"
topic="5GMETA_1011_CITS_MEDIUM_34"

c = AvroConsumer({
    'bootstrap.servers': platformaddress+ ':' + bootstrap_port,
    'schema.registry.url':'http://'+platformaddress+':' + schema_registry_port, 
    'group.id': topic+'_'+generateRandomGroupId(4),
    'api.version.request': True,
    'auto.offset.reset': 'earliest'
})

c.subscribe([topic.upper()])

print("Subscibed topics: " + str(topic))
print("Running...")

i = 0

while True:
    msg = c.poll(1.0)

    if msg is None:
        #print("Empty msg: " + str(msg) );
        print(".",  end="", flush=True)
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue
    print("NEW MESSAGE")
    currentTime=time.time_ns() // 1_000_000

    sys.stderr.write('\n%% %s [%d] at offset %d with key %s:\n\n' %
        (msg.topic(), msg.partition(), msg.offset(), str(msg.key())))
    
    # The AVRO Message here in mydata
    mydata = msg.value() # .decode('latin-1') #.replace("'", '"')
    #print( "Message: " + str(mydata))
    #print(mydata['PROPERTIES'])

    # The QPID proton message: this is the message sent from the S&D to the MEC
    #print(mydata)
    raw_sd = mydata['BYTES_PAYLOAD']
    msg_sd = proton.Message()
    proton.Message.decode(msg_sd, raw_sd)

    # The msg_sd.body contains the data of the sendor
    bodyJson=json.loads(msg_sd.body)
    print("RECEIVED_TIME")
    print(currentTime)
    print("MESSAGE_TIMESTAMP")
    message_timestamp=mydata['MESSAGE_TIMESTAMP']
    print(message_timestamp)
    print("ORIGIN_TIME")
    origin_time=bodyJson['cam']['camParameters']['lowFrequencyContainer']['basicVehicleContainerLowFrequency']['pathHistory'][0]['pathDeltaTime']
    print(origin_time)
    print("MESSAGE_ID")
    message_id=bodyJson['header']['stationID']
    print(message_id)
    latency1=message_timestamp-origin_time
    print("LATENCY1 milliseconds")
    print(latency1)
    latency2=currentTime-origin_time
    print("LATENCY2 milliseconds")
    print(latency2)    
    '''print("Size " + str(sys.getsizeof(msg_sd.body)))

    outfile = open("../output/body_"+str(i)+".txt", 'w')
    i=i+1
    try:
        outfile.write(msg_sd.body)
    except:
        print("An error decoding the message happened!")
        
    outfile.close()
    '''
c.close()
