"""Estructuras de datos lineales en memoria (Pila, Cola y Lista) para afiliados."""

from abc import ABC, abstractmethod
from collections import deque
from typing import Deque, Iterator, List as PyList, Optional, Set

from src.config.constants import STRUCTURE_LIST, STRUCTURE_QUEUE, STRUCTURE_STACK
from src.domain.affiliate import Affiliate


class BaseAffiliateStructure(ABC):
    """Clase base para las estructuras lineales con verificación de ID en O(1)."""

    def __init__(self) -> None:
        self._registered_ids: Set[str] = set()

    @abstractmethod
    def __iter__(self) -> Iterator[Affiliate]:
        """Itera sobre los afiliados almacenados sin clonar la estructura."""

    @abstractmethod
    def __len__(self) -> int:
        """Retorna la cantidad de afiliados en la estructura."""

    def contains_id(self, id_number: str) -> bool:
        """Verifica en O(1) si existe un afiliado con el ID indicado."""
        return id_number.strip() in self._registered_ids

    def get_all(self) -> PyList[Affiliate]:
        """Retorna una lista con los elementos actuales de la estructura."""
        return list(self)

    def is_empty(self) -> bool:
        """Indica si la estructura se encuentra vacía."""
        return len(self) == 0

    def size(self) -> int:
        """Retorna el total de registros en la estructura."""
        return len(self)


class Stack(BaseAffiliateStructure):
    """Pila LIFO (Last-In, First-Out) implementada con collections.deque."""

    def __init__(self) -> None:
        super().__init__()
        self._items: Deque[Affiliate] = deque()

    def __iter__(self) -> Iterator[Affiliate]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def push(self, affiliate: Affiliate) -> None:
        """Apila un afiliado en el tope de la pila."""
        if self.contains_id(affiliate.id_number):
            raise ValueError(
                f"Ya existe un afiliado con el número de identificación {affiliate.id_number} en la Pila."
            )
        self._items.appendleft(affiliate)
        self._registered_ids.add(affiliate.id_number)

    def pop(self) -> Affiliate:
        """Desapila y retorna el último afiliado ingresado."""
        if self.is_empty():
            raise IndexError("La Pila está vacía. No hay registros para desapilar.")
        removed = self._items.popleft()
        self._registered_ids.discard(removed.id_number)
        return removed

    def peek(self) -> Optional[Affiliate]:
        """Obtiene el afiliado en el tope sin eliminarlo."""
        return self._items[0] if self._items else None


class Queue(BaseAffiliateStructure):
    """Cola FIFO (First-In, First-Out) implementada con collections.deque."""

    def __init__(self) -> None:
        super().__init__()
        self._items: Deque[Affiliate] = deque()

    def __iter__(self) -> Iterator[Affiliate]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def enqueue(self, affiliate: Affiliate) -> None:
        """Encola un afiliado al final de la cola."""
        if self.contains_id(affiliate.id_number):
            raise ValueError(
                f"Ya existe un afiliado con el número de identificación {affiliate.id_number} en la Cola."
            )
        self._items.append(affiliate)
        self._registered_ids.add(affiliate.id_number)

    def dequeue(self) -> Affiliate:
        """Desencola y retorna el primer afiliado ingresado."""
        if self.is_empty():
            raise IndexError("La Cola está vacía. No hay registros para desencolar.")
        removed = self._items.popleft()
        self._registered_ids.discard(removed.id_number)
        return removed

    def peek_front(self) -> Optional[Affiliate]:
        """Obtiene el primer afiliado de la cola sin eliminarlo."""
        return self._items[0] if self._items else None


class List(BaseAffiliateStructure):
    """Lista secuencial implementada con list nativo de Python."""

    def __init__(self) -> None:
        super().__init__()
        self._items: PyList[Affiliate] = []

    def __iter__(self) -> Iterator[Affiliate]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def append_affiliate(self, affiliate: Affiliate) -> None:
        """Agrega un afiliado al final de la lista."""
        if self.contains_id(affiliate.id_number):
            raise ValueError(
                f"Ya existe un afiliado con el número de identificación {affiliate.id_number} en la Lista."
            )
        self._items.append(affiliate)
        self._registered_ids.add(affiliate.id_number)

    def find_by_id(self, id_number: str) -> Optional[Affiliate]:
        """Busca un afiliado por número de identificación en la lista."""
        normalized_id = id_number.strip()
        if normalized_id not in self._registered_ids:
            return None
        for item in self._items:
            if item.id_number == normalized_id:
                return item
        return None

    def remove_by_id(self, id_number: str) -> Affiliate:
        """Busca y elimina el afiliado cuyo número de identificación coincida."""
        if self.is_empty():
            raise IndexError("La Lista está vacía. No hay registros para eliminar.")
        normalized_id = id_number.strip()
        if normalized_id not in self._registered_ids:
            raise LookupError(
                f"No se encontró ningún afiliado con el número de identificación '{normalized_id}' en la Lista."
            )
        for index, item in enumerate(self._items):
            if item.id_number == normalized_id:
                removed = self._items.pop(index)
                self._registered_ids.discard(normalized_id)
                return removed
        raise LookupError(
            f"No se encontró ningún afiliado con el número de identificación '{normalized_id}' en la Lista."
        )


AffiliateStack = Stack
AffiliateQueue = Queue
AffiliateList = List


class AffiliateRepository:
    """Repositorio en memoria que gestiona las tres estructuras lineales."""

    def __init__(self) -> None:
        self.stack: Stack = Stack()
        self.queue: Queue = Queue()
        self.affiliate_list: List = List()

    def get_structure(self, structure_type: str) -> BaseAffiliateStructure:
        """Retorna la instancia de la estructura seleccionada."""
        if structure_type == STRUCTURE_STACK:
            return self.stack
        if structure_type == STRUCTURE_QUEUE:
            return self.queue
        if structure_type == STRUCTURE_LIST:
            return self.affiliate_list
        raise ValueError(f"Estructura de datos no reconocida: '{structure_type}'.")

    def add_affiliate(self, structure_type: str, affiliate: Affiliate) -> None:
        """Inserta un afiliado según el comportamiento de la estructura activa."""
        if structure_type == STRUCTURE_STACK:
            self.stack.push(affiliate)
            return
        if structure_type == STRUCTURE_QUEUE:
            self.queue.enqueue(affiliate)
            return
        if structure_type == STRUCTURE_LIST:
            self.affiliate_list.append_affiliate(affiliate)
            return
        raise ValueError(f"Estructura de datos no reconocida: '{structure_type}'.")

    def get_affiliates(self, structure_type: str) -> PyList[Affiliate]:
        """Retorna los registros actuales de la estructura indicada."""
        return self.get_structure(structure_type).get_all()

    def is_structure_empty(self, structure_type: str) -> bool:
        """Verifica si la estructura indicada no tiene registros."""
        return self.get_structure(structure_type).is_empty()

    def peek_target_for_deletion(
        self,
        structure_type: str,
        target_id: Optional[str] = None,
    ) -> Optional[Affiliate]:
        """Obtiene el afiliado candidato a eliminarse antes de confirmar."""
        if structure_type == STRUCTURE_STACK:
            return self.stack.peek()
        if structure_type == STRUCTURE_QUEUE:
            return self.queue.peek_front()
        if structure_type == STRUCTURE_LIST:
            if not target_id:
                return None
            return self.affiliate_list.find_by_id(target_id)
        raise ValueError(f"Estructura de datos no reconocida: '{structure_type}'.")

    def remove_affiliate(
        self,
        structure_type: str,
        target_id: Optional[str] = None,
    ) -> Affiliate:
        """Elimina y retorna el afiliado según la disciplina de la estructura activa."""
        if structure_type == STRUCTURE_STACK:
            return self.stack.pop()
        if structure_type == STRUCTURE_QUEUE:
            return self.queue.dequeue()
        if structure_type == STRUCTURE_LIST:
            if not target_id:
                raise ValueError(
                    "Debe especificar el Número de Identificación para eliminar de la Lista."
                )
            return self.affiliate_list.remove_by_id(target_id)
        raise ValueError(f"Estructura de datos no reconocida: '{structure_type}'.")
