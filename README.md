# Energy Monitor API

An API designed to query and analyze energy consumption data by sector from a local data.csv source.

Installation

```bash
pip install -r requirements.txt
```

Usage
Start the development server using Uvicorn:

```bash
uvicorn main:app --reload
```

API Endpoints

- `/` - Returns the API status and a summary of available sectors.
- `/sectors` - Returns a comprehensive list of all sectors present in the dataset.
- `/consumption/{setor}` - Returns detailed consumption metrics for the specified sector, including:

    Time-series consumption values.
    Average consumption ($\bar{x}$).
    Peak consumption values.

Data Source

- The API processes data from a data.csv file located in the root directory. Ensure the file is correctly formatted before starting the service