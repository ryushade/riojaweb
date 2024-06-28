from bd import obtener_conexion
import random
import hashlib

def generar_codverificacion():
    return random.randint(100000, 999999)

def encript_passw(passw):
    return hashlib.sha256(passw.encode()).hexdigest()

def insertar_usuario(username, passw):
    codeverify=generar_codverificacion()
    estado="I"
    epassw=encript_passw(passw)
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuarios(username, passw, codeverify, estado) values (%s, %s, %s, %s)",
                        (username, epassw, codeverify, estado))
    conexion.commit()
    conexion.close()
    return codeverify


def verificar_usuario(username, codeverify):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE username = %s AND codeverify = %s", (username, codeverify))
        user = cursor.fetchone()
        if user:
            cursor.execute("UPDATE usuarios SET estado = %s WHERE username = %s", ("A", username))
            conexion.commit()
            return True
        else:
            return False

def listarusuarios():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT* FROM usuarios where estado='A'")
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

def obtener_usuario_por_username(username):
    conexion = obtener_conexion()
    user = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, username, passw FROM usuarios where username = %s and estado='A'", (username,))
        user = cursor.fetchone()
    conexion.close()
    return user

def obtener_usuario_por_id(id):
    conexion = obtener_conexion()
    user = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, username, passw FROM usuarios WHERE id = %s", (id,))
        user = cursor.fetchone()
    conexion.close()
    return user