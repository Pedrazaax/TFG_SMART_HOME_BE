from tuya_connector import TuyaOpenAPI, TUYA_LOGGER
from properties import ACCESS_ID, ACCESS_KEY, API_ENDPOINT
import logging

#Login en Tuya OpenAPI
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

#JSON Cloud
"""[
  {
    "code": "switch_1",
    "value": false
  },
  {
    "code": "cou
    ntdown_1",
    "value": 0
  },
  {
    "code": "relay_status"
  },
  {
    "code": "overcharge_switch",
    "value": false
  },
  {
    "code": "light_mode"
  },
  {
    "code": "child_lock",
    "value": false
  },
  {
    "code": "cycle_time"
  },
  {
    "code": "random_time"
  },
  {
    "code": "switch_inching"
  }
]"""

flag=True
while True:
    input('Pulsa enter para encender/apagar el enchufe')
    flag = not flag
    commands = {'commands': [{'code': 'switch_1', 'value': flag}]}
    openapi.post('/v1.0/iot-03/devices/{}/commands'.format("bfca08a265208cdccdiz2g"), commands)