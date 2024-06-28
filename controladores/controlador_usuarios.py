from bd import obtener_conexion
from clases.clase_usuario import clsUsuario
import secrets
import string

def obtener_user_por_username(username):
    try:
        conexion = obtener_conexion()
        user = None
        with conexion.cursor() as cursor:
            cursor.execute("SELECT usuario, password_hash, codigo_verificacion, estado_verificado, token FROM usuarios WHERE usuario = %s", (username,))
            user_data = cursor.fetchone()
        conexion.close()
        if user_data:
            user = clsUsuario(user_data['usuario'], user_data['password_hash'], user_data['codigo_verificacion'], user_data['estado_verificado'], user_data['token'])
        return user
    except Exception as e:
        print(f"Error en obtener_user_por_username: {e}")
        return None

def obtener_user_por_id(user_id):
    try:
        conexion = obtener_conexion()
        user = None
        with conexion.cursor() as cursor:
            cursor.execute("SELECT usuario, password_hash, estado_verificado FROM usuarios WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
        conexion.close()
        if user_data:
            user = clsUsuario(user_data['usuario'], user_data['password_hash'], user_data['codigo_verificacion'], user_data['estado_verificado'], user_data['token'])
        return user
    except Exception as e:
        print(f"Error en obtener_user_por_id: {e}")
        return None

def generar_codigo_verificacion():
    # Generar un código de verificación aleatorio de longitud 6
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))

def registrar_usuario(username, hashed_password):
    try:
        conexion = obtener_conexion()
        codigo_verificacion = generar_codigo_verificacion()
        user_id = None
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO usuarios (usuario, password_hash, codigo_verificacion, estado_verificado) VALUES (%s, %s, %s, %s)", 
                           (username, hashed_password, codigo_verificacion, False))
            user_id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return user_id, codigo_verificacion
    except Exception as e:
        print(f"Error en registrar_usuario: {e}")
        return None, None

def guardar_codigo_verificacion(user_id, codeverify):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE usuarios SET codigo_verificacion = %s WHERE id = %s", (codeverify, user_id))
        conexion.commit()
        conexion.close()
    except Exception as e:
        print(f"Error en guardar_codigo_verificacion: {e}")

def verificar_codigo(username, codeverify):
    try:
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
    except Exception as e:
        print(f"Error en verificar_codigo: {e}")
        return False


def obtener_usuarios_verificados():
    try:
        conexion = obtener_conexion()
        users = []
        with conexion.cursor() as cursor:
            cursor.execute("SELECT usuario, password_hash FROM usuarios WHERE estado_verificado = %s", (True,))
            users_data = cursor.fetchall()
        conexion.close()
        for user_data in users_data:
            user = clsUsuario(user_data['usuario'], user_data['password_hash'], user_data['codigo_verificacion'], user_data['estado_verificado'], user_data['token'])
            users.append(user.dic_usuario)
        return users
    except Exception as e:
        print(f"Error en obtener_usuarios_verificados: {e}")
        return []

def actualizartoken_user(username, token):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE usuarios SET token = %s WHERE usuario = %s", (token, username))
        conexion.commit()
        conexion.close()
    except Exception as e:
        print(f"Error en actualizartoken_user: {e}")
