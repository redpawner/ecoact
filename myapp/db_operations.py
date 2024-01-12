from pydantic import ValidationError
from sqlalchemy import and_
from sqlmodel import Session, select
from myapp.models import DetailedData, SummaryData
from myapp.database import engine
import pandas as pd
import logging

from myapp.pydantic_models import DetailedDataModel, SummaryDataModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def data_already_loaded() -> bool:
    """
    Check if the data is already loaded into the database.
    """
    with Session(engine) as session:
        # Check if there is at least one record in the SummaryData table
        result = session.exec(select(SummaryData).limit(1)).first()
        return result is not None

def insert_summary_data(df: pd.DataFrame) -> None:
    """
    Inserts a dataframe into the database using the SummaryData model.
    """
    logging.info("Inserting summary data...")
    with Session(engine) as session:
        for index, row in df.iterrows():
            try:
                data = SummaryData(
                    id=int(row['id']),
                    structure=row['structure'],
                    element_status=row['element_status'],
                    base_name=row['base_name'],
                    attribute_name=row['attribute_name'],
                    other_name=row['other_name'],
                    category_code=row['category_code'],
                    tags=row['tags'],
                    unit=row['unit'],
                    contributor=row['contributor'],
                    program=row['program'],
                    program_url=row['program_url'],
                    source=row['source'],
                    location=row['location'],
                    sub_location=row['sub_location'],
                    creation_date=row['creation_date'],
                    last_update_date=row['last_update_date'],
                    validity_period=row['validity_period'],
                    uncertainty=row['uncertainty'],
                    reglementations=row['reglementations'],
                    transparency=row['transparency'],
                    quality=row['quality'],
                    quality_ter=row['quality_ter'],
                    quality_gr=row['quality_gr'],
                    quality_tir=row['quality_tir'],
                    quality_c=row['quality_c'],
                    quality_p=row['quality_p'],
                    quality_m=row['quality_m'],
                    comment=row['comment'],
                    emission_type=row['emission_type'],
                    emission_type_name=row['emission_type_name'],
                    unaggregated_total=row['unaggregated_total'],
                    co2f=row['co2f'],
                    ch4f=row['ch4f'],
                    ch4b=row['ch4b'],
                    n2o=row['n2o'],
                    other_greenhouse_gas=row['other_greenhouse_gas'],
                    co2b=row['co2b'],
                    sf6=row['sf6']
                )
                session.add(data)
            except Exception as e:
              logging.error(f"Error inserting row at index {index}: {e}")
              logging.info(f"Row data: {row.to_dict()}")
              session.rollback()
              continue
        session.commit()

def insert_detailed_data(df: pd.DataFrame) -> None:
    """
    Inserts a dataframe into the database using the DetailedData model.
    """

    logging.info('Inserting detailed data...')
    with Session(engine) as session:
        for index, row in df.iterrows():
            try:
                data = DetailedData(
                    summary_id=int(row['id']),
                    structure=row['structure'],
                    element_status=row['element_status'],
                    base_name=row['base_name'],
                    attribute_name=row['attribute_name'],
                    other_name=row['other_name'],
                    category_code=row['category_code'],
                    tags=row['tags'],
                    unit=row['unit'],
                    creation_date=row['creation_date'],
                    last_update_date=row['last_update_date'],
                    validity_period=row['validity_period'],
                    uncertainty=row['uncertainty'],
                    reglementations=row['reglementations'],
                    transparency=row['transparency'],
                    quality=row['quality'],
                    quality_ter=row['quality_ter'],
                    quality_gr=row['quality_gr'],
                    quality_tir=row['quality_tir'],
                    quality_c=row['quality_c'],
                    quality_p=row['quality_p'],
                    quality_m=row['quality_m'],
                    comment=row['comment'],
                    emission_type=row['emission_type'],
                    emission_type_name=row['emission_type_name'],
                    unaggregated_total=row['unaggregated_total'],
                    co2f=row['co2f'],
                    ch4f=row['ch4f'],
                    ch4b=row['ch4b'],
                    n2o=row['n2o'],
                    other_greenhouse_gas=row['other_greenhouse_gas'],
                    co2b=row['co2b'],
                    sf6=row['sf6']
                )
                session.add(data)
                session.commit()
            except Exception as e:
                logging.error(f"Error inserting row at index {index}: {e}")
                session.rollback()
                continue

def fetch_all_summary_data() -> list:
    """
    Fetches all data in the summarydata table
    """
    with Session(engine) as session:
        statement = select(SummaryData)
        results = session.exec(statement)
        data = results.all()
        if data:
              try:
                  return [SummaryDataModel.model_validate(record) for record in data]
              except ValidationError as e:
                  logging.error(f"Validation error: {e}")
                  return None
        return None

def fetch_one_summary_data(id: int):
    """
    Fetches a single row of data in the summarydata table

    Args:
        item_id (int): The id (key) of the desired row of data

    """
    with Session(engine) as session:
        statement = select(SummaryData).where(SummaryData.id == id)
        result = session.exec(statement)
        record = result.first()
        if record:
              try:
                  return SummaryDataModel.model_validate(record)
              except ValidationError as e:
                  logging.error(f"Validation error: {e}")
                  return None
        return None

def fetch_detailed_data_by_summary_id(summary_id: int) -> list:
    """
    Fetches all rows of data linked to a parent row of data in the summary field.

    Args:
        summary_id (int): The id of the parent row in the summarydata table.

    """
    with Session(engine) as session:
        statement = select(DetailedData).where(DetailedData.summary_id == summary_id)
        results = session.exec(statement)
        data = results.all()
        if data:
              try:
                  return [DetailedDataModel.model_validate(record) for record in data]
              except ValidationError as e:
                  logging.error(f"Validation error: {e}")
                  return None
        return None

def fetch_one_detailed_data(id: int):
    """
    Fetches all rows of data linked to a parent row of data in the summary field.

    Args:
        item_id (int): The id (key) of the desired row of data

    """
    with Session(engine) as session:
        statement = select(DetailedData).where(DetailedData.id == id)
        result = session.exec(statement)
        record = result.first()
        if record:
              try:
                  return DetailedDataModel.model_validate(record)
              except ValidationError as e:
                  logging.error(f"Validation error: {e}")
                  return None
        return None

def fetch_summary_data_by_filter(column_name: str, filter_value: str):
    with Session(engine) as session:
        # Create a condition to filter by the specified column and value
        condition = and_(getattr(SummaryData, column_name) == filter_value)

        # Use the condition in the SELECT statement
        statement = select(SummaryData).where(condition)

        results = session.exec(statement)
        data = results.all()
        if data:
            try:
                return [SummaryDataModel.model_validate(record) for record in data]
            except ValidationError as e:
                logging.error(f"Validation error: {e}")
                return []
        return []
