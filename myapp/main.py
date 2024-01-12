import logging
from typing import List
from fastapi import FastAPI, HTTPException
from myapp.database import create_db_and_tables
from myapp.db_operations import fetch_all_summary_data, fetch_detailed_data_by_summary_id, fetch_one_detailed_data, fetch_one_summary_data, fetch_summary_data_by_filter
from myapp.pydantic_models import DetailedDataModel, SummaryDataModel
from myapp.explore_data import process_and_load_data

create_db_and_tables()
process_and_load_data()

app = FastAPI()

@app.get("/summary-data/{id}", response_model=SummaryDataModel)
async def get_one_summary_data(id: int):
    try:
        data = fetch_one_summary_data(id)
        if data is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return data
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summary-data", response_model=list[SummaryDataModel])
async def get_all_summary_data():
    try:
        data = fetch_all_summary_data()
        if data is None:
            raise HTTPException(status_code=404, detail="Table is empty")
        return data
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/detailed-data/by-summary/{summary_id}", response_model=List[DetailedDataModel])
async def get_detailed_data_by_summary_id(summary_id: int):
    try:
        data = fetch_detailed_data_by_summary_id(summary_id)
        if data == [] or None:
            raise HTTPException(status_code=404, detail="No linked data")
        return data
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/detailed-data/{id}", response_model=DetailedDataModel)
async def get_one_detailed_data(id: int):
    try:
        data = fetch_one_detailed_data(id)
        if data is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return data
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summary-data/filter", response_model=List[SummaryDataModel])
async def filter_summary_data(column_name: str, filter_value: str):
    try:
        data = fetch_summary_data_by_filter(column_name, filter_value)
        if not data:
            raise HTTPException(status_code=404, detail=f"No data found for column '{column_name}' with value '{filter_value}'")
        return data
    except Exception as e:
        logging.error(f"Error fetching data by column: {e}")
        raise HTTPException(status_code=500, detail=str(e))


