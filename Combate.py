FATOR_CALIBRACAO_DEFESA = 0.3  
DANO_MAXIMO_POR_TURNO = 60


def simular_batalha(
    atk_soft_attack, atk_hard_attack, atk_breakthrough, atk_org, atk_armor, atk_hardness, atk_supply,
    def_defense, def_soft_attack, def_hard_attack, def_org, def_piercing, def_entrenchment, def_supply,
    terrain_mod, fort_level, cas_support,
):
    
    # Poder ofensivo de cada lado
    penalidade_fortes = max(0.1, 1.0 - (fort_level * 0.15))
    bonificacao_cas = 1.25 if cas_support == 1 else 1.0
    atk_efetivo = ((atk_soft_attack * 0.8) + (atk_hard_attack * 0.2)) * terrain_mod * penalidade_fortes * atk_supply * bonificacao_cas
    def_efetivo = ((def_soft_attack * 0.8) + (def_hard_attack * 0.2)) * def_supply

    # Poder de resistência de cada lado
    def_resistencia = def_defense * (1 + (def_entrenchment * 0.02)) * FATOR_CALIBRACAO_DEFESA
    atk_resistencia = atk_breakthrough * (1 + (atk_hardness * 0.3))

    # Blindagem (Armor vs Piercing)
    multiplicador_dano_tanque = 1.5 if (atk_armor > def_piercing and atk_hardness > 0.3) else 1.0

    # Dano por turno 
    dano_no_defensor = (atk_efetivo / (atk_efetivo + def_resistencia)) * DANO_MAXIMO_POR_TURNO * multiplicador_dano_tanque
    dano_no_atacante = (def_efetivo / (def_efetivo + atk_resistencia)) * DANO_MAXIMO_POR_TURNO

    turnos_defensor = def_org / max(0.1, dano_no_defensor)
    turnos_atacante = atk_org / max(0.1, dano_no_atacante)

    victory = 1 if turnos_defensor < turnos_atacante else 0

    return {
        "atk_efetivo": atk_efetivo,
        "def_efetivo": def_efetivo,
        "atk_resistencia": atk_resistencia,
        "def_resistencia": def_resistencia,
        "multiplicador_dano_tanque": multiplicador_dano_tanque,
        "dano_no_defensor": dano_no_defensor,
        "dano_no_atacante": dano_no_atacante,
        "turnos_defensor": turnos_defensor,
        "turnos_atacante": turnos_atacante,
        "victory": victory,
    }