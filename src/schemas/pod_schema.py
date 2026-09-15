"""Pydantic schemas for POD document data."""

from typing import Optional
from pydantic import BaseModel, Field


class PODExtractionResult(BaseModel):
    """Schema for extracted POD fields."""

    document_type: str = Field(..., description="Type of document, e.g. Delivery Note, Receipt")
    tracking_number: Optional[str] = Field(None, description="Tracking or consignment ID")
    receiver_name: Optional[str] = Field(None, description="Name of the receiver")
    delivery_date: Optional[str] = Field(None, description="Delivery date")
    signature_present: bool = Field(False, description="Whether signature is present")
    stamp_present: bool = Field(False, description="Whether stamp is present")
    status: str = Field(..., description="Valid POD, Invalid POD, or Incomplete")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    remarks: Optional[str] = Field(None, description="Additional notes or remarks")
