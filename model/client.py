from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal


class Client(BaseModel):
    name: str
    contact: str
    lang: Optional[Literal["en", "ar"]] = "en"


class Item(BaseModel):
    sku: str
    qty: int
    unit_cost: float
    margin_pct: float


class QuoteRequest(BaseModel):
    client: Client
    currency: str
    items: List[Item]
    delivery_terms: str
    notes: str


class QuoteResponse(BaseModel):
    subject: str = Field(..., example="subject of the email")
    body: str = Field(..., example="body of the email")
    grand_total: float
    line_totals: List[float]
