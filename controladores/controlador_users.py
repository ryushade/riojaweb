from bd import obtener_conexion
import hashlib
import random

def registrar_usuario(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    codigo_verificacion = random.randint(100000, 999999)
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO usuarios(usuario, password_hash, codigo_verificacion, estado_verificado) VALUES (%s, %s, %s, %s)",
            (username, password_hash, codigo_verificacion, False))
    conexion.commit()
    conexion.close()
    return codigo_verificacion

def confirmar_usuario(username, codigo_verificacion):
    conexion = obtener_conexion()
    verificado = False
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE usuarios SET estado_verificado = %s WHERE usuario = %s AND codigo_verificacion = %s",
            (True, username, codigo_verificacion))
        if cursor.rowcount == 1:
            verificado = True
    conexion.commit()
    conexion.close()
    return verificado

def obtener_usuario_por_username(username):
    conexion = obtener_conexion()
    user = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT usuario, password_hash, codigo_verificacion, estado_verificado FROM usuarios WHERE usuario = %s", (username,))
        user = cursor.fetchone()
    conexion.close()
    return user
