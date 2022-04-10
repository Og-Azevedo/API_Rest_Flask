from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST


argumentos = reqparse.RequestParser()
argumentos.add_argument('login', type=str, required=True, help="The fild 'login' cannot be left blank")
argumentos.add_argument('senha', type=str, required=True, help="The fild 'senha' cannot be left blank")

class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    @jwt_required()
    def put(self, user_id):
        dados = argumentos.parse_args()
        usuario_encontrado = UserModel.find_user(user_id)
        if usuario_encontrado:
            usuario_encontrado.update_user(**dados)
            usuario_encontrado.save_user()
            return usuario_encontrado.json(), 200
        usuario = UserModel(user_id, **dados)
        try:
            usuario.save_user()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500
        return usuario.json(), 201

    @jwt_required()
    def delete(self, user_id):
        tipo_usuario = get_jwt_identity()['tipo']
        print(f"Tipo usuário:{tipo_usuario}")
        if "admin" in tipo_usuario:
            user = UserModel.find_user(user_id)
            if user:
                try:
                    user.delete_user()
                except:
                    return {'message': 'An error ocurred trying to delet user.'}, 500
                return {'message': 'User deleted'}
            return {'message': 'User not found'}, 404
        return {'message': 'Você não tem acesso'}, 401

class UserRegister(Resource):
    #/cadastro
    def post(self):
        dados = argumentos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message': "The login '{}' already exists".format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()
        return {'message': "User created successfully!"}, 201

class UserLogin(Resource):

    @classmethod
    def post(cls):

        dados = argumentos.parse_args()
        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            # token_de_acesso = create_access_token(identity=user.user_id)
            # token_de_acesso = create_access_token(identity= f"{user.user_id}_UserComum")
            token_de_acesso = create_access_token(identity= user.json())

            return {'access_token': token_de_acesso}, 200
        return {'message': "The username or password is incorrect."}, 401

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        print(f"Identificador: {get_jwt_identity()}")
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200