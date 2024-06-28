from flask import Flask, render_template, request, redirect, flash, jsonify, make_response
import controladores.controlador_discos as controlador_discos
import controladores.controlador_artistas as controlador_artistas
import controladores.controlador_users as controlador_users
import clases.clase_disco as clase_disco
import clases.clase_pedido as clase_pedido
from flask_jwt import JWT, jwt_required, current_identity
from hashlib import sha256
import random

##### SEGURIDAD - INICIO #####
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

#users = [
#    User(1, 'user1', 'abcxyz'),
#    User(2, 'user2', 'abcxyz'),
#]

#username_table = {u.username: u for u in users}
#userid_table = {u.id: u for u in users}

def authenticate(username, password):
    epassword = sha256(password.encode("utf-8")).hexdigest()
    userfrombd = controlador_users.obtener_user_confirmado(username, epassword)
    user = None
    if userfrombd is not None:
        user = User(userfrombd[0], userfrombd[1], userfrombd[2])
    return user


def identity(payload):
    user_id = payload['identity']
    userfrombd = controlador_users.obtener_user_por_id(user_id)
    user = None
    if userfrombd is not None:
        user = User(userfrombd[0], userfrombd[1], userfrombd[2])
    #return userid_table.get(user_id, None)
    return user

##### SEGURIDAD - FIN #####

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)

###### DISCOS ######

@app.route("/agregar_disco")
def formulario_agregar_disco():
    return render_template("agregar_disco.html")


@app.route("/guardar_disco", methods=["POST"])
def guardar_disco():
    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    artista = request.form["artista"]
    precio = request.form["precio"]
    genero = request.form["genero"]
    controlador_discos.insertar_disco(codigo, nombre, artista, precio, genero)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/discos")


@app.route("/")
@app.route("/discos")
def discos():
    username = request.cookies.get('username')
    token = request.cookies.get('token')
    user = controlador_users.obtener_user_por_username(username)
    if user is not None and user[3] == token:
        discos = controlador_discos.obtener_discos()
        return render_template("discos.html", discos=discos)
    else:
        return redirect("/login")

@app.route("/eliminar_disco", methods=["POST"])
def eliminar_disco():
    controlador_discos.eliminar_disco(request.form["id"])
    return redirect("/discos")


@app.route("/formulario_editar_disco/<int:id>")
def editar_disco(id):
    # Obtener el disco por ID
    disco = controlador_discos.obtener_disco_por_id(id)
    return render_template("editar_disco.html", disco=disco)


@app.route("/actualizar_disco", methods=["POST"])
def actualizar_disco():
    id = request.form["id"]
    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    artista = request.form["artista"]
    precio = request.form["precio"]
    genero = request.form["genero"]
    controlador_discos.actualizar_disco(codigo, nombre, artista, precio, genero, id)
    return redirect("/discos")

###### ARTISTAS ######
@app.route("/artistas")
def artistas():
    artistas = controlador_artistas.obtener_artistas()
    return render_template("artistas.html", artistas=artistas)

@app.route("/agregar_artista")
def formulario_agregar_artista():
    return render_template("agregar_artista.html")

@app.route("/guardar_artista", methods=["POST"])
def guardar_artista():
    nombre = request.form["nombre"]
    nacionalidad = request.form["nacionalidad"]
    controlador_artistas.insertar_artista(nombre, nacionalidad)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/artistas")

@app.route("/formulario_editar_artista/<int:id>")
def editar_artista(id):
    # Obtener el artista por ID
    artista = controlador_artistas.obtener_artista_por_id(id)
    return render_template("editar_artista.html", artista=artista)

@app.route("/actualizar_artista", methods=["POST"])
def actualizar_artista():
    id = request.form["id"]
    nombre = request.form["nombre"]
    nacionalidad = request.form["nacionalidad"]
    controlador_artistas.actualizar_artista(nombre, nacionalidad, id)
    return redirect("/artistas")

@app.route("/eliminar_artista", methods=["POST"])
def eliminar_artista():
    controlador_artistas.eliminar_artista(request.form["id"])
    return redirect("/artistas")

##### APIs #####
@app.route("/api_pruebajson")
def api_pruebajson():
    satc = ["Carrie", "Samantha", "Charlote", "Miranda"]
    pinkfloyd = {
                    "bajo" : "Roger Waters",
                    "guitarra" : "David Gilmour",
                    "teclados" : "Richard Wright",
                    "bateria" : "Nick Mason",
                    "soporte" : satc
                }
    return jsonify(pinkfloyd)

@app.route("/api_obtenerdiscos")
@jwt_required()
def api_obtenerdiscos():
    rpta = dict()
    try:
        listadiscos = list()
        discos = controlador_discos.obtener_discos()
        total = 0.0
        for disco in discos:
            total += float(disco[4])
            objDisco = clase_disco.clsDisco(disco[0], disco[1], disco[2],
                                            disco[3], disco[4], disco[5])
            listadiscos.append(objDisco.diccdisco.copy())
        objPedido = clase_pedido.clsPedido(1, "2024-05-11", total, listadiscos)

        rpta["code"] = 1
        rpta["message"] = "Listado correcto de discos"
        rpta["data"] = objPedido.diccpedido
        return jsonify(rpta)
    except:
        rpta["code"] = 0
        rpta["message"] = "Problemas en el servicio web"
        rpta["data"] = dict()
        return rpta

@app.route("/api_guardardisco", methods=["POST"])
def api_guardardisco():
    rpta = dict()
    try:
        codigo = request.json["codigo"]
        nombre = request.json["nombre"]
        artista = request.json["artista"]
        precio = request.json["precio"]
        genero = request.json["genero"]
        idgenerado = controlador_discos.insertar_disco(codigo, nombre, artista, precio, genero)
        rpta["code"] = 1
        rpta["message"] = "Disco registrado correctamente"
        rpta["data"] = {"idgenerado" : idgenerado}
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
        rpta["data"] = dict()
    return rpta

##### APIS mascotaS #####




@app.route("/api_registrarusuario_p3", methods=["POST"])
def api_registrarusuario_p3():
    rpta = dict()
    try:
        # Obtener los datos de la solicitud
        data = request.get_json()
        username = data["usuario"]
        password = data["pass"]

        # Encriptar la contraseña
        epassword = sha256(password.encode("utf-8")).hexdigest()

        # Insertar el usuario en la base de datos
        controlador_users.insertar_user(username, epassword)

        # Generar el código de verificación de 6 dígitos
        codeverify = random.randint(100000, 999999)

        # Actualizar el código de verificación en la base de datos
        controlador_users.actualizar_codeverify_user(username, codeverify)

        # Preparar la respuesta
        rpta["code"] = 1
        rpta["data"] = {
            "usuario": username,
            "codeverify": codeverify
        }
        rpta["message"] = "Usuario registrado correctamente"
    except Exception as e:
        rpta["code"] = 0
        rpta["data"] = dict()
        rpta["message"] = f"Ocurrió un problema: {str(e)}"

    return jsonify(rpta)

@app.route("/api_confirmarusuario_p3", methods=["POST"])
def api_confirmarusuario_p3():
    rpta = dict()
    try:
        # Obtener los datos de la solicitud
        data = request.get_json()
        username = data["usuario"]
        codeverify = data["codeverify"]

        # Verificar el código de verificación
        user = controlador_users.verificar_codeverify_user(username, codeverify)
        if user:
            # Confirmar el usuario en la base de datos
            controlador_users.confirmar_user(username)
            rpta["code"] = 1
            rpta["data"] = {}
            rpta["message"] = "Usuario verificado correctamente"
        else:
            rpta["code"] = 0
            rpta["data"] = {}
            rpta["message"] = "Código de verificación incorrecto"
    except Exception as e:
        rpta["code"] = 0
        rpta["data"] = dict()
        rpta["message"] = f"Ocurrió un problema: {str(e)}"

    return jsonify(rpta)

@app.route("/api_listarusuarios_p3", methods=["GET"])
@jwt_required()
def api_listarusuarios_p3():
    rpta = dict()
    try:
        # Obtener todos los usuarios
        usuarios = controlador_users.obtener_todos_los_usuarios()
        
        # Formatear la respuesta
        usuarios_list = [{"email": user[0], "password": user[1]} for user in usuarios]
        
        rpta["code"] = 1
        rpta["data"] = usuarios_list
        rpta["message"] = "Listado correcto de usuarios"
    except Exception as e:
        rpta["code"] = 0
        rpta["data"] = []
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
    
    return jsonify(rpta)


@app.route("/login")
def login():
    username = request.cookies.get('username')
    token = request.cookies.get('token')
    user = controlador_users.obtener_user_por_username(username)
    if user is not None and user[3] == token:
        discos = controlador_discos.obtener_discos()
        return render_template("discos.html", discos=discos)
    else:
        return render_template("login.html")

@app.route("/procesar_login", methods=["POST"])
def procesar_login():
    username = request.form["username"]
    password = request.form["password"]
    epassword = sha256(password.encode("utf-8")).hexdigest()
    user = controlador_users.obtener_user_por_username(username)
    if user[2] == epassword:
        aleatorio = str(random.randint(1, 1024))
        token = sha256(aleatorio.encode("utf-8")).hexdigest()
        resp = make_response(redirect("/discos"))
        resp.set_cookie('username', username)
        resp.set_cookie('token', token)
        controlador_users.actualizar_token_user(username, token)
        return resp
    else:
        return redirect("/login")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/procesar_signup", methods=["POST"])
def procesar_signup():
    username = request.form["username"]
    password = request.form["password"]
    epassword = sha256(password.encode("utf-8")).hexdigest()
    controlador_users.insertar_user(username, epassword)
    return redirect("/login")

@app.route("/logout")
def logout():
    resp = make_response(redirect("/login"))
    resp.set_cookie('token', "", expires=0)
    return resp

# Iniciar el servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
