from flask import Flask, request, jsonify, render_template, redirect, make_response
from flask_jwt import JWT, jwt_required, current_identity
from hashlib import sha256
import random
import controladores.controlador_usuarios as controlador_usuarios
import controladores.controlador_discos as controlador_discos

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

##### SEGURIDAD - INICIO #####
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return f"User(id='{self.id}')"

def authenticate(username, password):
    try:
        user = controlador_usuarios.obtener_user_por_username(username)
        if user and sha256(password.encode()).hexdigest() == user['password_hash'] and user['estado_verificado']:
            return User(user['usuario'], username, user['password_hash'])
    except Exception as e:
        print(f"Error in authenticate: {e}")
        return None

def identity(payload):
    try:
        user_id = payload['identity']
        userfrombd = controlador_usuarios.obtener_user_por_id(user_id)
        if userfrombd:
            return User(userfrombd['usuario'], userfrombd['usuario'], userfrombd['password_hash'])
    except Exception as e:
        print(f"Error in identity: {e}")
        return None

##### SEGURIDAD - FIN #####

jwt = JWT(app, authenticate, identity)

### Rutas para Usuarios ###
@app.route('/api_registrarusuario_p3', methods=['POST'])
def api_registrarusuario_p3():
    try:
        data = request.get_json()
        print(f"Datos recibidos: {data}")
        usuario = data['usuario']
        password = data['pass']
        hashed_password = sha256(password.encode()).hexdigest()
        print(f"Usuario: {usuario}, Hashed Password: {hashed_password}")

        user_id = controlador_usuarios.registrar_usuario(usuario, hashed_password)
        print(f"ID de usuario registrado: {user_id}")

        codeverify = random.randint(100000, 999999)
        controlador_usuarios.guardar_codigo_verificacion(user_id, codeverify)
        print(f"Código de verificación generado: {codeverify}")

        return jsonify({
            "code": 1,
            "data": {
                "usuario": usuario,
                "codeverify": codeverify
            },
            "message": "Usuario registrado correctamente"
        })
    except Exception as e:
        print(f"Error en api_registrarusuario_p3: {e}")
        return jsonify({
            "code": 0,
            "message": f"Error al registrar usuario: {str(e)}"
        }), 500

@app.route('/api_confirmarusuario_p3', methods=['POST'])
def api_confirmarusuario_p3():
    try:
        data = request.get_json()
        usuario = data['usuario']
        codeverify = int(data['codeverify'])

        if controlador_usuarios.verificar_codigo(usuario, codeverify):
            return jsonify({"code": 1, "data": {}, "message": "Usuario verificado correctamente"})
        else:
            return jsonify({"code": 0, "data": {}, "message": "Código de verificación incorrecto"})
    except Exception as e:
        print(f"Error in api_confirmarusuario_p3: {e}")
        return jsonify({
            "code": 0,
            "message": "Error al confirmar usuario"
        }), 500

@app.route('/api_listarusuarios_p3', methods=['GET'])
@jwt_required()
def api_listarusuarios_p3():
    try:
        usuarios = controlador_usuarios.obtener_usuarios_verificados()
        data = [{"email": u['usuario'], "password": u['password_hash']} for u in usuarios]

        return jsonify({
            "code": 1,
            "data": data,
            "message": "Listado correcto de usuarios"
        })
    except Exception as e:
        print(f"Error in api_listarusuarios_p3: {e}")
        return jsonify({
            "code": 0,
            "message": "Error al listar usuarios"
        }), 500

### Rutas para Discos ###
@app.route("/agregar_disco")
def formulario_agregar_disco():
    return render_template("agregar_disco.html")

@app.route("/guardar_disco", methods=["POST"])
def guardar_disco():
    try:
        codigo = request.form["codigo"]
        nombre = request.form["nombre"]
        artista = request.form["artista"]
        precio = request.form["precio"]
        genero = request.form["genero"]
        controlador_discos.insertar_disco(codigo, nombre, artista, precio, genero)
        return redirect("/discos")
    except Exception as e:
        print(f"Error in guardar_disco: {e}")
        return redirect("/discos")

@app.route("/")
@app.route("/discos")
def discos():
    try:
        username = request.cookies.get('username')
        token = request.cookies.get('token')
        user = controlador_usuarios.obtener_user_por_username(username)
        if user and user['token'] == token:
            discos = controlador_discos.obtener_discos()
            return render_template("discos.html", discos=discos)
        else:
            return redirect("/login")
    except Exception as e:
        print(f"Error in discos: {e}")
        return redirect("/login")

@app.route("/eliminar_disco", methods=["POST"])
def eliminar_disco():
    try:
        controlador_discos.eliminar_disco(request.form["id"])
        return redirect("/discos")
    except Exception as e:
        print(f"Error in eliminar_disco: {e}")
        return redirect("/discos")

@app.route("/formulario_editar_disco/<int:id>")
def editar_disco(id):
    try:
        disco = controlador_discos.obtener_disco_por_id(id)
        return render_template("editar_disco.html", disco=disco)
    except Exception as e:
        print(f"Error in editar_disco: {e}")
        return redirect("/discos")

@app.route("/actualizar_disco", methods=["POST"])
def actualizar_disco():
    try:
        id = request.form["id"]
        codigo = request.form["codigo"]
        nombre = request.form["nombre"]
        artista = request.form["artista"]
        precio = request.form["precio"]
        genero = request.form["genero"]
        controlador_discos.actualizar_disco(codigo, nombre, artista, precio, genero, id)
        return redirect("/discos")
    except Exception as e:
        print(f"Error in actualizar_disco: {e}")
        return redirect("/discos")

### Autenticación ###
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/procesar_login", methods=["POST"])
def procesar_login():
    try:
        username = request.form["username"]
        password = request.form["password"]
        epassword = sha256(password.encode("utf-8")).hexdigest()
        user = controlador_usuarios.obtener_user_por_username(username)
        if user and user['password_hash'] == epassword:
            aleatorio = str(random.randint(1, 1024))
            token = sha256(aleatorio.encode("utf-8")).hexdigest()
            resp = make_response(redirect("/discos"))
            resp.set_cookie('username', username)
            resp.set_cookie('token', token)
            controlador_usuarios.actualizartoken_user(username, token)
            return resp
        else:
            return redirect("/login")
    except Exception as e:
        print(f"Error in procesar_login: {e}")
        return redirect("/login")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/procesar_signup", methods=["POST"])
def procesar_signup():
    try:
        username = request.form["username"]
        password = request.form["password"]
        epassword = sha256(password.encode("utf-8")).hexdigest()
        controlador_usuarios.insertar_user(username, epassword)
        return redirect("/login")
    except Exception as e:
        print(f"Error in procesar_signup: {e}")
        return redirect("/signup")

@app.route("/logout")
def logout():
    resp = make_response(redirect("/login"))
    resp.set_cookie('token', "", expires=0)
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
