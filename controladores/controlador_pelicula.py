from bd import obtener_conexion

def insertar_pelicula(nombre, director, productora, anioproduccion, aniolanzamiento, weboficial):
    conexion = obtener_conexion()
    idgenerado = None
    try:
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO pelicula(nombre, director, productora, anioproduccion, aniolanzamiento, weboficial) VALUES (%s, %s, %s, %s, %s, %s)",
                           (nombre, director, productora, anioproduccion, aniolanzamiento, weboficial))
            idgenerado = cursor.lastrowid
        conexion.commit()
    except Exception as e:
        print(f"Error during insertion: {e}")  # Agrega esta línea para la depuración
    finally:
        conexion.close()
    return idgenerado

def obtener_peliculas():
    conexion = obtener_conexion()
    peliculas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, director, productora, anioproduccion, aniolanzamiento, weboficial FROM pelicula")
        peliculas = cursor.fetchall()
    conexion.close()
    return peliculas