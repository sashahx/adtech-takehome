from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Order:
    id: Optional[int]
    name: str
    address: str
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()
