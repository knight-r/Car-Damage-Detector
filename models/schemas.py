from pydantic import BaseModel, Field
from typing import List, Optional

class DamageDetail(BaseModel):
    type: str = Field(..., description="Type of damage (e.g., 'Side Panel Dent', 'Scratch', 'Broken Glass')")
    bbox: List[int] = Field(..., description="Bounding box coordinates [x1, y1, x2, y2]")
    severity: int = Field(..., ge=1, le=5, description="Severity rating from 1 (minor) to 5 (severe)")
    description: str = Field(..., description="Detailed description of the damage")

class CarDamageResponse(BaseModel):
    image_name: str
    damages: List[DamageDetail]
    total_damages: int
    overall_severity: str  # "minor", "moderate", "severe"

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None