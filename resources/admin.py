from flask_restful import Resource, reqparse
from models.admin import AdminModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST


argumentos = reqparse.RequestParser()
argumentos.add_argument('login', type=str, required=True, help="The fild 'login' cannot be left blank")
argumentos.add_argument('senha', type=str, required=True, help="The fild 'senha' cannot be left blank")

class Admin(Resource):
    def get(self, admin_id):
        admin = AdminModel.find_admin(admin_id)
        if admin:
            return admin.json()
        return {'message': 'User not found.'}, 404

    @jwt_required()
    def delete(self, admin_id):
        admin = AdminModel.find_admin(admin_id)
        if admin:
            try:
                admin.delete_admin()
            except:
                return {'message': 'An error ocurred trying to delet user.'}, 500
            return {'message': 'User deleted'}
        return {'message': 'User not found'}, 404


class AdminRegister(Resource):
    #/cadastro
    def post(self):
        dados = argumentos.parse_args()

        if AdminModel.find_by_login(dados['login']):
            return {'message': "The login '{}' already exists".format(dados['login'])}

        admin = AdminModel(**dados)
        admin.save_admin()
        return {'message': "User created successfully!"}, 201

class AdminLogin(Resource):

    @classmethod
    def post(cls):
        dados = argumentos.parse_args()
        admin = AdminModel.find_by_login(dados['login'])

        if admin and safe_str_cmp(admin.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=admin.json())
            return {'access_token': token_de_acesso}, 200
        return {'message': "The username or password is incorrect."}, 401

class AdminLogout(Resource):

    @jwt_required()
    def post(self):
        # print(f"ADMIN ATUAL:{get_current_user()}")
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200