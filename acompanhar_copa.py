"""
acompanhar_copa.py
==================
Script diário para registrar resultados do mata-mata da Copa 2026
e verificar a acurácia da simulação Monte Carlo.

Como usar:
  python acompanhar_copa.py          → mostra situação atual
  python acompanhar_copa.py --add    → modo interativo para adicionar jogo
  python acompanhar_copa.py --html   → atualiza a seção de resultados no index.html
"""

import json, math, sys, os
from datetime import date

# ── Arquivo de dados ────────────────────────────────────────────────────────
RESULTADOS_FILE = "resultados_copa2026.json"
HTML_FILE       = "index.html"

# ── Scores do modelo (MERIT_DATA) ───────────────────────────────────────────
SCORES = {
    "Espanha": 1.51, "Alemanha": 1.38, "França": 1.29, "Argentina": 1.27,
    "Brasil": 1.24, "Inglaterra": 1.21, "Países Baixos": 1.18, "Canadá": 1.15,
    "Portugal": 1.13, "Colômbia": 1.10, "Bélgica": 1.08, "Marrocos": 1.05,
    "Estados Unidos": 1.02, "México": 0.99, "Uruguai": 0.96, "Senegal": 0.93,
    "Croácia": 0.90, "Suíça": 0.88, "Japão": 0.85, "Turquia": 0.82,
    "Dinamarca": 0.79, "Equador": 0.76, "Áustria": 0.73, "Polônia": 0.70,
    "Coreia do Sul": 0.24, "Austrália": 0.21, "Costa do Marfim": 0.18,
    "Argélia": 0.15, "Gana": 0.12, "Egito": 0.09, "Bósnia e Herz.": 0.06,
    "Suécia": 0.03, "Noruega": 0.00,
    "África do Sul": -0.38, "Paraguai": -1.06, "Cabo Verde": -0.45,
    "RD Congo": -0.52, "Gana": -0.60,
}

# ── Bracket R32 simulado ─────────────────────────────────────────────────────
R32_SIMULADO = [
    ("Espanha",       "Paraguai"),
    ("Alemanha",      "Cabo Verde"),
    ("Países Baixos", "RD Congo"),
    ("Bélgica",       "Austrália"),
    ("França",        "Gana"),
    ("Inglaterra",    "Egito"),
    ("Colômbia",      "Japão"),
    ("Argentina",     "Noruega"),
    ("Marrocos",      "África do Sul"),
    ("Canadá",        "Áustria"),
    ("Brasil",        "Bósnia e Herz."),
    ("Suíça",         "Costa do Marfim"),
    ("México",        "Croácia"),
    ("Estados Unidos","Argélia"),
    ("Senegal",       "Equador"),
    ("Portugal",      "Suécia"),
]


def p_vitoria(time_a, time_b, k=1.5):
    """Probabilidade de time_a vencer time_b — Bradley-Terry."""
    sa = SCORES.get(time_a, 0.0)
    sb = SCORES.get(time_b, 0.0)
    return round(1 / (1 + math.exp(-k * (sa - sb))), 3)


def favorito(time_a, time_b):
    """Retorna o favorito do modelo e sua probabilidade."""
    p = p_vitoria(time_a, time_b)
    if p >= 0.5:
        return time_a, p
    return time_b, round(1 - p, 3)


def carregar_resultados():
    if os.path.exists(RESULTADOS_FILE):
        with open(RESULTADOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"jogos": []}


def salvar_resultados(dados):
    with open(RESULTADOS_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def mostrar_situacao(dados):
    jogos = dados["jogos"]
    print(f"\n{'='*60}")
    print(f"  COPA DO MUNDO 2026 — Acompanhamento do Mata-Mata")
    print(f"  {date.today().strftime('%d/%m/%Y')}")
    print(f"{'='*60}")

    if not jogos:
        print("\n  Nenhum resultado registrado ainda.")
    else:
        acertos = sum(1 for j in jogos if j["vencedor"] == j["favorito_modelo"])
        total   = len(jogos)

        print(f"\n  Jogos registrados : {total}")
        print(f"  Acertos do modelo : {acertos}/{total}  ({100*acertos//total}%)")
        print()

        rodadas = {}
        for j in jogos:
            rodadas.setdefault(j["rodada"], []).append(j)

        for rodada, lista in rodadas.items():
            print(f"  ── {rodada} ──")
            for j in lista:
                acertou = "✓" if j["vencedor"] == j["favorito_modelo"] else "✗"
                cor_fav = j["favorito_modelo"]
                placar  = j.get("placar", "? – ?")
                p       = j.get("prob_favorito", "?")
                print(f"  {acertou}  {j['time_a']} {placar} {j['time_b']}")
                print(f"      Favorito: {cor_fav} ({p*100:.0f}%)  →  Vencedor real: {j['vencedor']}")
            print()

    print(f"{'='*60}\n")


def adicionar_jogo(dados):
    print("\n── Registrar novo resultado ──")
    print("Rodadas disponíveis: Oitavas (R32), Quartas, Semifinal, Final")
    rodada  = input("Rodada: ").strip() or "Oitavas (R32)"
    time_a  = input("Time A (ex: Brasil): ").strip()
    time_b  = input("Time B (ex: Croácia): ").strip()
    placar  = input("Placar (ex: 2-1): ").strip()
    vencedor = input(f"Vencedor ({time_a} ou {time_b}): ").strip()

    fav, prob = favorito(time_a, time_b)
    acertou   = "✓ ACERTOU" if vencedor == fav else "✗ SURPRESA"

    print(f"\n  Favorito do modelo: {fav} ({prob*100:.0f}%)")
    print(f"  Resultado: {acertou}")

    dados["jogos"].append({
        "data"             : str(date.today()),
        "rodada"           : rodada,
        "time_a"           : time_a,
        "time_b"           : time_b,
        "placar"           : placar,
        "vencedor"         : vencedor,
        "favorito_modelo"  : fav,
        "prob_favorito"    : prob,
    })
    salvar_resultados(dados)
    print(f"\n  Jogo salvo em {RESULTADOS_FILE}")


def gerar_html_card(jogo):
    """Gera o HTML de um card de resultado."""
    acertou    = jogo["vencedor"] == jogo["favorito_modelo"]
    cor_borda  = "#bbf7d0" if acertou else "#fecaca"
    cor_bg     = "#f0fdf4" if acertou else "#fff1f2"
    badge_bg   = "#15803d" if acertou else "#dc2626"
    badge_txt  = "✓ Favorito venceu" if acertou else "✗ Surpresa"
    venc_lado  = "a" if jogo["vencedor"] == jogo["time_a"] else "b"
    placar     = jogo.get("placar", "? – ?").replace("-", " – ")
    prob_pct   = f"{jogo['prob_favorito']*100:.0f}%"

    def time_html(nome, lado):
        score_str = f"score {SCORES.get(nome, '?'):+.2f}" if nome in SCORES else ""
        bold = "font-weight:700;" if jogo["vencedor"] == nome else ""
        check = " ✓" if jogo["vencedor"] == nome else ""
        align = "right" if lado == "a" else "left"
        return f'''<div style="text-align:{align};flex:1">
              <div style="font-size:13px;{bold}color:#0a1a3f">{nome}{check}</div>
              <div style="font-size:11px;color:#9ca3af">{score_str}</div>
            </div>'''

    return f'''      <div style="background:{cor_bg};border:1.5px solid {cor_borda};border-radius:14px;padding:14px 16px">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap">
          <div style="display:flex;align-items:center;gap:12px;flex:1;min-width:200px">
            {time_html(jogo["time_a"], "a")}
            <div style="font-size:22px;font-weight:800;color:#0a1a3f;min-width:60px;text-align:center">{placar}</div>
            {time_html(jogo["time_b"], "b")}
          </div>
          <div style="display:flex;flex-direction:column;align-items:flex-end;gap:4px">
            <span style="background:{badge_bg};color:#fff;font-size:11px;font-weight:700;padding:3px 10px;border-radius:20px">{badge_txt}</span>
            <span style="font-size:11px;color:#5b6b82">Favorito {jogo["favorito_modelo"]} ({prob_pct})</span>
          </div>
        </div>
      </div>'''


def atualizar_html(dados):
    if not os.path.exists(HTML_FILE):
        print(f"  Arquivo {HTML_FILE} não encontrado na pasta atual.")
        return

    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    jogos  = dados["jogos"]
    total  = len(jogos)
    acertos = sum(1 for j in jogos if j["vencedor"] == j["favorito_modelo"])
    pct    = f"{100*acertos//total}%" if total else "—"

    # Gerar cards agrupados por rodada
    rodadas = {}
    for j in jogos:
        rodadas.setdefault(j["rodada"], []).append(j)

    cards_html = ""
    for rodada, lista in rodadas.items():
        cards_html += f'\n    <div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:14px 0 8px">{rodada}</div>\n'
        for j in lista:
            cards_html += gerar_html_card(j) + "\n"

    # Nota final
    nota = ""
    surpresas = [j for j in jogos if j["vencedor"] != j["favorito_modelo"]]
    if surpresas:
        nomes = ", ".join(j["vencedor"] for j in surpresas)
        nota = f'<p class="note" style="margin-top:14px">⚡ Surpresas do torneio: <b>{nomes}</b> eliminaram os favoritos do modelo.</p>'
    else:
        nota = '<p class="note" style="margin-top:14px">💡 Até agora o modelo acertou todos os vencedores — os times com maior score ajustado avançaram como esperado.</p>'

    novo_conteudo = f'''<section id="resultados">
  <h2>🏆 Resultados do Mata-Mata <span class="tag t-v">ao vivo</span></h2>
  <p class="section-intro">Resultados reais confrontados com a simulação Monte Carlo. Verde = modelo acertou. Vermelho = surpresa.</p>

  <div id="resultados-lista" style="display:flex;flex-direction:column;gap:10px">
{cards_html}  </div>

  <div id="resultados-resumo" style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px">
    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:12px 18px;text-align:center;flex:1;min-width:110px">
      <div style="font-size:28px;font-weight:800;color:#15803d">{total}</div>
      <div style="font-size:12px;color:#5b6b82">Jogos disputados</div>
    </div>
    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:12px 18px;text-align:center;flex:1;min-width:110px">
      <div style="font-size:28px;font-weight:800;color:#15803d">{acertos}/{total}</div>
      <div style="font-size:12px;color:#5b6b82">Favoritos passaram</div>
    </div>
    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:12px 18px;text-align:center;flex:1;min-width:110px">
      <div style="font-size:28px;font-weight:800;color:#15803d">{pct}</div>
      <div style="font-size:12px;color:#5b6b82">Acurácia do modelo</div>
    </div>
  </div>
  {nota}
</section>

'''

    # Substituir seção existente
    import re
    html_novo = re.sub(
        r'<section id="resultados">.*?</section>\s*\n',
        novo_conteudo,
        html,
        flags=re.DOTALL
    )

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_novo)
    print(f"  ✓ {HTML_FILE} atualizado com {total} jogo(s).")


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    dados = carregar_resultados()

    # Inicializa com o primeiro resultado se arquivo não existir
    if not dados["jogos"]:
        dados["jogos"].append({
            "data"            : "2026-06-28",
            "rodada"          : "Oitavas (R32)",
            "time_a"          : "África do Sul",
            "time_b"          : "Canadá",
            "placar"          : "0 – 1",
            "vencedor"        : "Canadá",
            "favorito_modelo" : "Canadá",
            "prob_favorito"   : p_vitoria("Canadá", "África do Sul"),
        })
        salvar_resultados(dados)
        print("  → Primeiro resultado registrado automaticamente.")

    if "--add" in sys.argv:
        adicionar_jogo(dados)

    if "--html" in sys.argv:
        dados = carregar_resultados()
        atualizar_html(dados)

    mostrar_situacao(dados)
