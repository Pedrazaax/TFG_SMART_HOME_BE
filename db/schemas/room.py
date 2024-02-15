### Room schema ###

def room_schema(room ) -> dict:
    return {"id": str(room["_id"]),
            "name": room["name"]}

def rooms_schema(users) -> list:
    return [room_schema(user) for user in users]