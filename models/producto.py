from abc import ABC, abstractmethod
from db import db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class Productos(db.Model, Base):
    __tablename__ = 'productos'

    id = db.Column(Integer, primary_key=True)
    tipo = db.Column(String(50), nullable=False)
    nombre = db.Column(String(100), nullable=False)
    precio_publico = db.Column(Integer, nullable=False)
    tipo_vaso = db.Column(String(50))
    volumen = db.Column(Integer)
    
    # Definición de las relaciones con los ingredientes
    ingrediente_1 = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), nullable=False)
    ingrediente_2 = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), nullable=False)
    ingrediente_3 = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), nullable=False)
    
    # Relaciones con la clase Ingrediente
    ingrediente1 = db.relationship("Ingredientes", foreign_keys=[ingrediente_1])
    ingrediente2 = db.relationship("Ingredientes", foreign_keys=[ingrediente_2])
    ingrediente3 = db.relationship("Ingredientes", foreign_keys=[ingrediente_3])

    def calcular_costo(self) -> str:
        precio = 0
        ingredientes = [self.ingrediente1, self.ingrediente2, self.ingrediente3]
    
        for ingrediente in ingredientes:
            if ingrediente:
                precio += ingrediente.precio
    
        return f"Costo del producto: ${precio}"

    def calcular_calorias(self) -> str:
        calorias_totales = 0
        ingredientes = [self.ingrediente1, self.ingrediente2, self.ingrediente3]
        for ingrediente in ingredientes:
            if ingrediente:
                calorias_totales += ingrediente.calorias
        
        total_calorias = round(calorias_totales * 0.95, 2)
        return f"Calorias totales: {total_calorias}"
    
    def calcular_rentabilidad(self)->str:
        precios_ingredientes = 0
        ingredientes = [self.ingrediente1, self.ingrediente2, self.ingrediente3]
        for ingrediente in ingredientes:
            precios_ingredientes += ingrediente.precio
        rentabilidad = self.precio_publico - precios_ingredientes
        return ("Rentabilidad: $" + str(rentabilidad))
    
    ## Getters y Setters:

    def get_nombre(self) -> str:
        return self.nombre

    def set_nombre(self, nombre: str) -> None:
        self.nombre = nombre

    def get_precio_publico(self) -> int:
        return self.precio_publico

    def set_precio_publico(self, precio_publico: int) -> None:
        self.precio_publico = precio_publico

    def get_tipo_vaso(self) -> int:
        return self.tipo_vaso

    def set_tipo_vaso(self, tipo_vaso: int) -> None:
        self.tipo_vaso = tipo_vaso
    
    def get_ingredientes(self)->list:
        return [
        self.ingrediente1.nombre if self.ingrediente1 else None,
        self.ingrediente2.nombre if self.ingrediente2 else None,
        self.ingrediente3.nombre if self.ingrediente3 else None,
        ]

    def set_ingredientes(self, ingredientes: list) -> None:
        self.ingredientes = ingredientes
    

    
    
