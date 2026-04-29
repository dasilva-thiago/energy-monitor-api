from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI(title="Energy Monitor API")

# CORS (liberal for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = Path("data.csv")


def load_data(file_path: Path) -> pd.DataFrame:
    """Load CSV and normalize timestamp column if present."""
    df = pd.read_csv(file_path)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


@app.on_event("startup")
def startup_load_data() -> None:
    """Load data at startup and store on the app state.

    If the file is missing, an empty DataFrame with expected columns is created.
    """
    try:
        app.state.df = load_data(DATA_FILE)
    except FileNotFoundError:
        # create an empty frame with expected columns to keep endpoints stable
        app.state.df = pd.DataFrame(columns=["timestamp", "setor", "consumo"])
    except Exception:
        # re-raise unexpected errors so the server fails fast and the issue is visible
        raise


@app.get("/")
def root():
    """Health-check and quick summary."""
    sectors = []
    if not app.state.df.empty and "setor" in app.state.df.columns:
        sectors = app.state.df["setor"].dropna().unique().tolist()
    return {"status": "ok", "sectors": sectors}


@app.get("/sectors")
def list_sectors() -> dict:
    """Return the list of known sectors."""
    if app.state.df.empty:
        return {"sectors": []}
    return {"sectors": app.state.df["setor"].dropna().unique().tolist()}


@app.get("/consumption/{setor}")
def get_consumption(setor: str) -> dict:
    """Return consumption values, mean and peak for a given `setor`."""
    df = app.state.df
    if df.empty or "setor" not in df.columns or "consumo" not in df.columns:
        raise HTTPException(status_code=500, detail="Data not available or malformed")

    data = df[df["setor"] == setor]
    if data.empty:
        raise HTTPException(status_code=404, detail=f"No data for sector '{setor}'")

    media = float(data["consumo"].mean())
    pico = float(data["consumo"].max())

    return {
        "valores": data["consumo"].tolist(),
        "media": media,
        "pico": pico,
    }