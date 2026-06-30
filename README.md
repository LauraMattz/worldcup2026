# ⚽ Copa do Mundo 2026 — Análise Preditiva e Acompanhamento em Tempo Real

**Relatório interativo de análise estatística e acompanhamento ao vivo da Copa do Mundo 2026**

![Status](https://img.shields.io/badge/status-ao%20vivo-brightgreen) ![Acurácia](https://img.shields.io/badge/acur%C3%A1cia-67%25-orange) ![Jogos](https://img.shields.io/badge/jogos-3%2F16-blue) ![Surpresas](https://img.shields.io/badge/surpresas-1-red)

## 📊 Sobre o Projeto

Este projeto combina **análise preditiva** com **acompanhamento em tempo real** da fase de mata-mata da Copa do Mundo 2026. Utilizamos dois modelos estatísticos complementares:

1. **Modelo Bradley-Terry (Monte Carlo)** — 10.000 simulações do mata-mata baseadas em scores ajustados de desempenho
2. **Modelo Poisson (xG)** — Previsões de placares usando expected goals e força defensiva

O objetivo é avaliar a acurácia de modelos probabilísticos confrontando previsões com resultados reais, jogo a jogo.

---

## 🎯 Funcionalidades

- **Simulação Monte Carlo** de 10.000 cenários da fase eliminatória
- **Previsões Poisson** de placares e probabilidades para cada jogo das oitavas
- **Acompanhamento ao vivo** dos resultados reais vs. previsões
- **Dashboard interativo** com visualizações ECharts 5.5
- **Análise de clusters** de 48 seleções (Elite, Competitivas, Intermediárias, Baixo Desempenho)
- **Tracking de acurácia** em tempo real (favoritos, placares, surpresas)

---

## 📁 Estrutura do Projeto

```
worldcup2026/
├── .github/workflows/
│   ├── atualizar-automatico.yml    # Workflow agendado (cron)
│   └── atualizar-resultados.yml    # Workflow manual
├── index.html                      # Relatório web interativo (standalone)
├── acompanhar_copa.py              # Script de registro e atualização de resultados
├── buscar_resultado.py             # Web scraping automático de resultados
├── previsao_vs_resultado.py        # Validação de previsões Poisson
├── resultados_copa2026.json        # Base de dados dos jogos disputados
├── analise_copa_2026_machine_learning.ipynb  # Análise completa em Python
└── README.md                       # Este arquivo
```

---

## 🚀 Como Usar

### 1️⃣ Visualizar o Relatório

Acesse o relatório interativo hospedado no GitHub Pages:

👉 **[Ver Relatório Completo](https://lauramattz.github.io/worldcup2026/)**

Ou abra `index.html` localmente no navegador (funciona offline).

---

### 2️⃣ Registrar Novo Resultado

#### 🤖 **Método 1: GitHub Actions (Recomendado)**

O jeito mais fácil é usar o workflow automatizado direto no GitHub:

1. Vá para **[Actions](https://github.com/LauraMattz/worldcup2026/actions)**
2. Clique em **"Atualizar Resultados da Copa"** no menu lateral
3. Clique em **"Run workflow"** no canto superior direito
4. Preencha os campos:
   - **Time A**: Nome do primeiro time (ex: `Alemanha`)
   - **Time B**: Nome do segundo time (ex: `Paraguai`)
   - **Placar**: Resultado final (ex: `2-0`)
   - **Vencedor**: Time que venceu (nome completo)
   - **Rodada**: (opcional, padrão: `Oitavas (R32)`)
5. Clique em **"Run workflow"**

O script vai:
- ✅ Adicionar o resultado ao `resultados_copa2026.json`
- ✅ Atualizar `previsao_vs_resultado.py` automaticamente
- ✅ Regenerar `index.html` com os cards atualizados
- ✅ Fazer commit e push das mudanças
- ✅ GitHub Pages atualiza em ~1 minuto

#### 💻 **Método 2: Linha de Comando (Local)**

Quando um jogo das oitavas terminar, use o script `acompanhar_copa.py`:

```bash
# Visualizar situação atual
python acompanhar_copa.py

# Adicionar novo resultado (modo interativo)
python acompanhar_copa.py --add

# Atualizar automaticamente o index.html
python acompanhar_copa.py --html
```

**Exemplo de uso:**
```
$ python acompanhar_copa.py --add
── Registrar novo resultado ──
Rodada: Oitavas (R32)
Time A: Brasil
Time B: Japão
Placar: 2-1
Vencedor: Brasil

  Favorito do modelo: Brasil (64%)
  Resultado: ✓ ACERTOU
```

---

### 3️⃣ Verificar Previsões Poisson

Para avaliar as previsões de placar baseadas em xG:

```bash
python previsao_vs_resultado.py
```

**Output esperado:**
```
================================================================================
  COPA 2026 · Previsões Poisson vs Resultados Reais
================================================================================
✅ 28/06  Canadá × África do Sul          Prev: 1×0 (Canadá)  |  Real: 1×0 (Canadá)  🎯
✅ 29/06  Brasil × Japão                  Prev: 1×1 (Brasil)  |  Real: 2×1 (Brasil)
--------------------------------------------------------------------------------
  Jogos avaliados : 2/16
  Favorito certo  : 2/2  (100%)
  Placar exato    : 1/2  (50%)
================================================================================
```

---

## 📈 Metodologia

### Modelo Bradley-Terry (Simulação Monte Carlo)

**Score Ajustado:**
```
Score = 0.60 × (xG − xGA) + 0.25 × força_adversários + 0.15 × (posição_FIFA / 100)
```

**Probabilidade de vitória:**
```
P(A vence B) = 1 / (1 + exp(-k × (score_A − score_B)))
```
onde `k = 1.5` (parâmetro de escala).

**Processo:**
1. Calcular scores ajustados para as 48 seleções
2. Definir bracket das oitavas baseado em classificação dos grupos
3. Simular 10.000 torneios completos (oitavas → quartas → semi → final)
4. Agregar probabilidades de avanço por rodada

### Modelo Poisson (Previsões de Placar)

**Expected goals (λ):**
```
λ_time = média(xG_time, xGA_adversário)
```

**Probabilidade de placar X×Y:**
```
P(X, Y) = Poisson(λ_A, X) × Poisson(λ_B, Y)
```

Fonte de dados: [FootyStats.org](https://footystats.org)

---

## 🎨 Stack Tecnológico

| Tecnologia | Uso |
|-----------|-----|
| **Python 3.12** | Scripts de análise e atualização |
| **JSON** | Armazenamento de resultados |
| **ECharts 5.5** | Visualizações interativas (gráficos de rede, barras, radar) |
| **HTML5 + CSS3** | Interface standalone sem dependências |
| **GitHub Pages** | Hospedagem do relatório |

**Bibliotecas Python:**
- `json` — manipulação de dados
- `math` — cálculos probabilísticos
- `re` — parsing e substituição de HTML

---

## 📊 Resultados Atuais

| Métrica | Valor |
|---------|-------|
| **Jogos disputados** | 3/16 |
| **Favoritos que passaram** | 2/3 (67%) |
| **Acurácia do modelo** | 67% |
| **Placares exatos (Poisson)** | 1/3 (33%) |
| **Surpresas** | 1 🚨 |

**Jogos registrados:**
- ✅ **Canadá 1×0 África do Sul** — Favorito: Canadá (91%) ✓
- ✅ **Brasil 2×1 Japão** — Favorito: Brasil (64%) ✓
- 🚨 **Alemanha 1(3)×1(4) Paraguai** — Favorito: Alemanha (99.5%) ✗ **ZEBRA!**

---

## 🔄 Atualização

Os resultados são atualizados **automaticamente via GitHub Actions**:

### 🤖 Atualização Automática (Recomendado)
O workflow `atualizar-automatico.yml` roda automaticamente após cada jogo:
- Busca resultados via web scraping (Google, Olympics.com)
- Atualiza JSON, Python e HTML automaticamente
- Faz commit e push sem intervenção manual

### 💻 Atualização Manual (Fallback)
Se necessário, use:
```bash
python acompanhar_copa.py --add
python acompanhar_copa.py --html
git add . && git commit -m "Atualizar resultado Jogo X"
git push origin main
```

O GitHub Pages reflete as mudanças automaticamente em ~1 minuto.

---

## 👥 Autores

**Laura Mattos** ([@LauraMattz](https://github.com/LauraMattz)) — Desenvolvimento e análise estatística

---

## 📄 Licença

Este projeto é de código aberto para fins educacionais e de pesquisa.

---

## 🔗 Links Úteis

- [Relatório Interativo](https://lauramattz.github.io/worldcup2026/)
- [Dados de xG — FootyStats](https://footystats.org)
- [Documentação do ECharts](https://echarts.apache.org/en/index.html)

---

**Última atualização:** 29/06/2026 — 🚨 Paraguai elimina Alemanha nos pênaltis (1ª surpresa do torneio!)
