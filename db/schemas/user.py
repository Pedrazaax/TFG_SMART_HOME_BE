### User schema ###

def home_assistant_schema(ha) -> dict:
    return {
        "tokenHA": ha["tokenHA"],
        "dominio": ha["dominio"]
    }

def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "disabled": user["disabled"],
            "email": user["email"],
            "password": user["password"],
            "pwd2": user["pwd2"],
            "homeAssistant": [home_assistant_schema(ha) for ha in user.get("homeAssistant", ())] if "homeAssistant" in user and user["homeAssistant"] is not None else None}

def users_schema(users) -> list:
    return [user_schema(user) for user in users]


