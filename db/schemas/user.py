### User schema ###

def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "disabled": user["disabled"],
            "email": user["email"],
            "password": user["password"],
            "pwd2": user["pwd2"]}


def users_schema(users) -> list:
    return [user_schema(user) for user in users]
