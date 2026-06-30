"""
Copa do Mundo 2026 — Previsões Poisson vs Resultados Reais
Modelo: λ = média(xG_time, xGA_adversário) — fonte: footystats.org
Atualizar RESULTADOS à medida que os jogos são disputados.
"""

# ── PREVISÕES DO MODELO (Poisson, calculadas antes dos jogos) ─────────────────
# Formato: "Time A × Time B": {
#     "fav": "Time A" | "Time B" | "Empate",
#     "pct_a": % vitória A, "pct_emp": % empate, "pct_b": % vitória B,
#     "placar": "mais provável nos 90min",
#     "lambda_a": λA, "lambda_b": λB,
#     "data": "DD/MM"
# }

PREVISOES = {
    "Canadá × África do Sul": {
        "fav": "Canadá", "pct_a": 58, "pct_emp": 22, "pct_b": 20,
        "placar": "1×0", "lambda_a": 1.89, "lambda_b": 0.79, "data": "28/06"
    },
    "Brasil × Japão": {
        "fav": "Brasil", "pct_a": 40, "pct_emp": 27, "pct_b": 33,
        "placar": "1×1", "lambda_a": 1.35, "lambda_b": 1.21, "data": "29/06"
    },
    "Alemanha × Paraguai": {
        "fav": "Alemanha", "pct_a": 66, "pct_emp": 19, "pct_b": 13,
        "placar": "2×0", "lambda_a": 2.21, "lambda_b": 0.85, "data": "29/06"
    },
    "Países Baixos × Marrocos": {
        "fav": "Marrocos", "pct_a": 33, "pct_emp": 24, "pct_b": 42,
        "placar": "1×1", "lambda_a": 1.36, "lambda_b": 1.57, "data": "29/06"
    },
    "Costa do Marfim × Noruega": {
        "fav": "Costa do Marfim", "pct_a": 38, "pct_emp": 25, "pct_b": 36,
        "placar": "1×1", "lambda_a": 1.46, "lambda_b": 1.41, "data": "30/06"
    },
    "França × Suécia": {
        "fav": "França", "pct_a": 44, "pct_emp": 25, "pct_b": 31,
        "placar": "1×1", "lambda_a": 1.54, "lambda_b": 1.25, "data": "30/06"
    },
    "México × Equador": {
        "fav": "Equador", "pct_a": 35, "pct_emp": 26, "pct_b": 39,
        "placar": "1×1", "lambda_a": 1.27, "lambda_b": 1.37, "data": "30/06"
    },
    "Inglaterra × RD Congo": {
        "fav": "Inglaterra", "pct_a": 53, "pct_emp": 24, "pct_b": 22,
        "placar": "1×0", "lambda_a": 1.70, "lambda_b": 1.01, "data": "01/07"
    },
    "Bélgica × Senegal": {
        "fav": "Bélgica", "pct_a": 47, "pct_emp": 22, "pct_b": 29,
        "placar": "1×1", "lambda_a": 1.88, "lambda_b": 1.44, "data": "01/07"
    },
    "EUA × Bósnia": {
        "fav": "EUA", "pct_a": 52, "pct_emp": 25, "pct_b": 22,
        "placar": "1×0", "lambda_a": 1.62, "lambda_b": 0.97, "data": "01/07"
    },
    "Espanha × Áustria": {
        "fav": "Espanha", "pct_a": 58, "pct_emp": 23, "pct_b": 18,
        "placar": "1×0", "lambda_a": 1.76, "lambda_b": 0.84, "data": "02/07"
    },
    "Portugal × Croácia": {
        "fav": "Portugal", "pct_a": 42, "pct_emp": 26, "pct_b": 32,
        "placar": "1×1", "lambda_a": 1.42, "lambda_b": 1.20, "data": "02/07"
    },
    "Suíça × Argélia": {
        "fav": "Suíça", "pct_a": 41, "pct_emp": 26, "pct_b": 32,
        "placar": "1×1", "lambda_a": 1.45, "lambda_b": 1.25, "data": "02/07"
    },
    "Austrália × Egito": {
        "fav": "Egito", "pct_a": 29, "pct_emp": 24, "pct_b": 46,
        "placar": "1×1", "lambda_a": 1.28, "lambda_b": 1.67, "data": "03/07"
    },
    "Argentina × Cabo Verde": {
        "fav": "Argentina", "pct_a": 54, "pct_emp": 24, "pct_b": 20,
        "placar": "1×0", "lambda_a": 1.65, "lambda_b": 0.90, "data": "03/07"
    },
    "Colômbia × Gana": {
        "fav": "Colômbia", "pct_a": 60, "pct_emp": 23, "pct_b": 16,
        "placar": "1×0", "lambda_a": 1.75, "lambda_b": 0.76, "data": "03/07"
    },
}

# ── RESULTADOS REAIS (preencher conforme os jogos acontecem) ──────────────────
# "Time A × Time B": "gols_a×gols_b"  (resultado nos 90min)
# Se foi prorrogação/pênaltis, coloque o placar normal dos 90min mesmo.
# Ex: "Brasil × Japão": "1×1"  (se foi 1×1 → prorrogação)

RESULTADOS = {
    "Canadá × África do Sul": "1×0",  # confirmado
    "Brasil × Japão": "2×1",  # confirmado - gols: Casemiro, Martinelli (BRA); Sano (JPN)
    "Alemanha × Paraguai": "1×1",  # 90min: Enciso (PAR); Paraguai venceu pênaltis 4×3 — ZEBRA (modelo: Alemanha 66%)
    # "Países Baixos × Marrocos": "?×?",
    # "Costa do Marfim × Noruega": "?×?",
    # "França × Suécia": "?×?",
    # "México × Equador": "?×?",
    # "Inglaterra × RD Congo": "?×?",
    # "Bélgica × Senegal": "?×?",
    # "EUA × Bósnia": "?×?",
    # "Espanha × Áustria": "?×?",
    # "Portugal × Croácia": "?×?",
    # "Suíça × Argélia": "?×?",
    # "Austrália × Egito": "?×?",
    # "Argentina × Cabo Verde": "?×?",
    # "Colômbia × Gana": "?×?",
}

# ── LÓGICA DE AVALIAÇÃO ───────────────────────────────────────────────────────

def vencedor_90min(placar_str, time_a, time_b):
    """Quem venceu nos 90min (ou 'Empate')."""
    g = placar_str.split("×")
    ga, gb = int(g[0]), int(g[1])
    if ga > gb: return time_a
    if gb > ga: return time_b
    return "Empate"

def avaliar():
    acertos_fav  = 0   # modelo acertou o favorito
    acertos_placar = 0 # modelo acertou o placar exato
    total = 0

    linhas = []
    for jogo, prev in PREVISOES.items():
        resultado = RESULTADOS.get(jogo)
        if not resultado:
            continue
        total += 1
        time_a, time_b = [t.strip() for t in jogo.split("×")]
        venc_real = vencedor_90min(resultado, time_a, time_b)

        fav_ok     = (venc_real == prev["fav"]) or \
                     (venc_real == "Empate" and prev["fav"] == "Empate")
        placar_ok  = resultado == prev["placar"]

        if fav_ok:     acertos_fav  += 1
        if placar_ok:  acertos_placar += 1

        icone = "✅" if fav_ok else "❌"
        placar_icone = "🎯" if placar_ok else ""
        linhas.append(
            f"{icone} {prev['data']}  {jogo:35s}  "
            f"Prev: {prev['placar']} ({prev['fav']})  |  "
            f"Real: {resultado} ({venc_real})  {placar_icone}"
        )

    print("=" * 80)
    print("  COPA 2026 · Previsões Poisson vs Resultados Reais")
    print("=" * 80)
    for l in linhas:
        print(l)
    print("-" * 80)
    if total:
        print(f"  Jogos avaliados : {total}/16")
        print(f"  Favorito certo  : {acertos_fav}/{total}  ({acertos_fav/total*100:.0f}%)")
        print(f"  Placar exato    : {acertos_placar}/{total}  ({acertos_placar/total*100:.0f}%)")
    else:
        print("  Nenhum resultado registrado ainda.")
    print("=" * 80)

if __name__ == "__main__":
    avaliar()
