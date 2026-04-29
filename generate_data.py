import random
from faker import Faker
import pandas as pd

fake = Faker()

PROFILES = {
    "industrial":  {"day": (150, 200), "night": (80, 130)},
    "comercial":   {"day": (100, 180), "night": (50, 90)},
    "residencial": {"day": (60, 100),  "night": (130, 200)},
}

dados = []
setores = list(PROFILES.keys())

for _ in range(300):
    timestamp = fake.date_time_this_month()
    sector     = random.choice(setores)
    period    = "day" if 6 <= timestamp.hour < 20 else "night"
    low, high = PROFILES[sector][period]
    consumption   = random.randint(low, high)

    dados.append({"timestamp": timestamp, "sector": sector, "consumption": consumption})    

pd.DataFrame(dados).to_csv("data.csv", index=False)
print(f"{len(dados)} records generated with realistic profile.")