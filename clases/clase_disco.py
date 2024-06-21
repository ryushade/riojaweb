class clsDisco:
    id = 0
    codigo = ""
    nombre = ""
    artista = ""
    precio = 0.0
    genero = ""
    diccdisco = dict()

    def __init__(self, p_id, p_codigo, p_nombre, p_artista, p_precio, p_genero):
        self.id = p_id
        self.codigo = p_codigo
        self.nombre = p_nombre
        self.artista = p_artista
        self.precio = p_precio
        self.genero = p_genero
        self.diccdisco["id"] = p_id
        self.diccdisco["codigo"] = p_codigo
        self.diccdisco["nombre"] = p_nombre
        self.diccdisco["artista"] = p_artista
        self.diccdisco["precio"] = p_precio
        self.diccdisco["genero"] = p_genero