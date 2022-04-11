from flask_restful import Resource, reqparse, inputs
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, decode_token
import json


def is_admin():
    tipo_usuario = get_jwt_identity()['tipo']
    if "admin" in tipo_usuario:
        return True
    return False


class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The fild 'nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="The fild 'estrelas' cannot be left blank")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')


    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404

    @jwt_required() #criar novos hoteis
    def post(self, hotel_id):
        if is_admin():
            if HotelModel.find_hotel(hotel_id):
                return {"message": "Hotel id '{}' already exists".format(hotel_id)}, 400
            dados = Hotel.argumentos.parse_args()
            hotel = HotelModel(hotel_id,**dados)
            try:
                hotel.save_hotel()
            except:
                return {'message': 'An internal error ocurred trying to save hotel.'}, 500
            return hotel.json()
        return {'message': 'Only administrators can create new hotels.'}, 401

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
                return {'message': 'An internal error ocurred trying to save hotel.'}, 500
            return hotel.json(), 201
        return {'message': 'Only administrators can edit hotels.'}, 401

    @jwt_required() #deletar hoteis
    def delete(self, hotel_id):
        if is_admin():
            hotel = HotelModel.find_hotel(hotel_id)
            if hotel:
                try:
                    hotel.delete_hotel()
                except:
                    return {'message': 'An error ocurred trying to delet hotel.'}, 500
                return {'message': 'Hotel deleted'}
            return {'message': 'Hotel not found'}, 404
        return {'message': 'Only administrators can create new hotels.'}, 401


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
                return {'message': 'An error ocurred trying to reserv hotel.'}, 500
            return {'message': 'Hotel reservado com sucesso'}
        return {'message': 'Hotel not found'}, 404




