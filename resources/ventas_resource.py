from flask_restful import Resource
from flask import jsonify, request
from models.heladeria import Heladeria 
from flask_login import current_user

class VentaResource(Resource):
    def __init__(self):
        self.heladeria = Heladeria() 

    def post(self, id):
        #if not current_user.is_authenticated:
        #    return {'error': 'No autorizado'}, 401
        try:
            mensaje = self.heladeria.vender(id)
            return jsonify({'mensaje': mensaje})
        except ValueError as ve:
            return {'error': str(ve)}, 400
        except Exception as e:
            return {'error': str(e)}, 500
