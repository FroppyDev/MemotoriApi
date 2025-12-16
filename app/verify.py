def verify_password(plain_password, hashed_password):

    if plain_password + "fakehash"  == hashed_password:
        return True
    else:
        return False