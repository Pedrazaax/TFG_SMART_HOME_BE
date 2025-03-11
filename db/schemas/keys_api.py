'''### KeysAPI_schema ###'''

def keys_api_schema(keys_api) -> dict:
    '''Esquema de la colección KeysAPI'''
    return {"id": str(keys_api["_id"]),
            "username": keys_api["username"],
            "access_id": keys_api["access_id"],
            "access_key": keys_api["access_key"],
            "api_endpoint": keys_api["api_endpoint"],
            "mq_endpoint": keys_api["mq_endpoint"]}
