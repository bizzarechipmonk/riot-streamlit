from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class DealContext:
    opp_id: str
    account: str
    stage: str
    vertical: str
    product: str

    # Optional / nullable fields
    amount: Optional[float] = None
    competitor: Optional[str] = None
    owner: Optional[str] = None
    close_date: Optional[str] = None  # keep string for now
    region: Optional[str] = None