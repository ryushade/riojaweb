from bd import obtener_conexion
import hashlib

def obtener_user_por_username(username):
    conexion = obtener_conexion()
    user = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT usuario, password_hash, codigo_verificacion, estado_verificado FROM usuarios WHERE usuario = %s", (username,))
        user = cursor.fetchone()
    conexion.close()
    return user

def obtener_user_por_id(user_id):
    conexion = obtener_conexion()
    user = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT usuario, password_hash, estado_verificado FROM usuarios WHERE id = %s", (user_id,))
        user = cursor.fetchone()
    conexion.close()
    return user

def registrar_usuario(username, hashed_password):
    conexion = obtener_conexion()
    user_id = None
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuarios (usuario, password_hash, codigo_verificacion, estado_verificado) VALUES (%s, %s, %s, %s)", 
                       (username, hashed_password, 0, False))
        user_id = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return user_id

def guardar_codigo_verificacion(user_id, codeverify):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET codigo_verificacion = %s WHERE id = %s", (codeverify, user_id))
    conexion.commit()
    conexion.close()

def verificar_codigo(username, codeverify):
    conexion = obtener_conexion()
    verificado = False
    with conexion.cursor() as cursor:
        cursor.execute("SELECT codigo_verificacion FROM usuarios WHERE usuario = %s", (username,))
        user = cursor.fetchone()
        if user and user['codigo_verificacion'] == codeverify:
            cursor.execute("UPDATE usuarios SET estado_verificado = %s WHERE usuario = %s", (True, username))
            verificado = True
    conexion.commit()
    conexion.close()
    return verificado

def obtener_usuarios_verificados():
    conexion = obtener_conexion()
    users = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT usuario, password_hash FROM usuarios WHERE estado_verificado = %s", (True,))
        users = cursor.fetchall()
    conexion.close()
    return users

def actualizartoken_user(username, token):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET token = %s WHERE usuario = %s", (token, username))
    conexion.commit()
    conexion.close()
