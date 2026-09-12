
import math
import random
import sys

from Combate import simular_batalha

BASE = dict(
    atk_soft_attack=425, atk_hard_attack=204, atk_breakthrough=265,
    atk_org=55, atk_armor=60, atk_hardness=0.5, atk_supply=0.65,
    def_defense=550, def_soft_attack=320, def_hard_attack=155,
    def_org=55, def_piercing=60, def_entrenchment=12, def_supply=0.65,
    terrain_mod=0.74, fort_level=0, cas_support=0,
)

falhas = []


def checar(condicao, descricao):
    status = "OK  " if condicao else "FAIL"
    print(f"[{status}] {descricao}")
    if not condicao:
        falhas.append(descricao)


def rodar(**overrides):
    params = {**BASE, **overrides}
    return simular_batalha(**params)


def eh_monotonico(nome_param, valores, chave_metrica, crescente=True):
    """Ordena `valores` de forma crescente, roda a batalha pra cada um e checa
    se `chave_metrica` (ex: 'turnos_atacante') se move na direção esperada
    conforme o parâmetro aumenta. `crescente=False` checa se a métrica cai."""
    valores_ordenados = sorted(valores)
    metricas = [rodar(**{nome_param: v})[chave_metrica] for v in valores_ordenados]
    for anterior, atual in zip(metricas, metricas[1:]):
        if crescente and atual < anterior - 1e-9:
            return False
        if not crescente and atual > anterior + 1e-9:
            return False
    return True


print("=" * 70)
print("TESTES DE SANIDADE — combate.py")
print("=" * 70)


# ---------------------------------------------------------------------
print("\n--- Suprimento ---")
checar(
    eh_monotonico("atk_supply", [0.3, 0.5, 0.65, 0.8, 1.0], "turnos_defensor", crescente=False),
    "atk_supply MAIOR -> turnos_defensor cai (defensor quebra mais rápido)"
)
checar(
    eh_monotonico("def_supply", [0.3, 0.5, 0.65, 0.8, 1.0], "turnos_atacante", crescente=False),
    "def_supply MAIOR -> turnos_atacante cai (atacante quebra mais rápido)"
)


# ---------------------------------------------------------------------
print("\n--- Organização ---")
checar(
    eh_monotonico("atk_org", [30, 45, 55, 65, 80], "turnos_atacante", crescente=True),
    "atk_org MAIOR -> turnos_atacante cresce (mais fôlego pro atacante)"
)
checar(
    eh_monotonico("def_org", [30, 45, 55, 65, 80], "turnos_defensor", crescente=True),
    "def_org MAIOR -> turnos_defensor cresce (mais fôlego pro defensor)"
)


# ---------------------------------------------------------------------
print("\n--- Fortificação e terreno ---")
checar(
    eh_monotonico("fort_level", [0, 1, 2, 3, 5, 10], "turnos_defensor", crescente=True),
    "fort_level MAIOR -> turnos_defensor cresce (forte reduz dano do atacante)"
)
checar(
    eh_monotonico("terrain_mod", [0.4, 0.6, 0.8, 0.9, 1.0], "turnos_defensor", crescente=False),
    "terrain_mod MAIOR (terreno mais fácil) -> turnos_defensor cai"
)
checar(
    eh_monotonico("def_entrenchment", [0, 5, 10, 15, 20, 25], "turnos_defensor", crescente=True),
    "def_entrenchment MAIOR -> turnos_defensor cresce (mais difícil de desalojar)"
)


# ---------------------------------------------------------------------
print("\n--- Breakthrough e defesa ---")
checar(
    eh_monotonico("atk_breakthrough", [30, 100, 200, 300, 400, 500], "turnos_atacante", crescente=True),
    "atk_breakthrough MAIOR -> turnos_atacante cresce (atacante resiste mais ao contra-ataque)"
)
checar(
    eh_monotonico("def_defense", [100, 300, 550, 750, 1000], "turnos_defensor", crescente=True),
    "def_defense MAIOR -> turnos_defensor cresce (mais difícil de desalojar)"
)


# ---------------------------------------------------------------------
print("\n--- Blindagem e suporte aéreo ---")
sem_blindagem = rodar(atk_armor=50, def_piercing=80, atk_hardness=0.5)
com_blindagem = rodar(atk_armor=100, def_piercing=50, atk_hardness=0.5)
checar(
    com_blindagem["multiplicador_dano_tanque"] == 1.5 and sem_blindagem["multiplicador_dano_tanque"] == 1.0,
    "armor > piercing (com hardness>0.3) ativa o multiplicador de 1.5x"
)
checar(
    com_blindagem["dano_no_defensor"] > sem_blindagem["dano_no_defensor"],
    "Bônus de blindagem realmente aumenta o dano no defensor"
)
checar(
    rodar(atk_armor=100, def_piercing=50, atk_hardness=0.2)["multiplicador_dano_tanque"] == 1.0,
    "Blindagem NÃO ativa bônus se atk_hardness <= 0.3 (regra de dureza mínima respeitada)"
)
checar(
    rodar(cas_support=1)["dano_no_defensor"] > rodar(cas_support=0)["dano_no_defensor"],
    "cas_support=1 aumenta o dano no defensor (+25%)"
)


# ---------------------------------------------------------------------
print("\n--- Robustez numérica (valores extremos aleatórios) ---")
random.seed(42)
problemas = 0
for _ in range(20000):
    r = simular_batalha(
        atk_soft_attack=random.randint(50, 800), atk_hard_attack=random.randint(10, 400),
        atk_breakthrough=random.randint(30, 500), atk_org=random.randint(30, 80),
        atk_armor=random.randint(0, 120), atk_hardness=round(random.uniform(0, 1), 2),
        atk_supply=round(random.uniform(0.3, 1.0), 2),
        def_defense=random.randint(100, 1000), def_soft_attack=random.randint(40, 600),
        def_hard_attack=random.randint(10, 300), def_org=random.randint(30, 80),
        def_piercing=random.randint(0, 120), def_entrenchment=random.randint(0, 25),
        def_supply=round(random.uniform(0.3, 1.0), 2),
        terrain_mod=random.choice([1.0, 0.9, 0.8, 0.6, 0.4]),
        fort_level=random.choice([0, 1, 2, 3, 5, 10]),
        cas_support=random.choice([0, 1]),
    )
    valores = [r["dano_no_defensor"], r["dano_no_atacante"], r["turnos_defensor"], r["turnos_atacante"]]
    if any(math.isnan(v) or math.isinf(v) or v < 0 for v in valores):
        problemas += 1
checar(problemas == 0, f"0 batalhas com NaN/Inf/negativo em 20.000 simulações (encontrados: {problemas})")


# ---------------------------------------------------------------------
print("\n--- Balanceamento geral da taxa de vitória ---")
random.seed(7)
vitorias = 0
N = 20000
for _ in range(N):
    r = simular_batalha(
        atk_soft_attack=random.randint(50, 800), atk_hard_attack=random.randint(10, 400),
        atk_breakthrough=random.randint(30, 500), atk_org=random.randint(30, 80),
        atk_armor=random.randint(0, 120), atk_hardness=round(random.uniform(0, 1), 2),
        atk_supply=round(random.uniform(0.3, 1.0), 2),
        def_defense=random.randint(100, 1000), def_soft_attack=random.randint(40, 600),
        def_hard_attack=random.randint(10, 300), def_org=random.randint(30, 80),
        def_piercing=random.randint(0, 120), def_entrenchment=random.randint(0, 25),
        def_supply=round(random.uniform(0.3, 1.0), 2),
        terrain_mod=random.choice([1.0, 0.9, 0.8, 0.6, 0.4]),
        fort_level=random.choice([0, 0, 0, 1, 2, 3, 5, 10]),
        cas_support=random.choice([0, 0, 1]),
    )
    vitorias += r["victory"]
taxa = vitorias / N
checar(0.40 <= taxa <= 0.60, f"Taxa de vitória do atacante em {taxa:.1%} (esperado entre 40% e 60%)")

# ---------------------------------------------------------------------
print("\n" + "=" * 70)
if falhas:
    print(f"❌ {len(falhas)} TESTE(S) FALHARAM:")
    for f in falhas:
        print(f"   - {f}")
    sys.exit(1)
else:
    print("✅ TODOS OS TESTES PASSARAM — mecânicas de combate validadas.")
    sys.exit(0)