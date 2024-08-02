from abc import ABC, abstractmethod
from db import db
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ingredientes(db.Model, Base):
    __tablename__ = 'ingredientes'

    id = db.Column(Integer, primary_key=True)
    precio = db.Column(Integer, nullable=False)
    calorias = db.Column(Integer, nullable=False)
    nombre = db.Column(String(255), nullable=False)
    inventario = db.Column(Integer, nullable=False)
    es_vegetariano = db.Column(Boolean, nullable=False)
    tipo = db.Column(String(20), nullable=False)
    sabor = db.Column(String(50))
    
    def esSano(self) -> bool:
        return self.calorias < 100 or self.es_vegetariano

    def abastecer(self):
        self.inventario += 5
    
    def renovar_inventario(self) -> int:
        self.inventario = 0
        return self.inventario
    
    def get_precio(self) -> int:
        return self.precio
    
    def set_precio(self, nuevo_precio: int) -> None:
        self.precio = nuevo_precio
    
    def get_calorias(self) -> int:
        return self.calorias
    
    def set_calorias(self, nuevas_calorias: int) -> None:
        self.calorias = nuevas_calorias
    
    def get_nombre(self) -> str:
        return self.nombre
    
    def set_nombre(self, nuevo_nombre: str) -> None:
        self.nombre = nuevo_nombre
    
    def get_inventario(self) -> int:
        return self.inventario
    
    def set_inventario(self, nuevo_inventario: int) -> None:
        self.inventario = nuevo_inventario

    def get_es_vegetariano(self) -> bool:
        return self._es_vegetariano
    
    def set_es_vegetariano(self, nuevo_valor: bool) -> None:
        self._es_vegetariano = nuevo_valor

    
    
