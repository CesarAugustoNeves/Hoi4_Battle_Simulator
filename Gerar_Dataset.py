import pandas as pd
import random

dados_batalhas = []
quantidade_batalhas = 15000

print(f"Gerando {quantidade_batalhas} batalhas simuladas...")

for i in range(quantidade_batalhas):
    # Atributos da Divisão Atacante
    atk_soft_attack = random.randint(50, 800)
    atk_hard_attack = random.randint(10, 400)
    atk_breakthrough = random.randint(30, 500)
    atk_org = random.randint(30, 80)
    atk_armor = random.randint(0, 120)
    atk_hardness = round(random.uniform(0.0, 1.0), 2)
    atk_supply = round(random.uniform(0.3, 1.0), 2)
    
    # Atributos da Divisão Defensora
    def_defense = random.randint(100, 1000)
    def_soft_attack = random.randint(40, 600)
    def_hard_attack = random.randint(10, 300)
    def_org = random.randint(30, 80)
    def_piercing = random.randint(0, 120)
    def_entrenchment = random.randint(0, 25)
    def_supply = round(random.uniform(0.3, 1.0), 2)

    # Atributos do Campo de Batalha
    terrain_mod = round(random.choice([1.0, 0.9, 0.8, 0.6, 0.4]), 2) # Planície, Floresta, Colina, Montanha, Marsh
    fort_level = random.choice([0, 0, 0, 1, 2, 3, 5, 10]) # Maioria das batalhas sem forte
    cas_support = random.choice([0, 0, 1]) # 1 para suporte aéreo presente

    #-------------------- Matemática do Combate -------------------------#


    # Defesa real do defensor (aumenta com nivel de forte e entrincheiramento)
    def_efetiva = (def_defense * (1 + (def_entrenchment * 0.02)))
    
    # Ataque real do atacante (reduzido por terreno, fortes e falta de suprimento, aumentado por CAS)
    penalidade_fortes = max(0.1, 1.0 - (fort_level * 0.15))
    bonificacao_cas = 1.25 if cas_support == 1 else 1.0
    
    # O dano do atacante é calculado pela dureza (Hardness) do defensor
    atk_efetivo = ((atk_soft_attack * (1 - 0.2)) + (atk_hard_attack * 0.2)) * terrain_mod * penalidade_fortes * atk_supply * bonificacao_cas
    
    # Regra de Ouro da Blindagem (Armor vs Piercing)
    multiplicador_dano_tanque = 1.0
    if atk_armor > def_piercing and atk_hardness > 0.3:
        multiplicador_dano_tanque = 1.5 # Tanque do atacante não foi perfurado!
        
    # Cálculo de Dano por Turno
    dano_no_defensor = (atk_efetivo / max(10, def_efetiva - atk_efetivo)) * 10 * multiplicador_dano_tanque
    dano_no_atacante = (def_soft_attack / max(10, atk_breakthrough - def_soft_attack)) * 10
    
    turnos_defensor = def_org / max(0.1, dano_no_defensor)
    turnos_atacante = atk_org / max(0.1, dano_no_atacante)
    
    # Target: 1 se Atacante venceu, 0 se Defensor venceu
    victory = 1 if turnos_defensor < turnos_atacante else 0
    
    dados_batalhas.append({
        'atk_soft_attack': atk_soft_attack,
        'atk_hard_attack': atk_hard_attack,
        'atk_breakthrough': atk_breakthrough,
        'atk_org': atk_org,
        'atk_armor': atk_armor,
        'atk_hardness': atk_hardness,
        'atk_supply': atk_supply,
        'def_defense': def_defense,
        'def_soft_attack': def_soft_attack,
        'def_hard_attack': def_hard_attack,
        'def_org': def_org,
        'def_piercing': def_piercing,
        'def_entrenchment': def_entrenchment,
        'def_supply': def_supply,
        'terrain_mod': terrain_mod,
        'fort_level': fort_level,
        'cas_support': cas_support,
        'victory': victory
    })

df_batalhas = pd.DataFrame(dados_batalhas)
df_batalhas.to_csv('dataset_treinamento_ia.csv', index=False)

print("✅ Dataset 'dataset_treinamento_ia.csv' gerado com sucesso!")