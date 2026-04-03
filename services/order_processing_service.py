import random
import string
import multiprocessing
from models.order_record import OrderRecord
from utils.config import ORDER_RECORD_COUNT

SUPPLIERS = ["SupplierA", "SupplierB", "SupplierC", "SupplierD"]

def generate_order_records(count=ORDER_RECORD_COUNT):
    records = []
    for i in range(count):
        record = OrderRecord(
            order_id=''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
            supplier=random.choice(SUPPLIERS),
            quantity=random.randint(1, 100),
            unit_price=round(random.uniform(5.0, 500.0), 2),
            days_since_dispatch=random.randint(0, 30)
        )
        records.append(record)
    return records

def process_record(record: OrderRecord) -> dict:
    total_value = record.quantity * record.unit_price
    status = "urgent" if record.days_since_dispatch > 14 else "normal"
    return {
        "order_id": record.order_id,
        "supplier": record.supplier,
        "quantity": record.quantity,
        "unit_price": record.unit_price,
        "days_since_dispatch": record.days_since_dispatch,
        "total_value": round(total_value, 2),
        "status": status
    }

def process_orders_parallel(records):
    with multiprocessing.Pool() as pool:
        results = pool.map(process_record, records)
    return results

def process_orders_sequential(records):
    return [process_record(r) for r in records]
