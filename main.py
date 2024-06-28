from flask import Flask, request, jsonify, make_response
from flask_jwt import JWT, jwt_required, current_identity
from hashlib import sha256
import random
import controladores.controlador_usuarios as controlador_usuarios

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

### API para Registrar Usuario ###
@app.route('/api_registrarusuario_p3', methods=['POST'])
def api_registrarusuario_p3():
    try:
        data = request.get_json()
        usuario = data['usuario']
        password = data['pass']
        hashed_password = sha256(password.encode()).hexdigest()
        user_id = controlador_usuarios.registrar_usuario(usuario, hashed_password)
        codeverify = random.randint(100000, 999999)
        controlador_usuarios.guardar_codigo_verificacion(user_id, codeverify)

        return jsonify({
            "code": 1,
            "data": {
                "usuario": usuario,
                "codeverify": codeverify
            },
            "message": "Usuario registrado correctamente"
        })
    except Exception as e:
        print(f"Error in api_registrarusuario_p3: {e}")
        return jsonify({
            "code": 0,
            "message": "Error al registrar usuario"
        }), 500

### API para Confirmar Usuario ###
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

### API para Listar Usuarios Verificados ###
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
