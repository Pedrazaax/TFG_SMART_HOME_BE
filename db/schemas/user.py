### User schema ###

def home_assistant_schema(ha) -> dict:
    if isinstance(ha, list) and len(ha) == 2:  # Verifica si ha es una lista de longitud 2
        return {"tokenHA": ha[0], "dominio": ha[1]}  # Devuelve un diccionario con los valores correctos
    return None


def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "disabled": user["disabled"],
        "email": user["email"],
        "password": user["password"],
        "pwd2": user["pwd2"],
        "homeAssistant": home_assistant_schema(user.get("homeAssistant")) if "homeAssistant" in user and user["homeAssistant"] is not None else None
    }

def users_schema(users) -> list:
    return [user_schema(user) for user in users]


