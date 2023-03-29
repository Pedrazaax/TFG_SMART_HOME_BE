import logging
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER
from properties import ACCESS_ID, ACCESS_KEY, API_ENDPOINT

# Enable debug log
TUYA_LOGGER.setLevel(logging.DEBUG)

# Init OpenAPI and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# Set up device_id
DEVICE_ID ="bfca08a265208cdccdiz2g"

# Call APIs from Tuya
# Get the device information
response = openapi.get("/v1.0/iot-03/devices/{}".format(DEVICE_ID))

# Get the instruction set of the device
response = openapi.get("/v1.0/iot-03/devices/{}/functions".format(DEVICE_ID))

# Send commands
commands = {'commands': [{'code': 'switch_led', 'value': False}]}
openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)

# Get the status of a single device
response = openapi.get("/v1.0/iot-03/devices/{}/status".format(DEVICE_ID))
