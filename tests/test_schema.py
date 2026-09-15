"""Tests for schema validation."""

import pytest
from src.schemas.pod_schema import PODExtractionResult


def test_schema_valid():
    data = {
        "document_type": "Delivery Note",
        "tracking_number": "TRK-123456",
        "receiver_name": "John Doe",
        "delivery_date": "2026-09-15",
        "signature_present": True,
        "stamp_present": True,
        "status": "Valid POD",
        "confidence": 0.95,
        "remarks": "Signature and stamp confirmed",
    }
    result = PODExtractionResult(**data)
    assert result.signature_present is True
    assert result.status == "Valid POD"
