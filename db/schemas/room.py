'''### Room schema ###'''

def room_schema(room ) -> dict:
    '''Devuelve un esquema de habitación'''
    return {"id": str(room["_id"]),
            "name": room["name"]}

def rooms_schema(users) -> list:
    '''Devuelve una lista de esquemas de habitaciones'''
    return [room_schema(user) for user in users]
