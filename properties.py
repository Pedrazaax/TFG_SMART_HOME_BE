#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from tuya_connector import TuyaOpenAPI

ACCESS_ID = "q5r8cmmu7epcxttt7vgf"
ACCESS_KEY = "85a47365a7c04bc8ba9dfce9823c2038"
API_ENDPOINT = "https://openapi.tuyaeu.com"
MQ_ENDPOINT = "wss://mqe.tuyaeu.com:8285/"

API_KEY_NVD = "747ab5fb-9faa-48a1-bf10-5e5325b13648"

flag = False

def get_openapi_instance():
    global flag
    
    if not flag:
        openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
        openapi.connect()
        flag = True

    return openapi