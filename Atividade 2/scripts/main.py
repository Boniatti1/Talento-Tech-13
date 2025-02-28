import yfinance as yf
from pathlib import Path

PATH = Path(__file__).parent
DATA_3_MONTHS = PATH.parent / "data" / "data_3_months.csv"
DATA_6_MONTHS = PATH.parent / "data" / "data_6_months.csv"
DATA_1_YEAR = PATH.parent / "data" / "data_1_year.csv"
DATA_2_YEARS = PATH.parent / "data" / "data_2_years.csv"

data_3_months = yf.download("GC=F", start="2024-11-01", end="2025-02-01")
data_6_months = yf.download("GC=F", start="2024-08-01", end="2025-02-01")
data_2_years = yf.download("GC=F", start="2023-02-01", end="2025-02-01")
data_1_year = yf.download("GC=F", start="2024-02-01", end="2025-02-01")

data_3_months.to_csv(DATA_3_MONTHS) 
data_6_months.to_csv(DATA_6_MONTHS)
data_2_years.to_csv(DATA_2_YEARS)
data_1_year.to_csv(DATA_1_YEAR)
