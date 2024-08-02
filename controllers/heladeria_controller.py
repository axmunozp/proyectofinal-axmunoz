from models.heladeria import Heladeria
from flask import render_template, make_response
from flask_restful import Resource



class Heladeria_Controller(Resource):
    def __init__(self):
        self.heladeria = Heladeria()  

    def encontrar_mejor_producto(self,heladeria: Heladeria) -> str:
        return heladeria.mejor_producto()

    def get(self, id_producto: int) -> str:
        try:
            exito = self.heladeria.vender(id_producto)
            return "¡Vendido!" if exito else "No se pudo vender el producto."
        except ValueError as e:
            return f"Oh no! Nos hemos quedado sin {str(e)}"

    def listar_productos(self,heladeria: Heladeria):
        return heladeria.listar_productos()
