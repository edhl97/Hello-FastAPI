# This function allows to convert the user from database in an object type user
def user_schema(user)  -> dict:
    return {"id": str(user["_id"]), # The direct transformation to str is needed because of the way of saving the user in the database
            "username":user["username"],
            "email":user["email"]}

def users_schema(users) -> list:
    return [user_schema(user) for user in users]