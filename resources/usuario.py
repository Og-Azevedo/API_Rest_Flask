from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST


def is_admin():
    tipo_usuario = get_jwt_identity()['tipo']
    if "admin" in tipo_usuario:
        return True
    return False

argumentos = reqparse.RequestParser()
argumentos.add_argument('login', type=str, required=True, help="The fild 'login' cannot be left blank")
argumentos.add_argument('senha', type=str, required=True, help="The fild 'senha' cannot be left blank")

class Users(Resource):

    @jwt_required()
    def get(self):
        if is_admin():
            return {'usuarios': [user.json() for user in UserModel.query.all()]}
        return {'message': 'Você não pode acessar a lista de usuários'}

class User(Resource):

    @jwt_required()
    def get(self, user_id):
        if is_admin():
            user = UserModel.find_user(user_id)
            if user:
                return user.json()
            return {'message': 'Usuario não encontrado.'}, 404
        return {'message': 'Você não pode acessar informações dos usuários.'}, 404

    @jwt_required()
    def put(self, user_id): #editar usuario
        if is_admin():
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
                return {'message': 'Um erro interno ocorreu ao tentar editar o usuario.'}, 500
            return usuario.json(), 201
        return {'message': 'Apenas administradores podem editar usuários.'}, 500

    @jwt_required()
    def delete(self, user_id): #deletar usuario
        if is_admin():
            user = UserModel.find_user(user_id)
            if user:
                try:
                    user.delete_user()
                except:
                    return {'message': 'Aconteceu um erro ao tentar deletar o usuario.'}, 500
                return {'message': 'Usuario deletado'}
            return {'message': 'Usuario não encontrado'}, 404
        return {'message': 'Você não tem acesso'}, 401

class UserRegister(Resource):

    def post(self): #criar usuario
        dados = argumentos.parse_args()
        if UserModel.find_by_login(dados['login']):
            return {'message': "O usuario '{}' já existe".format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()
        return {'message': "Usuario criado com sucesso!"}, 201

class UserLogin(Resource):

    @classmethod
    def post(cls): #fazer login

        dados = argumentos.parse_args()
        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity= user.json())

            return {'access_token': token_de_acesso}, 200
        return {'message': "Login e senha incorretos."}, 401

class UserLogout(Resource):

    @jwt_required()
    def post(self): #fazer logout
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged feito com sucesso!'}, 200