from flask_restful import Resource
from flask import jsonify, request
from models.ingrediente import Ingredientes
from db import db
from flask_login import current_user



class IngredientesResource(Resource):
    def get(self, id=None):
        try:
            nombre = request.args.get('nombre')
            essano = request.args.get('essano')
            
            if nombre:

                return self.obtener_ingredientes_por_nombre(nombre)
            elif id:
                if essano:
                    return self.obtener_sano_ingrediente_por_id(id)
                else:
                    return self.obtener_ingrediente_por_id(id)
            else:
                return self.obtener_todos_ingredientes()
        except Exception as e:
            return {'error': str(e)}, 500
    
    def obtener_todos_ingredientes(self):
        if not current_user.is_authenticated or current_user.is_cliente():
            return {'error': 'No autorizado'}, 401
        ingredientes = Ingredientes.query.all()
        ingredientes_list = [self.convertir_ingrediente_a_dict(i) for i in ingredientes]
        return jsonify({'ingredientes': ingredientes_list})

    def obtener_ingrediente_por_id(self, id):
        if not current_user.is_authenticated or current_user.is_cliente():
            return {'error': 'No autorizado'}, 401
        ingrediente = Ingredientes.query.get(id)
        if ingrediente:
            return jsonify(self.convertir_ingrediente_a_dict(ingrediente))
        else:
            return {'error': 'Ingrediente no encontrado'}, 404
    
    def obtener_ingredientes_por_nombre(self, nombre):
        if not current_user.is_authenticated or current_user.is_cliente():
            return {'error': 'No autorizado'}, 401
        ingredientes = Ingredientes.query.filter(Ingredientes.nombre.ilike(f'%{nombre}%')).all()
        if ingredientes:
            ingredientes_list = [self.convertir_ingrediente_a_dict(i) for i in ingredientes]
            return jsonify({'ingredientes': ingredientes_list})
        else:
            return {'error': 'No se encontraron ingredientes con el nombre proporcionado'}, 404
    
    def obtener_sano_ingrediente_por_id(self, id):
        if not current_user.is_authenticated or current_user.is_cliente():
            return {'error': 'No autorizado'}, 401
        ingrediente = Ingredientes.query.get(id)
        if ingrediente:
            es_sano = ingrediente.esSano()
            return jsonify({'id': ingrediente.id, 'nombre': ingrediente.nombre, 'es_sano': es_sano})
        else:
            return {'error': 'Ingrediente no encontrado'}, 404
    
    def convertir_ingrediente_a_dict(self, ingrediente):
        return {
            'id': ingrediente.id,
            'nombre': ingrediente.nombre,
            'precio': ingrediente.precio,
            'calorias': ingrediente.calorias,
            'inventario': ingrediente.inventario,
            'es_vegetariano': ingrediente.es_vegetariano,
            'tipo': ingrediente.tipo,
            'sabor': ingrediente.sabor
        }

class AbastecerIngredienteResource(Resource):
    def put(self, id):
        #if not current_user.is_authenticated or current_user.is_cliente():
        #    return {'error': 'No autorizado'}, 401
        try:
            ingrediente = Ingredientes.query.get(id)
            if ingrediente:
                ingrediente.abastecer()
                db.session.commit()
                return jsonify({'message': 'Ingrediente reabastecido exitosamente', 'id': id})
            else:
                return {'error': 'Ingrediente no encontrado'}, 404
        except Exception as e:
            return {'error': str(e)}, 500

class RenovarInventarioIngredienteResource(Resource):
    def put(self, id):
        #if not current_user.is_authenticated or current_user.is_cliente():
        #    return {'error': 'No autorizado'}, 401
        try:
            ingrediente = Ingredientes.query.get(id)
            if ingrediente:
                cantidad_nueva = ingrediente.renovar_inventario()
                db.session.commit()
                return jsonify({'message': 'Inventario renovado exitosamente', 'id': id, 'nuevo_inventario': cantidad_nueva})
            else:
                return {'error': 'Ingrediente no encontrado'}, 404
        except Exception as e:
            return {'error': str(e)}, 500
