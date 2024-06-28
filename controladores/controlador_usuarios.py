from bd import obtener_conexion

def obtener_todos_los_usuarios():
    conexion = obtener_conexion()
    users = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT usuario, pass FROM users")
        users = cursor.fetchall()
    conexion.close()
    return users

def actualizar_codeverify_user(username, codeverify):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE users SET codeverify = %s WHERE usuario = %s",
                       (codeverify, username))
    conexion.commit()
    conexion.close()

def confirmar_user(username):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE users SET confirmed = TRUE WHERE usuario = %s",
                       (username,))
    conexion.commit()
    conexion.close()

def verificar_codeverify_user(username, codeverify):
    conexion = obtener_conexion()
    user = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE usuario = %s AND codeverify = %s",
                       (username, codeverify))
        user = cursor.fetchone()
    conexion.close()
    return user

def obtener_user_confirmado(username, password):
    conexion = obtener_conexion()
    user = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM users WHERE usuario = %s AND pass = %s AND confirmed = TRUE", 
            (username, password)
        )
        user = cursor.fetchone()
    conexion.close()
    return user


def obtener_user_por_username(username):
    conexion = obtener_conexion()
    user= None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, usuario, pass, token,codeverify FROM users WHERE usuario = %s",(username,))
        user = cursor.fetchone()
    conexion.close()
    return user

def obtener_user_por_id(id):
    conexion = obtener_conexion()
    user = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, usuario, pass FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()
    conexion.close()
    return user

def insertar_user(username, epassword):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO users(usuario, pass) VALUES (%s, %s)",
                       (username, epassword))
    conexion.commit()
    conexion.close()

def actualizar_token_user(username, token):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE users SET token =%s WHERE usuario = %s ",
                       (token, username))
    conexion.commit()
    conexion.close()


