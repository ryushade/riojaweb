import pymysql

def obtener_conexion():
    return pymysql.connect(host='riojadawb.mysql.pythonanywhere-services.com',
                                user='riojadawb',
                                password='23bf1a0d2',
                                db='riojadawb$discos')