'''### User schema ###'''

def home_assistant_schema(ha) -> dict:
    '''Devuelve un diccionario con los valores correctos de homeAssistant'''
    if isinstance(ha, list) and len(ha) == 2:
        return {"tokenHA": ha[0], "dominio": ha[1]}  
    return None

def user_schema(user) -> dict:
    '''Devuelve un diccionario con los valores correctos de user'''
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "disabled": user["disabled"],
        "email": user["email"],
        "password": user["password"],
        "pwd2": user["pwd2"],
        "homeAssistant": home_assistant_schema(
            user.get("homeAssistant")
            ) if "homeAssistant" in user and user["homeAssistant"] is not None else None
    }

def users_schema(users) -> list:
    '''Devuelve una lista de diccionarios con los valores correctos de users'''
    return [user_schema(user) for user in users]
