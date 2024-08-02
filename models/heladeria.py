from models.ingrediente import Ingredientes
from models.producto import Productos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import db


class Heladeria():
    def __init__(self):
        self.productos = []
        self.ventas_del_dia = 0

    def listar_productos(self):
        self.productos = Productos.query.all()
        return self.productos
    
    def mejor_producto(self):
        self.productos = Productos.query.all()
        lista_ordenada = sorted(self.productos, key=lambda prod: prod.precio_publico - prod.calcular_costo())
        return f"Producto más rentable: {lista_ordenada[-1].nombre}" if lista_ordenada else "No hay productos"

    def vender(self, id_producto):
        producto = Productos.query.filter_by(id=id_producto).first()

        if not producto:
            raise ValueError("No existe el producto con el ID proporcionado.")

        ingredientes_suficientes = True
        ingredientes_faltantes = []

        for i in range(1, 4): 
            ingrediente = getattr(producto, f'ingrediente{i}')
            if ingrediente and ingrediente.inventario < 1:
                ingredientes_suficientes = False
                ingredientes_faltantes.append(ingrediente.nombre)

        if not ingredientes_suficientes:
            raise ValueError(f"{', '.join(ingredientes_faltantes)}")

        # Actualizar inventarios 
        for i in range(1, 4):
            ingrediente = getattr(producto, f'ingrediente{i}')
            if ingrediente:
                ingrediente.inventario -= 1
                db.session.add(ingrediente)

        # Registrar la venta
        self.ventas_del_dia += producto.precio_publico
        db.session.commit()

        return "¡Vendido!"