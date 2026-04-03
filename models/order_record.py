from dataclasses import dataclass

@dataclass
class OrderRecord:
    order_id:str
    supplier:str
    quantity:int
    unit_price:float
    days_since_dispatch:int
