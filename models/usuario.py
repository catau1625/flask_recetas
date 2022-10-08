from config.mysqlconnection import connectToMySQL
from flask import flash
from models import receta
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recetas = []
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO usuarios (first_name,last_name,email,password,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
        return connectToMySQL('esquema_recetas').query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM usuarios WHERE email = %(email)s;"
        return connectToMySQL('esquema_recetas').query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query = "UPDATE usuarios SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL('esquema_recetas').query_db(query,data)
    
    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM usuarios WHERE email=%(email)s;"
        results = connectToMySQL('esquema_recetas').query_db(query,data)
        user = []
        for datos in results:
            if datos == None:
                return False
            user_data = {
                "id": datos['id'],
                "first_name": datos['first_name'],
                "last_name": datos['last_name'],
                "email": datos['email'],
                "password": datos['password'],
                "created_at": datos['created_at'],
                "updated_at": datos['updated_at']
            }
            user.append(Usuario(user_data))
        return user
    
    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM usuarios WHERE id=%(id)s;"
        results = connectToMySQL('esquema_recetas').query_db(query,data)
        user = []
        for datos in results:
            if datos == None:
                return False
            user_data = {
                "id": datos['id'],
                "first_name": datos['first_name'],
                "last_name": datos['last_name'],
                "email": datos['email'],
                "password": datos['password'],
                "created_at": datos['created_at'],
                "updated_at": datos['updated_at']
            }
            user.append(Usuario(user_data))
        return user
    
    @staticmethod
    def validacion(info):
        is_valid = True
        for data in info:
            if not data:
                flash('Todos los campos son obligatorios','error')
                return is_valid
        if len(info['first_name']) < 2:
            flash('El nombre debe tener al menos 2 letras','error')
            is_valid = False
        if len(info['last_name']) < 2:
            flash('El apellido debe contener al menos 2 letras','error')
            is_valid = False
        if not EMAIL_REGEX.match(info['email']):
            flash('Correo inválido','error')
            is_valid = False
        if len(info['password']) < 8:
            flash('La contraseña debe contener al menos 8 caracteres','error')
        return is_valid
    
    @classmethod
    def recetas_por_usuario(cls,data):
        query = "SELECT * FROM recetas JOIN likes ON recetas.id = likes.receta_id JOIN usuarios ON likes.usuario_id = usuarios.id WHERE usuarios.id = %(id)s;"
        results = connectToMySQL('esquema_recetas').query_db(query,data)
        recetas = []
        for info in results:
            receta_data = {
                "id": info['id'],
                "nombre": info['nombre'],
                "descripcion": info['descripcion'],
                "instruccion": info['instruccion'],
                "less_30min": info['less_30min'],
                "created_at": info['created_at'],
                "updated_at": info['updated_at']
            }
            recetas.append(receta.Receta(receta_data))
            print(recetas)
        return recetas