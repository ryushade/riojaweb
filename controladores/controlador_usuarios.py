from bd import obtener_conexion

def obtener_user_por_username(username):
    try:
        conexion = obtener_conexion()
        user = None
        with conexion.cursor() as cursor:
            cursor.execute("SELECT usuario, password_hash, codigo_verificacion, estado_verificado, token FROM usuarios WHERE usuario = %s", (username,))
            user = cursor.fetchone()
        conexion.close()
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
            user = cursor.fetchone()
        conexion.close()
        return user
    except Exception as e:
        print(f"Error en obtener_user_por_id: {e}")
        return None

def registrar_usuario(username, hashed_password):
    try:
        conexion = obtener_conexion()
        user_id = None
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO usuarios (usuario, password_hash, codigo_verificacion, estado_verificado) VALUES (%s, %s, %s, %s)", 
                           (username, hashed_password, 0, False))
            user_id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return user_id
    except Exception as e:
        print(f"Error en registrar_usuario: {e}")
        return None

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
            users = cursor.fetchall()
        conexion.close()
        return users
    except Exception as e:
        print(f"Error en obtener_usuarios_verificados: {e}")
        return []
