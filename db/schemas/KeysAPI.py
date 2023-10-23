### KeysAPI_schema ###

def keysAPI_schema(keysAPI) -> dict:
    return {"id": str(keysAPI["_id"]),
            "username": keysAPI["username"],
            "access_id": keysAPI["access_id"],
            "access_key": keysAPI["access_key"],
            "api_endpoint": keysAPI["api_endpoint"],
            "mq_endpoint": keysAPI["mq_endpoint"]}