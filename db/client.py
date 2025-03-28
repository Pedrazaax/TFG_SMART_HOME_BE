'''
Conexión a la base de datos de MongoDB
'''
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
URL = os.getenv("URL_DB")

client = MongoClient(URL).myhomeiq

clientConsumoLocal = MongoClient(URL).myhomeiqConsumoLocal
