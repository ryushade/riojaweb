import pymysql

def obtener_conexion():
    return pymysql.connect(host='dawb2024iiusat.mysql.pythonanywhere-services.com',
                                user='dawb2024iiusat',
                                password='abcDEF$123',
                                db='dawb2024iiusat$discos')