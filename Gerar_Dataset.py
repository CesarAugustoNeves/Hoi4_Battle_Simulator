import pandas as pd
import random

dados_batalhas = []
quantidade_batalhas = 10000

print(f"Gerando {quantidade_batalhas} batalhas simuladas...")

for i in range(quantidade_batalhas):
    # Atributos da Divisão Atacante
    atk_soft_attack = random.randint(50, 800)
    atk_breakthrough = random.randint(30, 500)
    atk_org = random.randint(30, 80)
    
    # Atributos da Divisão Defensora
    def_defense = random.randint(100, 1000)
    def_soft_attack = random.randint(40, 600)
    def_org = random.randint(30, 80)
    
    # Matemática do Combate 
    # Atacante causa dano à organização do defensor superando a defesa
    dano_no_defensor = (atk_soft_attack / max(10, def_defense - atk_soft_attack)) * 10
    
    # Defensor causa dano ao atacante superando o breakthrough
    dano_no_atacante = (def_soft_attack / max(10, atk_breakthrough - def_soft_attack)) * 10
    
    # Quantos turnos cada um sobrevive recebendo esse dano
    turnos_para_defensor_cair = def_org / max(0.1, dano_no_defensor)
    turnos_para_atacante_cair = atk_org / max(0.1, dano_no_atacante)
    
    # 1 = Atacante Venceu, 0 = Defensor Venceu
    victory = 1 if turnos_para_defensor_cair < turnos_para_atacante_cair else 0
    
    dados_batalhas.append({
        'atk_soft_attack': atk_soft_attack,
        'atk_breakthrough': atk_breakthrough,
        'atk_org': atk_org,
        'def_defense': def_defense,
        'def_soft_attack': def_soft_attack,
        'def_org': def_org,
        'victory': victory
    })

df_batalhas = pd.DataFrame(dados_batalhas)
df_batalhas.to_csv('dataset_treinamento_ia.csv', index=False)

print("✅ Dataset 'dataset_treinamento_ia.csv' gerado com sucesso!")