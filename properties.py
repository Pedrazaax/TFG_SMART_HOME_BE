'''
Este módulo se encarga de gestionar la conexión con la API de Tuya.
'''
import os
from dotenv import load_dotenv

from tuya_connector import TuyaOpenAPI

load_dotenv()

API_ENDPOINT = os.getenv("API_ENDPOINT")
ACCESS_ID = os.getenv("ACCESS_ID")
ACCESS_KEY = os.getenv("ACCESS_KEY")

flag : bool = False

def get_openapi_instance():
    '''Instancia la conexión con la API de Tuya.'''
    global flag    
    if not flag:
        openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
        openapi.connect()
        flag = True

    return openapi
