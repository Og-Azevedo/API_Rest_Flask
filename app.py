from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel, HotelReserva
from resources.usuario import Users, User, UserRegister, UserLogin, UserLogout
from resources.admin import Admins, Admin, AdminRegister, AdminLogin, AdminLogout
from flask_jwt_extended import JWTManager, get_current_user
from blacklist import BLACKLIST
from sql_alchemy import banco




app = Flask(__name__)
banco.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "String_segredo"
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def cria_banco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message':'You have been logged out.'}), 401


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(HotelReserva, '/hoteis/reserva/<string:hotel_id>')
api.add_resource(Users, '/usuarios')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Admins, '/admins')
api.add_resource(Admin, '/admins/<int:admin_id>')
api.add_resource(AdminRegister, '/admins/cadastro')
api.add_resource(AdminLogin, '/admins/login')
api.add_resource(AdminLogout, '/admins/logout')


# if __name__ == '__main__':
#     from sql_alchemy import banco
#     banco.init_app(app)
#     app.run(host="0.0.0.0", port=5000)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)