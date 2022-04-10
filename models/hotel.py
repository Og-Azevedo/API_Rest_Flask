from sql_alchemy import banco
from datetime import datetime

class HotelModel(banco.Model):
    __tablename__= 'hoteis'

    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))
    reserva = banco.Column(banco.Integer, default=0)
    checkin = banco.Column(banco.Date)
    hospede = banco.Column(banco.String, default="")


    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        # self.reserva = reserva
        # self.hospede = hospede

    def json(self):
        return {
            'hotel_id':self.hotel_id,
            'nome':self.nome,
            'estrelas':self.estrelas,
            'diaria':self.diaria,
            'cidade':self.cidade,
            'checkin':self.checkin.isoformat(),
            'reserva':self.reserva,
            'hospede':self.hospede
        }
    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    def reservar_quarto(self, num_diarias, hospede, checkin):
        self.reserva = num_diarias
        self.hospede = hospede
        self.checkin = checkin
        self.save_hotel()

    def update_hotel(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()

