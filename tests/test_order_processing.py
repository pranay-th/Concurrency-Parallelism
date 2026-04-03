import pytest
from models.order_record import OrderRecord
from services.order_processing_service import (
    generate_order_records,
    process_record,
    process_orders_sequential,
    process_orders_parallel,
)
from utils.config import ORDER_RECORD_COUNT


def make_record(**kwargs):
    defaults = dict(
        order_id="ABC12345",
        supplier="SupplierA",
        quantity=10,
        unit_price=50.0,
        days_since_dispatch=5,
    )
    defaults.update(kwargs)
    return OrderRecord(**defaults)


def test_generate_returns_correct_count():
    records = generate_order_records(100)
    assert len(records) == 100

def test_generate_default_count():
    records = generate_order_records()
    assert len(records) == ORDER_RECORD_COUNT

def test_generate_returns_order_record_instances():
    records = generate_order_records(10)
    assert all(isinstance(r, OrderRecord) for r in records)

def test_generate_valid_quantity_range():
    records = generate_order_records(200)
    assert all(1 <= r.quantity <= 100 for r in records)

def test_generate_valid_unit_price_range():
    records = generate_order_records(200)
    assert all(5.0 <= r.unit_price <= 500.0 for r in records)

def test_generate_valid_days_range():
    records = generate_order_records(200)
    assert all(0 <= r.days_since_dispatch <= 30 for r in records)

def test_generate_valid_suppliers():
    from services.order_processing_service import SUPPLIERS
    records = generate_order_records(200)
    assert all(r.supplier in SUPPLIERS for r in records)


def test_process_record_total_value():
    record = make_record(quantity=10, unit_price=50.0)
    result = process_record(record)
    assert result["total_value"] == 500.0

def test_process_record_status_normal():
    record = make_record(days_since_dispatch=14)
    result = process_record(record)
    assert result["status"] == "normal"

def test_process_record_status_urgent():
    record = make_record(days_since_dispatch=15)
    result = process_record(record)
    assert result["status"] == "urgent"

def test_process_record_preserves_fields():
    record = make_record()
    result = process_record(record)
    assert result["order_id"] == record.order_id
    assert result["supplier"] == record.supplier
    assert result["quantity"] == record.quantity
    assert result["unit_price"] == record.unit_price
    assert result["days_since_dispatch"] == record.days_since_dispatch

def test_process_record_total_value_rounded():
    record = make_record(quantity=3, unit_price=1.005)
    result = process_record(record)
    assert result["total_value"] == round(3 * 1.005, 2)


def test_sequential_returns_same_count():
    records = generate_order_records(50)
    results = process_orders_sequential(records)
    assert len(results) == 50

def test_parallel_returns_same_count():
    records = generate_order_records(50)
    results = process_orders_parallel(records)
    assert len(results) == 50

def test_sequential_and_parallel_same_results():
    records = generate_order_records(50)
    seq = process_orders_sequential(records)
    par = process_orders_parallel(records)
    seq_sorted = sorted(seq, key=lambda x: x["order_id"])
    par_sorted = sorted(par, key=lambda x: x["order_id"])
    assert seq_sorted == par_sorted
