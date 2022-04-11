from flask_restful import Resource, reqparse, inputs
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, decode_token



def is_admin():
    tipo_usuario = get_jwt_identity()['tipo']
    if "admin" in tipo_usuario:
        return True
    return False


class Hoteis(Resource):

    @jwt_required()
    def get(self):
        try:
            return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}
        except:
            return {'message': 'Erro interno.'}, 500



class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="O campo 'nome' não pode ser deixado em branco")
    argumentos.add_argument('estrelas', type=float, required=True, help="O campo 'estrelas' não pode ser deixado em branco")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    @jwt_required()
    def get(self, hotel_id):
        if is_admin():
            hotel = HotelModel.find_hotel(hotel_id)
            if hotel:
                try:
                    return hotel.json()
                except:
                    return {'message': 'Erro interno.'}, 500
            return {'message': 'Hootel não encontrado.'}, 404
        return {'message': 'Você não pode acessar informações dos hoteis.'}, 401

    @jwt_required() #criar novos hoteis
    def post(self, hotel_id):
        if is_admin():
            if HotelModel.find_hotel(hotel_id):
                return {"message": "Hotel id '{}' já existe".format(hotel_id)}, 400
            dados = Hotel.argumentos.parse_args()
            hotel = HotelModel(hotel_id,**dados)
            try:
                hotel.save_hotel()
            except:
                return {'message': 'Um erro interno ocorreu ao tentar criar esse hotel.'}, 500
            return hotel.json()
        return {'message': 'Apenas adminitradores podem criar hotel.'}, 401

    @jwt_required() #alterar dados de hoteis
    def put(self, hotel_id):
        if is_admin():
            dados = Hotel.argumentos.parse_args()
            hotel_encontrado = HotelModel.find_hotel(hotel_id)
            if hotel_encontrado:
                hotel_encontrado.update_hotel(**dados)
                hotel_encontrado.save_hotel()
                return hotel_encontrado.json(),200
            hotel = HotelModel(hotel_id, **dados)
            try:
                hotel.save_hotel()
            except:
                return {'message': 'Um erro interno ocorreu ao tentar editar esse hotel.'}, 500
            return hotel.json(), 201
        return {'message': 'Apenas administradores podem editar hotels.'}, 401

    @jwt_required() #deletar hoteis
    def delete(self, hotel_id):
        if is_admin():
            hotel = HotelModel.find_hotel(hotel_id)
            if hotel:
                try:
                    hotel.delete_hotel()
                except:
                    return {'message': 'Um erro ocorreu ao tentar deletar esse hotel.'}, 500
                return {'message': 'Hotel deletado com sucesso.'}
            return {'message': 'Hotel não encontrado'}, 404
        return {'message': 'Apenas administradores podem criar hoteis.'}, 401


class HotelReserva(Resource):

    @jwt_required()
    def post(self, hotel_id):
        hospede = get_jwt_identity()['login']
        # print(f"Tipo: {get_jwt_identity()}")
        argumentos = reqparse.RequestParser()
        argumentos.add_argument('checkin', type=inputs.date , required=True, help="The fild 'reserva' cannot be left blank")
        argumentos.add_argument('checkout', type=inputs.date , required=True, help="The fild 'reserva' cannot be left blank")
        dados = argumentos.parse_args()

        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.reservar_quarto(hospede, dados['checkin'], dados['checkout'])
            except:
                return {'message': 'Ocorreu um erro ao tentar encontrar o hotel.'}, 500
            return {'message': 'Hotel reservado com sucesso'}
        return {'message': 'Hotel não encontrado'}, 404




