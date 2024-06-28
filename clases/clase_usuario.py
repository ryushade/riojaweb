class clsUsuario:
    def __init__(self, usuario, password_hash, codigo_verificacion, estado_verificado, token):
        self.usuario = usuario
        self.password_hash = password_hash
        self.codigo_verificacion = codigo_verificacion
        self.estado_verificado = estado_verificado
        self.token = token

        self.dic_usuario = {
            "usuario": usuario,
            "password_hash": password_hash,
            "codigo_verificacion": codigo_verificacion,
            "estado_verificado": estado_verificado,
            "token": token
        }
