# app/dtos/pagination.py
from dataclasses import dataclass
from typing import List, Any

@dataclass
class PaginatedResult:
    items: List[Any]
    page: int
    limit: int
    total: int

    @property
    def total_pages(self):
        return (self.total + self.limit - 1) // self.limit
