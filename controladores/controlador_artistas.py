from bd import obtener_conexion


def insertar_artista(nombre, nacionalidad):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO artistas(nombre, nacionalidad) VALUES (%s, %s)",
                       (nombre, nacionalidad))
    conexion.commit()
    conexion.close()


def obtener_artistas():
    conexion = obtener_conexion()
    artistas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, nacionalidad FROM artistas")
        artistas = cursor.fetchall()
    conexion.close()
    return artistas


def eliminar_artista(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM artistas WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_artista_por_id(id):
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, nacionalidad FROM artistas WHERE id = %s", (id,))
        juego = cursor.fetchone()
    conexion.close()
    return juego


def actualizar_artista(nombre, nacionalidad, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE artistas SET nombre = %s, nacionalidad = %s WHERE id = %s",
                       (nombre, nacionalidad, id))
    conexion.commit()
    conexion.close()
