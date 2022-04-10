import sqlalchemy

from sql_alchemy import banco
from sqlalchemy import Boolean

class AdminModel(banco.Model):
    __tablename__= 'admins'

    admin_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))


    def __init__(self, login, senha):
        self.login = login
        self.senha = senha

    def json(self):
        return {
            'admin_id':self.admin_id,
            'login':self.login,
        }
    @classmethod
    def find_admin(cls, admin_id):
        admin = cls.query.filter_by(admin_id=admin_id).first()
        if admin:
            return admin
        return None

    @classmethod
    def find_by_login(cls, login):
        admin = cls.query.filter_by(login=login).first()
        if admin:
            return admin
        return None

    def save_admin(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_admin(self):
        banco.session.delete(self)
        banco.session.commit()

