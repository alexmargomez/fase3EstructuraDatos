"""In-memory linear data structures: Stack (deque), Queue (deque), and List (list)."""

from abc import ABC, abstractmethod
from collections import deque
from typing import Deque, List as PyList, Optional

from models.affiliate import Affiliate


class BaseLinearStructure(ABC):
    """Abstract base contract for linear data structures (OCP / LSP)."""

    @abstractmethod
    def get_all(self) -> PyList[Affiliate]:
        """Returns all affiliates currently stored in the structure."""

    @abstractmethod
    def contains_id(self, id_number: str) -> bool:
        """Checks whether an affiliate with the given ID number already exists."""

    def is_empty(self) -> bool:
        """Returns True if the structure contains no elements."""
        return len(self.get_all()) == 0


class AffiliateStack(BaseLinearStructure):
    """LIFO Stack structure implemented with collections.deque."""

    def __init__(self) -> None:
        self.items: Deque[Affiliate] = deque()

    def contains_id(self, id_number: str) -> bool:
        target = id_number.strip()
        return any(item.id_number == target for item in self.items)

    def push(self, affiliate: Affiliate) -> None:
        """Pushes an affiliate onto the top of the stack (LIFO)."""
        if self.contains_id(affiliate.id_number):
            raise ValueError(
                f"Ya existe un afiliado con la identificación {affiliate.id_number} en la Pila."
            )
        self.items.appendleft(affiliate)

    def peek(self) -> Optional[Affiliate]:
        """Returns the affiliate at the top of the stack without removing it."""
        return self.items[0] if self.items else None

    def pop(self) -> Affiliate:
        """Pops and returns the last inserted affiliate from the top of the stack."""
        if not self.items:
            raise IndexError("La Pila está vacía. No hay registros para desapilar.")
        return self.items.popleft()

    def get_total_fees(self) -> float:
        """Calculates the sum of affiliation fees of all records in the stack."""
        return round(sum(item.affiliation_fee for item in self.items), 2)

    def get_all(self) -> PyList[Affiliate]:
        return list(self.items)


class AffiliateQueue(BaseLinearStructure):
    """FIFO Queue structure implemented with collections.deque."""

    def __init__(self) -> None:
        self.items: Deque[Affiliate] = deque()

    def contains_id(self, id_number: str) -> bool:
        target = id_number.strip()
        return any(item.id_number == target for item in self.items)

    def enqueue(self, affiliate: Affiliate) -> None:
        """Enqueues an affiliate at the rear of the queue (FIFO)."""
        if self.contains_id(affiliate.id_number):
            raise ValueError(
                f"Ya existe un afiliado con la identificación {affiliate.id_number} en la Cola."
            )
        self.items.append(affiliate)

    def peek(self) -> Optional[Affiliate]:
        """Returns the first affiliate at the front of the queue without removing it."""
        return self.items[0] if self.items else None

    def dequeue(self) -> Affiliate:
        """Dequeues and returns the first inserted affiliate from the front of the queue."""
        if not self.items:
            raise IndexError("La Cola está vacía. No hay registros para desencolar.")
        return self.items.popleft()

    def get_record_count(self) -> int:
        """Returns the total count of records currently in the queue."""
        return len(self.items)

    def get_all(self) -> PyList[Affiliate]:
        return list(self.items)


class AffiliateList(BaseLinearStructure):
    """Sequential List structure implemented with Python's built-in list."""

    def __init__(self) -> None:
        self.items: PyList[Affiliate] = []

    def contains_id(self, id_number: str) -> bool:
        target = id_number.strip()
        return any(item.id_number == target for item in self.items)

    def add(self, affiliate: Affiliate) -> None:
        """Appends an affiliate to the end of the sequential list."""
        if self.contains_id(affiliate.id_number):
            raise ValueError(
                f"Ya existe un afiliado con la identificación {affiliate.id_number} en la Lista."
            )
        self.items.append(affiliate)

    def find_by_id(self, id_number: str) -> Optional[Affiliate]:
        """Searches and returns an affiliate by ID number, or None if not found."""
        target = id_number.strip()
        for item in self.items:
            if item.id_number == target:
                return item
        return None

    def remove_by_id(self, id_number: str) -> Affiliate:
        """Finds and removes an affiliate matching the given ID number."""
        if not self.items:
            raise IndexError("La Lista está vacía. No hay registros para eliminar.")
        target = id_number.strip()
        for index, item in enumerate(self.items):
            if item.id_number == target:
                return self.items.pop(index)
        raise LookupError(
            f"No existe ningún afiliado con el Número de Identificación '{target}' en la Lista."
        )

    def get_average_income(self) -> float:
        """Calculates the average current income of all records in the list."""
        if not self.items:
            return 0.0
        total_income = sum(item.current_income for item in self.items)
        return round(total_income / len(self.items), 2)

    def get_all(self) -> PyList[Affiliate]:
        return list(self.items)
