import os
import re
import pandas as pd

pasta_unidades = r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\common\units"
padrao = re.compile(r'^\s*(defense|breakthrough|soft_attack|hard_attack|max_organization|armor_value)\s*=\s*([0-9.]+)', re.MULTILINE)

# Lista vazia que vai guardar todas as unidades
dados_extraidos = []

for nome_arquivo in os.listdir(pasta_unidades):
    if nome_arquivo.endswith('.txt'):
        caminho_completo = os.path.join(pasta_unidades, nome_arquivo)
        
        with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as arquivo:
            conteudo = arquivo.read()
            resultados = padrao.findall(conteudo)
            
            # Só processa se o regex encontrou status militares no arquivo
            if resultados:
                status_unidade = {'unidade': nome_arquivo.replace('.txt', '')}
                
                for atributo, valor in resultados:
                    status_unidade[atributo] = float(valor)
                    
                dados_extraidos.append(status_unidade)

df = pd.DataFrame(dados_extraidos)

#Unidades sem blindagem (armor_value) ficam com valor nulo (NaN).
df = df.fillna(0)

df.to_csv('status_base_hoi4.csv', index=False)

print("✅ CSV 'status_base_hoi4.csv' gerado com sucesso!")
print("\n--- Visualização das 5 primeiras linhas ---")
print(df.head())