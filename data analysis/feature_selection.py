
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import chi2, SelectKBest, RFE
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# Separando os dados

df = pd.read_csv("./dataset.csv")


X = df.iloc[:, 1:17].copy()
y = df.iloc[:, -1].copy()

feature_names = X.columns

print("=" * 50)
print("DIMENSÕES DO DATASET")
print("=" * 50)
print(f"Quantidade de amostras: {len(X)}")
print(f"Quantidade de features: {X.shape[1]}")

# 2. Importancia de features pelo random forest

print("1. RANDOM FOREST")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=42, stratify=y
)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

importances = pd.Series(
    model.feature_importances_,
    index=feature_names
).sort_values(ascending=False)

print("\nImportância de cada feature:")
print(importances)

# Gráfico de importância
plt.figure(figsize=(10, 6))
sns.barplot(x=importances.values, y=importances.index)
plt.title("Random Forest - Importância das Features")
plt.xlabel("Importância")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()

# 3. SELECTKBEST - TESTE QUI-QUADRADO

print("2. SELECTKBEST - QUI-QUADRADO")

# O chi2 exige features não negativas.
if (X < 0).any().any():
    print(
        "\nNão foi possível aplicar chi2: "
        "existem features com valores negativos."
    )
else:
    seletor = SelectKBest(score_func=chi2, k=6)
    seletor.fit(X, y)

    features_chi2 = X.columns[seletor.get_support()]

    print("\n6 features selecionadas:")
    print(features_chi2.tolist())

    pontuacoes = pd.DataFrame({
        "Feature": X.columns,
        "Pontuação qui-quadrado": seletor.scores_
    })

    print("\nRanking das features:")
    print(
        pontuacoes.sort_values(
            by="Pontuação qui-quadrado",
            ascending=False
        ).to_string(index=False)
    )

# 4. RFE - LINEAR SVC

print("3. RFE - LINEAR SVC")

# Padronização para ajudar o SVM quando as escalas diferem.
model_svc = make_pipeline(
    StandardScaler(),
    LinearSVC(random_state=42, max_iter=10000)
)

rfe = RFE(
    estimator=model_svc,
    n_features_to_select=6,
    step=1
)

rfe.fit(X, y)

print("\n6 features selecionadas:")
print(X.columns[rfe.support_].tolist())

ranking = pd.DataFrame({
    "Feature": X.columns,
    "Selecionada": rfe.support_,
    "Ranking": rfe.ranking_
})

print("\nRanking de todas as features:")
print(ranking.sort_values("Ranking").to_string(index=False))

#Referencia: https://medium.com/data-hackers/como-selecionar-as-melhores-features-para-seu-modelo-de-machine-learning-faf74e357913