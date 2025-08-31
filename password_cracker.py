import hashlib


def obtener_passwords():
    passwords_sin_salts={}
    passwords_con_salts={}

    with open("known-salts.txt") as fs:
        salts = [line.strip() for line in fs]

    with open("top-10000-passwords.txt") as fp:
        for line_password in fp:
            password_limpia = line_password.strip()
            hash_pwd = hashlib.sha1(password_limpia.encode()).hexdigest()
            passwords_sin_salts[hash_pwd] = password_limpia

           
            for salt in salts:
                built_with_salt1 = f'{salt}{password_limpia}'
                built_with_salt2 = f'{password_limpia}{salt}'
                hash_with_salt1 = hashlib.sha1(built_with_salt1.encode()).hexdigest()
                hash_with_salt2 = hashlib.sha1(built_with_salt2.encode()).hexdigest()
                passwords_con_salts[hash_with_salt1] = password_limpia
                passwords_con_salts[hash_with_salt2] = password_limpia

    return {"passwords_sin_salts":passwords_sin_salts,"passwords_con_salts":passwords_con_salts}           

        
diccionario_passwords=obtener_passwords()

       

def crack_sha1_hash(hash, use_salts = False):
    diccionario = (
        diccionario_passwords["passwords_con_salts"]
        if use_salts
        else diccionario_passwords["passwords_sin_salts"]
    )
    return diccionario.get(hash, "PASSWORD NOT IN DATABASE")
        

