"""Pydantic schemas for POD document data."""

from typing import Literal, Optional
from pydantic import BaseModel, Field


class PODExtractionResult(BaseModel):
    """Schema for extracted POD fields."""
    cn_number : str | None = Field(None , description="Extracted  CN/consignment number")

    has_signature : bool = Field(False , description="Whether signature is present")


    has_stamp : bool = Field(False , description="Whether stamp is present")

    has_handwriting : bool = Field(False , description = "whether some handwrting is present in the document")
    
    image_quality_passed : bool = Field(False , description = "whether image quality is passed")    

    remarks_text: Optional[str] = Field(
    None,
    description="Remarks present in the POD"
    )
    remark: Literal["SHORT", "DAMAGE"] | None = Field(None, description="Remarks present in the POD")
    delivery_date: Optional[str] = Field(
    None,
    description="Delivery date of the POD in YYYY-MM-DD format"
    )
    physical_paper_damage : bool = Field(False , description = "whether physical paper damage is present")  

    business_damage : bool = Field(False , description = "whether business damage is present")  

    shortage : bool = Field(False , description = "whether shortage is present")  
    
    
    