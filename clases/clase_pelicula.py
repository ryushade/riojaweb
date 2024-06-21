class clsPelicula:
    def __init__(self, p_id, p_nombre, p_director, p_productora, p_anioproduccion, p_aniolanzamiento, p_weboficial):
        self.id = p_id
        self.nombre = p_nombre
        self.director = p_director
        self.productora = p_productora
        self.anioproduccion = p_anioproduccion
        self.aniolanzamiento = p_aniolanzamiento
        self.weboficial = p_weboficial

        self.dicpelicula = {
            "id": p_id,
            "nombre": p_nombre,
            "director": p_director,
            "productora": p_productora,
            "anioproduccion": p_anioproduccion,
            "aniolanzamiento": p_aniolanzamiento,
            "weboficial": p_weboficial
        }
