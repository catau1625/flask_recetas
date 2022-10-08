from config.mysqlconnection import connectToMySQL
from flask import flash
from models import usuario

class Receta:
    def __init__(self,data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.instruccion = data['instruccion']
        self.less_30min = data['less_30min']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.usuarios = []
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO recetas (nombre,descripcion,instruccion,less_30min,created_at,updated_at) VALUES (%(nombre)s,%(descripcion)s,%(instruccion)s,%(less_30min)s,NOW(),NOW());"
        return connectToMySQL('esquema_recetas').query_db(query,data)
    
    @classmethod
    def show_all(cls):
        query = "SELECT * FROM recetas;"
        results = connectToMySQL('esquema_recetas').query_db(query)
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
            recetas.append(Receta(receta_data))
        return recetas
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recetas WHERE id = %(id)s;"
        return connectToMySQL('esquema_recetas').query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query = "UPDATE recetas SET nombre=%(nombre)s,descripcion=%(descripcion)s,instruccion=%(instruccion)s,less_30min=%(less_30min)s,updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL('esquema_recetas').query_db(query,data)
    
    @classmethod
    def agregar_like(cls,data):
        query = "INSERT INTO likes (usuario_id,receta_id) VALUES (%(usuario_id)s,%(receta_id)s);"
        return connectToMySQL('esquema_recetas').query_db(query,data)
    
    @classmethod
    def usuarios_suscritos(cls,data):
        query = "SELECT usuarios.id,usuarios.first_name,usuarios.last_name,usuarios.email,usuarios.password,usuarios.created_at,usuarios.updated_at FROM usuarios JOIN likes ON usuarios.id = likes.usuario_id JOIN recetas ON likes.receta_id = recetas.id WHERE recetas.id=%(id)s GROUP BY usuarios.id;"
        results = connectToMySQL('esquema_recetas').query_db(query,data)
        usuarios = []
        for info in results:
            user_data = {
                "id": info['id'],
                "first_name": info['first_name'],
                "last_name": info['last_name'],
                "email": info['email'],
                "password": info['password'],
                "created_at": info['created_at'],
                "updated_at": info['updated_at']
            }
            usuarios.append(usuario.Usuario(user_data))
        return usuarios
    
    @staticmethod
    def validacion(info):
        is_valid = True
        if len(info['nombre']) < 3:
            flash('El nombre de la receta debe contener al menos 3 caracteres','error')
            is_valid = False
        if len(info['descripcion']) < 3:
            flash('La descripción debe contener al menos 3 caracteres','error')
            is_valid = False
        if len(info['instruccion']) < 3:
            flash('Las instrucciones deben contener al menos 3 caracteres','error')
            is_valid = False
        return is_valid
    
    @classmethod
    def show_receta_by_id(cls,data):
        query = "SELECT * FROM recetas WHERE id=%(id)s;"
        results = connectToMySQL('esquema_recetas').query_db(query,data)
        receta = []
        if not results:
            flash('La receta no existe, intente de nuevo','error')
            return None
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
            receta.append(Receta(receta_data))
        return receta