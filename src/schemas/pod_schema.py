"""Pydantic schemas for POD document data."""

from typing import Literal, Optional
from pydantic import BaseModel, Field


class PODExtractionResult(BaseModel):
    """Schema for extracted POD fields."""
    cn_number : str | None = Field(None , description="Extracted  CN/consignment number")

    has_signature : bool = Field(False , description="Whether signature is present")

    signature_presence_score: float = Field(
    0.0,
    ge=0.0,
    le=1.0,
    description="Confidence score (0.0 to 1.0) indicating presence of signature"
)

    has_stamp : bool = Field(False , description="Whether stamp is present")

    stamp_presence_score: float = Field(
    0.0,    
    ge=0.0,
    le=1.0,
    description="Confidence score (0.0 to 1.0) indicating presence of stamp"
)

    has_handwriting : bool = Field(False , description = "whether some handwrting is present in the document")
    
    handwriting_presence_score: float = Field(
    0.0,
    ge=0.0,
    le=1.0,
    description="Confidence score (0.0 to 1.0) indicating presence of handwriting"
    )


    image_quality_passed : bool = Field(False , description = "whether image quality is passed")    

    remarks_text: Optional[str] = Field(
    None,
    description="Remarks present in the POD"
    )
    remark: Literal["SHORT", "DAMAGE" , "DAMAGE_SHORT"] | None = Field(None, description="Remarks present in the POD")
    delivery_date: Optional[str] = Field(
    None,
    description="Delivery date of the POD in YYYY-MM-DD format"
    )
    physical_paper_damage : bool = Field(False , description = "whether physical paper damage is present")  

    physical_damage_score: float = Field(
    0.0,
    ge=0.0,
    le=1.0,
    description="Confidence score (0.0 to 1.0) indicating presence of physical damage"
    )

    business_damage : bool = Field(False , description = "whether business damage is present")  

    business_damage_score: float = Field(
    0.0,
    ge=0.0,
    le=1.0,
    description="Confidence score (0.0 to 1.0) indicating presence of business damage"
    )

    business_shortage : bool = Field(False , description = "whether shortage is present")  

    business_shortage_score: float = Field(
    0.0,
    ge=0.0,
    le=1.0,
    description="Confidence score (0.0 to 1.0) indicating presence of business shortage"
    )
    