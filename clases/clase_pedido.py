class clsPedido:
    id = 0
    fechapedido = ""
    total = 0.0
    detalle = list()
    diccpedido = dict()

    def __init__(self, p_id, p_fechapedido, p_total, p_detalle):
        self.id = p_id
        self.fechapedido = p_fechapedido
        self.total = p_total
        self.detalle = p_detalle
        self.diccpedido["id"] = p_id
        self.diccpedido["fechapedido"] = p_fechapedido
        self.diccpedido["total"] = p_total
        self.diccpedido["detalle"] = p_detalle