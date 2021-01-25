#!/usr/bin/python3
# -*- coding: utf-8 -*-

import signal
import time
import traceback
import json
import asyncio
import nibeuplink
import paho.mqtt.publish as mqtt_publish
import paho.mqtt.client as mqtt_client

# external files/classes
import logger
import serviceReport
import settings
import nibeIds

# Temp-Humi Sensoren THGR810

current_sec_time = lambda: int(round(time.time()))
current_milli_time = lambda: int(round(time.time() * 1000))

loop = None
Exit = False
# nibeDeviceGetDelay = current_sec_time()
#nibeDeviceGetDelay = 0
dataRxWatchTimer = current_sec_time()


def signal_handler(_signal, frame):
    global Exit

    print('You pressed Ctrl+C!')
    loop.stop()
    Exit = True


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT Client connected successfully")
        client.subscribe([(settings.MQTT_TOPIC_CHECK, 1)])
    else:
        print(("ERROR: MQTT Client connected with result code %s " % str(rc)))


# The callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(('ERROR: Received ' + msg.topic + ' in on_message function' + str(msg.payload)))


def sendNibeTempDevice(deviceName, value):
    sensorData = {}
    sensorData['Temperature'] = value
    mqtt_publish.single("huis/Nibe/%s/temp" % deviceName.replace(' ', '-'), json.dumps(sensorData, separators=(', ', ':')), hostname=settings.MQTT_ServerIP, retain=True)


###
# Initalisation ####
###
logger.initLogger(settings.LOG_FILENAME)

# Init signal handler, because otherwise Ctrl-C does not work
signal.signal(signal.SIGINT, signal_handler)

# Give Home Assistant and Mosquitto the time to startup
time.sleep(2)

# First start the MQTT client
client = mqtt_client.Client()
client.message_callback_add(settings.MQTT_TOPIC_CHECK, serviceReport.on_message_check)
client.on_connect = on_connect
client.on_message = on_message
client.connect(settings.MQTT_ServerIP, settings.MQTT_ServerPort, 60)
client.loop_start()


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
def token_read():
    try:
        with open(settings.AUTH_FILE, "r") as myfile:
            return json.load(myfile)
    except FileNotFoundError:
        return None


def token_write(token):
    with open(settings.AUTH_FILE, "w") as myfile:
        json.dump(token, myfile, indent=2)


async def run():
    # global nibeDeviceGetDelay
    global dataRxWatchTimer

    serviceReport.systemWatchTimer = current_sec_time()

    scope = ["READSYSTEM"]
    try:
        async with nibeuplink.UplinkSession(
            client_id=settings.NIBE_IDENTIFIER,
            client_secret=settings.NIBE_SECRET,
            redirect_uri=settings.NIBE_CALLBACK_URL,
            access_data=token_read(),
            access_data_write=token_write,
            scope=scope,
        ) as session:

            if not session.access_data:
                auth_uri = session.get_authorize_url()
                print(auth_uri)
                result = input("Enter full redirect url: ")
                await session.get_access_token(session.get_code_from_url(result))

            uplink = nibeuplink.Uplink(session)

            while not Exit:
                todo = []
                #Get system status
                #todo.extend([uplink.get_system(settings.NIBE_CLIENT_ID)])
                #print("get systemStatus")

                for id in nibeIds.idToDeviceName:
                    # if id == 10012: # 'CompressorGeblokkeerd':
                    #     #print("get CompressorGeblokkeerd")
                    #     todo.extend([uplink.get_parameter(settings.NIBE_CLIENT_ID, id)])
                    # else:
                    #     # Other devices
                    #     if (current_sec_time() - nibeDeviceGetDelay) > 900:
                    #print("get %s" % id)
                    todo.extend([uplink.get_parameter(settings.NIBE_CLIENT_ID, id)])

                # if (current_sec_time() - nibeDeviceGetDelay) > 900:
                todo.extend([uplink.get_system(settings.NIBE_CLIENT_ID)])
                # print("get systemStatus")

                #print("Get data")
                nibeData = {}
                responses = await asyncio.gather(*todo)
                #print(responses)
                if responses != "[None]":
                    for response in responses:
                        try:
                            if 'systemId' in response:
                                #print(json.dumps(response, indent=1))
                                #System response
                                if response['connectionStatus'] == 'ONLINE':
                                    nibeData['ONLINE'] = 1
                                else:
                                    nibeData['ONLINE'] = 0

                                #print("Online: %s" % response['connectionStatus'])
                            #if connectionOnline and 'parameterId' in response:
                            if 'parameterId' in response:
                                #Get the sensor data

                                #print(json.dumps(response, indent=1))
                                id = response['parameterId']
                                deviceName = nibeIds.idToDeviceName[id]
                                value = response['value']
                                # print("%s" % deviceName)
                                if id == 10012: # 'CompressorGeblokkeerd':
                                    value = response['rawValue']
                                    mqtt_publish.single("huis/Nibe/Actief-CompressorGeblokkeerd/rx", int(value), hostname=settings.MQTT_ServerIP, retain=True)
                                else:
                                    if deviceName in nibeIds.tempDevices:
                                        #Send as a seperate MQTT msg
                                        sendNibeTempDevice(deviceName, value)
                                    else:
                                        if value in nibeIds.valueConversion:
                                            value = nibeIds.valueConversion[value]
                                        if deviceName in nibeIds.deviceIntType:
                                            value = int(value)
                                            # print("%s: %d" % (deviceName, value))

                                        nibeData[deviceName] = value
                                    # if deviceName is not 'CompressorGeblokkeerd':
                                    # nibeDeviceGetDelay = current_sec_time()

                                # Data received reset timeout
                                dataRxWatchTimer = current_sec_time()

                        # except TypeError:
                        #     print(a)
                        except Exception as e:
                            print("Exception: " + str(e))
                            traceback.print_exc()

                if nibeData:
                    #Send MQTT Nibe JSON msg
                    jsonMsg = json.dumps(nibeData)
                    mqtt_publish.single("huis/Nibe/Warmtepomp/rx", jsonMsg, hostname=settings.MQTT_ServerIP, retain=True)

                #  Check the Nibe_MQTT Rx timeout
                if (current_sec_time() - serviceReport.systemWatchTimer) > 3600:
                    # Reset the data timeout timer
                    dataRxWatchTimer = current_sec_time()

                    #Report failure to Home Logic system check
                    serviceReport.sendFailureToHomeLogic(serviceReport.ACTION_RESTART, 'Nibe data receive timeout (60 min no data received)!')

                serviceReport.systemWatchTimer = current_sec_time()

                await asyncio.sleep(900)
    except Exception as e:
        print("Exception: " + str(e))
        traceback.print_exc()

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(run())
    loop.run_forever()
except Exception as arg:
    print("%s" % str(arg))
    traceback.print_exc()

print("Clean Exit!")
