'''
Conexión a la base de datos de MongoDB
'''
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://smartDB:tn2kjOysIfW60VnF@myhomeiqdb.6wzf76b.mongodb.net/?retryWrites=true&w=majority"
    ).myhomeiq

clientConsumoLocal = MongoClient(
    "mongodb+srv://smartDB:tn2kjOysIfW60VnF@myhomeiqdb.6wzf76b.mongodb.net/?retryWrites=true&w=majority"
    ).myhomeiqConsumoLocal
