import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("./data analysis\dataset.csv")

print(df.head())

colunas = df.columns.drop("victory")

grupos = df.groupby(list(colunas))["victory"].nunique()

conflitos = grupos[grupos > 1]

print("Combinações com resultados conflitantes:")
print(conflitos)

duplicados = df[df.duplicated(keep=False)]

print(duplicados)

colunas = df.columns.drop("victory")

duplicados = df[df.duplicated(subset=colunas, keep=False)]

print(duplicados)
