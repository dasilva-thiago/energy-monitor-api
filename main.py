from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from enum import Enum

class StrEnum(str, Enum):
    # Inheriting from str makes FastAPI treat it as a string in the URL
    industrial = "industrial"
    comercial = "comercial"
    residencial = "residencial"

app = FastAPI(
    title="Energy Monitor API",
    description="API for monitoring energy consumption by sector.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = Path("data.csv")

class StatusResponse(BaseModel):
    status: str = Field(description="API status. Always 'ok' if running.")
    sectors: list[str] = Field(description="List of available sectors in the dataset.")
    total_records: int = Field(description="Total records loaded from the CSV.")

class SectorsResponse(BaseModel):
    sectors: list[str] = Field(description="Unique names of all sectors.")
    count: int = Field(description="Number of distinct sectors.")

class ConsumptionResponse(BaseModel):
    sector: str = Field(description="Name of the queried sector.")
    values: list[float] = Field(description="All recorded consumption values.")
    average: float = Field(description="Arithmetic mean of consumption.")
    peak: float = Field(description="Maximum recorded value.")
    minimum: float = Field(description="Minimum recorded value.")
    total_records: int = Field(description="Number of readings for this sector.")

def load_data(file_path: Path) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

@app.on_event("startup")
def startup_load_data() -> None:
    try:
        app.state.df = load_data(DATA_FILE)
    except FileNotFoundError:
        app.state.df = pd.DataFrame(columns=["timestamp", "sector", "consumption"])
    except Exception:
        raise

@app.get("/", response_model=StatusResponse)
def root() -> StatusResponse:
    df = app.state.df
    sectors: list[str] = []

    if not df.empty and "sector" in df.columns:
        sectors = df["sector"].dropna().unique().tolist()

    return StatusResponse(
        status="ok",
        sectors=sectors,
        total_records=len(df),
    )

@app.get("/sectors", response_model=SectorsResponse)
def list_sectors() -> SectorsResponse:
    df = app.state.df

    if df.empty:
        return SectorsResponse(sectors=[], count=0)

    sectors = df["sector"].dropna().unique().tolist()
    return SectorsResponse(sectors=sectors, count=len(sectors))

@app.get("/consumption/{sector}", response_model=ConsumptionResponse)
def get_consumption(sector: StrEnum) -> ConsumptionResponse:
    df = app.state.df

    if df.empty:
        raise HTTPException(status_code=503, detail="Data not loaded.")
    
    data = df[df["sector"] == sector.value]
    consumption = data["consumption"]
    # .value extracts the string ("industrial") from the Enum member

    return ConsumptionResponse(
        sector=sector.value,
        values=consumption.tolist(),
        average=round(float(consumption.mean()), 2),
        peak=float(consumption.max()),
        minimum=float(consumption.min()),
        total_records=len(consumption),
    )

    if df.empty or "sector" not in df.columns or "consumption" not in df.columns:
        raise HTTPException(
            status_code=500,
            detail="Data unavailable or malformed on the server.",
        )

    normalized_sector = sector.strip().lower()
    data = df[df["sector"].str.lower() == normalized_sector]

    if data.empty:
        valid_sectors = df["sector"].dropna().unique().tolist()
        raise HTTPException(
            status_code=404,
            detail=f"Sector '{sector}' not found. Available sectors: {valid_sectors}",
        )

    consumption = data["consumption"]

    return ConsumptionResponse(
        sector=normalized_sector,
        values=consumption.tolist(),
        average=round(float(consumption.mean()), 2),
        peak=float(consumption.max()),
        minimum=float(consumption.min()),
        total_records=len(consumption),
    )