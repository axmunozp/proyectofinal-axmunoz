from flask_restful import Resource
from flask import jsonify, request
from models.producto import Productos
from flask_login import current_user

class ProductosResource(Resource):
    def get(self, id=None):
        try:
            nombre = request.args.get('nombre')
            
            if nombre:
                return self.obtener_productos_por_nombre(nombre)
            elif id:
                if 'calorias' in request.args:
                    return self.obtener_calorias_producto_por_id(id)
                elif 'rentabilidad' in request.args:
                    return self.obtener_rentabilidad_producto_por_id(id)
                elif 'costo' in request.args:
                    return self.obtener_costo_producto_por_id(id)
                else:
                    return self.obtener_producto_por_id(id)
            else:
                return self.obtener_todos_productos()
        except Exception as e:
            return {'error': str(e)}, 500

    def obtener_todos_productos(self):
        productos = Productos.query.all()
        productos_list = [self.convertir_producto_a_dict(p) for p in productos]
        return jsonify({'productos': productos_list})

    def obtener_producto_por_id(self, id):
        producto = Productos.query.get(id)
        if producto:
            return jsonify(self.convertir_producto_a_dict(producto))
        else:
            return {'error': 'Producto no encontrado'}, 404

    def obtener_productos_por_nombre(self, nombre):
        if not current_user.is_authenticated or current_user.is_cliente():
            return {'error': 'No autorizado'}, 401
        productos = Productos.query.filter(Productos.nombre.ilike(f'%{nombre}%')).all()
        if productos:
            productos_list = [self.convertir_producto_a_dict(p) for p in productos]
            return jsonify({'productos': productos_list})
        else:
            return {'error': 'No se encontraron productos con el nombre proporcionado'}, 404

    def obtener_calorias_producto_por_id(self, id):
        if not current_user.is_authenticated:
            return {'error': 'No autorizado'}, 401
        producto = Productos.query.get(id)
        if producto:
            calorias = producto.calcular_calorias()
            return jsonify({'id': producto.id, 'nombre': producto.nombre, 'calorias': calorias})
        else:
            return {'error': 'Producto no encontrado'}, 404

    def obtener_rentabilidad_producto_por_id(self, id):
        if not current_user.is_authenticated or not current_user.is_admin():
            return {'error': 'No autorizado'}, 401
        producto = Productos.query.get(id)
        if producto:
            rentabilidad = producto.calcular_rentabilidad()
            return jsonify({'id': producto.id, 'nombre': producto.nombre, 'rentabilidad': rentabilidad})
        else:
            return {'error': 'Producto no encontrado'}, 404

    def obtener_costo_producto_por_id(self, id):
        if not current_user.is_authenticated or current_user.is_cliente():
            return {'error': 'No autorizado'}, 401
        producto = Productos.query.get(id)
        if producto:
            costo = producto.calcular_costo()
            return jsonify({'id': producto.id, 'nombre': producto.nombre, 'costo': costo})
        else:
            return {'error': 'Producto no encontrado'}, 404

    def convertir_producto_a_dict(self, producto):
        ingredientes = {
            'ingrediente1': producto.ingrediente1.nombre if producto.ingrediente1 else None,
            'ingrediente2': producto.ingrediente2.nombre if producto.ingrediente2 else None,
            'ingrediente3': producto.ingrediente3.nombre if producto.ingrediente3 else None,
        }
        return {
            'id': producto.id,
            'nombre': producto.nombre,
            'precio_publico': producto.precio_publico,
            'tipo': producto.tipo,
            'tipo_vaso': producto.tipo_vaso,
            'volumen': producto.volumen,
            'ingredientes': ingredientes
        }
