# Energy Monitor API

A REST API built with **FastAPI** to query and analyze energy consumption data by sector, served from a local `data.csv` source. Includes a lightweight browser frontend using **Brython** (Python in the browser).

---

## Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI + Uvicorn |
| Data | Pandas |
| Frontend | HTML + Brython + CSS |

---

## Installation

```bash
pip install -r requirements.txt
```

To generate sample data before starting the server:

```bash
pip install faker
python generate_data.py
```

This creates a `data.csv` file with 200 randomized records spread across the three sectors.

---

## Running

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

The frontend (`static/index.html`) expects the API to be running on that same address and can be opened directly in the browser.

---

## Data Format

The API reads from `data.csv` in the project root. The file must have the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | datetime | Date and time of the reading |
| `sector` | string | One of: `industrial`, `comercial`, `residencial` |
| `consumption` | number | Energy consumption value (kWh) |

---

## API Endpoints

### `GET /`
Returns the API status and a summary of the loaded dataset.

**Response:**
```json
{
  "status": "ok",
  "sectors": ["industrial", "comercial", "residencial"],
  "total_records": 200
}
```

---

### `GET /sectors`
Returns all distinct sectors present in the dataset.

**Response:**
```json
{
  "sectors": ["industrial", "comercial", "residencial"],
  "count": 3
}
```

---

### `GET /consumption/{sector}`
Returns detailed consumption metrics for a specific sector.

**Path parameter:** `sector` — one of `industrial`, `comercial`, or `residencial`.

**Response:**
```json
{
  "sector": "industrial",
  "values": [130, 167, 105, "..."],
  "average": 127.43,
  "peak": 200.0,
  "minimum": 50.0,
  "total_records": 68
}
```
---

## Interactive Docs

FastAPI exposes auto-generated documentation at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## License

MIT © 2026 Thiago da Silva