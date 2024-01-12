from pydantic import BaseModel, ConfigDict, validator
from typing import Optional
from datetime import datetime
import math

class SummaryDataModel(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id: int
    structure: str
    element_status: str
    base_name: str
    attribute_name: Optional[str]
    other_name: Optional[str]
    category_code: str
    tags: Optional[str]
    unit: str
    contributor: Optional[str]
    program: Optional[str]
    program_url: Optional[str]
    source: Optional[str]
    location: str
    sub_location: str
    creation_date: datetime
    last_update_date: datetime
    validity_period: datetime
    uncertainty: Optional[float]
    reglementations: Optional[str]
    transparency: Optional[str]
    quality: Optional[str]
    quality_ter: Optional[str]
    quality_gr: Optional[str]
    quality_tir: Optional[str]
    quality_c: Optional[str]
    quality_p: Optional[str]
    quality_m: Optional[str]
    comment: Optional[str]
    emission_type: str
    emission_type_name: Optional[str]
    unaggregated_total: float
    co2f: float
    ch4f: float
    ch4b: float
    n2o: float
    other_greenhouse_gas: float
    co2b: float
    sf6: int

    @validator('*', pre=True, allow_reuse=True)
    def handle_non_compliant_values(cls, v):
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return None  # Replace non-compliant values with None
        return v

class DetailedDataModel(BaseModel):

    model_config = ConfigDict(from_attributes = True)

    id: int
    summary_id: int
    structure: str
    element_status: str
    base_name: str
    attribute_name: Optional[str]
    other_name: Optional[str]
    category_code: str
    tags: Optional[str]
    unit: str
    creation_date: datetime
    last_update_date: datetime
    validity_period: datetime
    uncertainty: Optional[float]
    reglementations: Optional[str]
    transparency: Optional[str]
    quality: Optional[str]
    quality_ter: Optional[str]
    quality_gr: Optional[str]
    quality_tir: Optional[str]
    quality_c: Optional[str]
    quality_p: Optional[str]
    quality_m: Optional[str]
    comment: Optional[str]
    emission_type: str
    emission_type_name: Optional[str]
    unaggregated_total: float
    co2f: float
    ch4f: float
    ch4b: float
    n2o: float
    other_greenhouse_gas: float
    co2b: float
    sf6: int

    @validator('*', pre=True, allow_reuse=True)
    def handle_non_compliant_values(cls, v):
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return None  # Replace non-compliant values with None
        return v