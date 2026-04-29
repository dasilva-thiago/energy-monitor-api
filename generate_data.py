from faker import Faker
import pandas as pd
import random

fake = Faker()

dados = []

setores = ["industrial", "comercial", "residencial"]

for _ in range(200):
    timestamp = fake.date_time_this_month()
    setor = random.choice(setores)
    consumo = random.randint(50, 200)

    dados.append({
        "timestamp": timestamp,
        "setor": setor,
        "consumo": consumo
    })

df = pd.DataFrame(dados)
df.to_csv("data.csv", index=False)

print("Dados gerados com sucesso!")