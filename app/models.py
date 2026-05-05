from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Producto:
    id: int
    nombre: str
    descripcion: str
    precio: float
    duracion_horas: int

class Carrito:
    def __init__(self):
        self.items: List[dict] = []  # lista de {"producto": Producto, "cantidad": int}

    def agregar(self, producto: Producto, cantidad: int = 1):
        # Buscar si ya existe
        for item in self.items:
            if item["producto"].id == producto.id:
                item["cantidad"] += cantidad
                return
        self.items.append({"producto": producto, "cantidad": cantidad})

    def eliminar(self, producto_id: int):
        self.items = [item for item in self.items if item["producto"].id != producto_id]

    def total(self) -> float:
        return sum(item["producto"].precio * item["cantidad"] for item in self.items)

    def vaciar(self):
        self.items.clear()