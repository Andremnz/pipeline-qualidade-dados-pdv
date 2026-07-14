# -*- coding: utf-8 -*-
"""
Gera uma amostra sintética de vendas no formato do relatório do PDV Consumer.
Nenhum dado real de cliente é usado aqui. Os produtos e preços são aproximados
para manter a escala realista (~R$ 2M em 29 meses de operação).
"""
import csv
import random
from datetime import datetime, timedelta

random.seed(42)

# produtos com peso de frequência (simula distribuição real: combos vendem mais)
produtos = [
    # (nome, preco_unitario, peso_frequencia)
    ("Combo 5 - 40 Peças",    149.00, 12),
    ("Combo 4 - 35 Peças",    122.50, 10),
    ("Combo 2 - 30 Peças",     98.50, 11),
    ("Combo 8 - 60 Peças",    243.00,  4),
    ("Temaki Salmão Philadelphia", 32.80, 20),
    ("Combo 1 - 25 Peças",     95.00,  8),
    ("Poke Salmão",            55.00,  9),
    ("Hot Salmão Philadelphia", 32.00, 13),
    ("Combo Omaki - 40 Peças", 132.00,  3),
    ("Uramaki Salmão Cream Cheese", 29.90, 8),
    ("Teppanyaki Misto",        58.50, 5),
    ("Ceviche Peixe Branco",    40.20, 6),
    ("Yakisoba de Carne",       42.00, 5),
    ("Sashimi Salmão 10 Peças", 45.00, 5),
    ("Guioza 6 Peças",          22.00, 7),
    ("Temaki Filadelfia",       32.00, 5),
    ("Harumaki 4 Peças",        18.50, 4),
    ("Hossomaki Salmão 10 Peças", 25.00, 4),
    ("Misso Shiro",             12.00, 6),
    ("Niguiri Salmão 4 Peças",  28.00, 3),
    ("Coca-Cola Lata",           6.00, 15),
    ("Água Mineral",             4.00, 10),
    ("Suco Natural",             9.00,  4),
    ("Cerveja Artesanal",       14.00,  5),
]

nomes =  [p[0] for p in produtos]
precos = [p[1] for p in produtos]
pesos =  [p[2] for p in produtos]

tipos = ["Mesa/Comanda", "Balcão"]
inicio = datetime(2023, 7, 1, 18, 0)
meses_operacao = 29
campos = ["Nome Prod", "Qtd.", "Valor Un. Item", "Valor. Tot. Item",
          "Data Ab. Ped.", "Data Fec. Ped.", "Tipo Ped.", "Núm. Mesa/Com."]

linhas = []
n_linhas = 3000

for _ in range(n_linhas):
    idx = random.choices(range(len(produtos)), weights=pesos, k=1)[0]
    nome = nomes[idx]
    preco = precos[idx]
    qtd = random.choices([1, 2, 3, 4], weights=[50, 30, 15, 5], k=1)[0]
    total = round(preco * qtd, 2)

    # alterna entre formato brasileiro ("89,90") e formato decimal ("89.90")
    if random.random() < 0.5:
        vlr_unit = f"{preco:.2f}".replace(".", ",")
        vlr_total = f"{total:.2f}".replace(".", ",")
    else:
        vlr_unit = f"{preco:.2f}"
        vlr_total = f"{total:.2f}"

    # injeta ~5% de divergência no total para o verificador do etl pegar
    if random.random() < 0.05:
        vlr_total = f"{total + random.choice([5, 10, -3]):.2f}".replace(".", ",")

    tipo = random.choices(tipos, weights=[0.6, 0.4])[0]
    dias_offset = random.randint(0, meses_operacao * 30)
    ab = inicio + timedelta(days=dias_offset, minutes=random.randint(0, 300))
    fec = ab + timedelta(minutes=random.randint(15, 120))
    mesa = random.randint(1, 20) if tipo == "Mesa/Comanda" else ""

    linhas.append({
        "Nome Prod": nome,
        "Qtd.": qtd,
        "Valor Un. Item": vlr_unit,
        "Valor. Tot. Item": vlr_total,
        "Data Ab. Ped.": ab.strftime("%d/%m/%Y %H:%M"),
        "Data Fec. Ped.": fec.strftime("%d/%m/%Y %H:%M"),
        "Tipo Ped.": tipo,
        "Núm. Mesa/Com.": mesa,
    })

with open("vendas_exemplo.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=campos, delimiter=";")
    w.writeheader()
    w.writerows(linhas)

print(f"Gerado vendas_exemplo.csv com {len(linhas)} linhas sintéticas.")
