from flask_restful import Resource, reqparse
from models.admin import AdminModel
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

class Admins(Resource):

    @jwt_required()
    def get(self):
        if is_admin():
            return {'admins': [admin.json() for admin in AdminModel.query.all()]}
        return {'message': 'Você não pode acessar a lista de administradores'}


class Admin(Resource):

    @jwt_required()
    def get(self, admin_id): #acessar lista de admins
        if is_admin():
            admin = AdminModel.find_admin(admin_id)
            if admin:
                return admin.json()
            return {'message': 'Admin não encontrado.'}, 404
        return {'message': 'Você não pode acessar a lista de administradores.'}, 401

    @jwt_required()
    def delete(self, admin_id): #delete admin
        if is_admin():
            admin = AdminModel.find_admin(admin_id)
            if admin:
                try:
                    admin.delete_admin()
                except:
                    return {'message': 'Ocorreu um erro ao tentar deletar.'}, 500
                return {'message': 'Usuário deletado'}
            return {'message': 'Usuário não encontrado'}, 404
        return {'message': 'Você não pode deletar administradores'}, 401


class AdminRegister(Resource):

    @jwt_required()
    def post(self):
        if is_admin():
            dados = argumentos.parse_args()

            if AdminModel.find_by_login(dados['login']):
                return {'message': "Esse login '{}' já existe, tente outro!".format(dados['login'])}

            admin = AdminModel(**dados)
            admin.save_admin()
            return {'message': "Admin criado com sucesso!"}, 201
        return {'message': "Somente administradores podem cadastrar novos admins!"}, 201

class AdminLogin(Resource):

    @classmethod
    def post(cls):
        dados = argumentos.parse_args()
        admin = AdminModel.find_by_login(dados['login'])

        if admin and safe_str_cmp(admin.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=admin.json())
            return {'access_token': token_de_acesso}, 200
        return {'message': "Login e senha incorretos."}, 401

class AdminLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logout feito com sucesso!'}, 200