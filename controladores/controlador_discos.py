from bd import obtener_conexion


def insertar_disco(codigo, nombre, artista, precio, genero):
    idgenerado = 0
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO discos(codigo, nombre, artista, precio, genero) VALUES (%s, %s, %s, %s, %s)",
                       (codigo, nombre, artista, precio, genero))
        cursor.execute('SELECT LAST_INSERT_ID()')
        cursor.lastrowid = cursor.fetchone()[0]
        idgenerado = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return idgenerado


def obtener_discos():
    conexion = obtener_conexion()
    discos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, codigo, nombre, artista, precio, genero FROM discos")
        discos = cursor.fetchall()
    conexion.close()
    return discos


def eliminar_disco(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM discos WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_disco_por_id(id):
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, codigo, nombre, artista, precio, genero FROM discos WHERE id = %s", (id,))
        juego = cursor.fetchone()
    conexion.close()
    return juego


def actualizar_disco(codigo, nombre, artista, precio, genero, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE discos SET codigo = %s, nombre = %s, artista = %s, precio = %s, genero = %s WHERE id = %s",
                       (codigo, nombre, artista, precio, genero, id))
    conexion.commit()
    conexion.close()
