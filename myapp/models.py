from sqlmodel import SQLModel, Field, ForeignKey
from typing import Optional
import datetime

class SummaryData(SQLModel, table=True):
    id: int = Field(primary_key=True)
    structure: str
    element_status: str = Field(index=True)
    base_name: str
    attribute_name: Optional[str]
    other_name: Optional[str]
    category_code: str = Field(index=True)
    tags: Optional[str]
    unit: str
    contributor: Optional[str]
    program: Optional[str]
    program_url: Optional[str]
    source: Optional[str]
    location: str = Field(index=True)
    sub_location: str
    creation_date: datetime.datetime
    last_update_date: datetime.datetime
    validity_period: datetime.datetime
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

class DetailedData(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    summary_id: int = Field(default=None, foreign_key="summarydata.id")
    structure: str
    element_status: str = Field(index=True)
    base_name: str
    attribute_name: Optional[str]
    other_name: Optional[str]
    category_code: str = Field(index=True)
    tags: Optional[str]
    unit: str
    creation_date: datetime.datetime
    last_update_date: datetime.datetime
    validity_period: datetime.datetime
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