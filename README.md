# Copa do Mundo 2026 — Análise Estatística

Relatório interativo da fase de grupos da Copa do Mundo 2026, combinando métricas de desempenho, perfis estatísticos e simulação do mata-mata via Monte Carlo.

**[Ver relatório ao vivo](https://lauramattz.github.io/worldcup2026)**

---

## O que o projeto faz

- Calcula o **Score Ajustado** de cada seleção: combina saldo de xG, força dos adversários e desempenho relativo ao ranking FIFA
- Agrupa as 48 seleções em 4 perfis por clustering (Elite, Competitivas, Intermediárias, Baixo desempenho)
- Mapeia correlações entre as principais variáveis ofensivas e defensivas
- Analisa se cada classificação foi merecida ou fruto de sorte (processo × resultado)
- Simula 10.000 vezes o chaveamento completo do mata-mata (R32 a final) usando o modelo **Bradley-Terry**
- Acompanha os resultados reais do mata-mata e compara com as previsões

## Métricas usadas

| Métrica | Descrição |
|---|---|
| xG/jogo | Gols esperados criados por jogo |
| xGA/jogo | Gols esperados sofridos por jogo |
| Saldo xG | Diferença entre xG e xGA |
| Score Ajustado | Métrica composta: xGD + força dos adversários + desempenho vs. FIFA Rank |
| Prob. avançar | Frequência de avanço no mata-mata nas 10.000 simulações |

## Estrutura

```
worldcup2026/
├── index.html                              # Relatório interativo (HTML único, sem dependências)
├── analise_copa_2026_machine_learning.ipynb  # Notebook com toda a análise em Python
├── resultados_copa2026.json                # Resultados reais do mata-mata (atualizado manualmente)
├── acompanhar_copa.py                      # Script para registrar e acompanhar resultados diários
└── README.md
```

## Como rodar o notebook

```bash
pip install pandas numpy scikit-learn networkx matplotlib seaborn jupyter
jupyter notebook analise_copa_2026_machine_learning.ipynb
```

## Como atualizar os resultados do mata-mata

```bash
# Ver situação atual
python acompanhar_copa.py

# Registrar novo resultado do dia
python acompanhar_copa.py --add

# Atualizar o index.html com os dados novos
python acompanhar_copa.py --html
```

## Tecnologias

- **Python:** Pandas, NumPy, Scikit-learn, NetworkX
- **Visualização:** ECharts 5.5.0 (embutido no HTML)
- **Simulação:** Monte Carlo + modelo Bradley-Terry
- **Deploy:** GitHub Pages (HTML estático, sem servidor)

## Autores

[Laura Mattos](https://br.linkedin.com/in/lauramattosc) e [Guilherme Cintra](https://www.linkedin.com/in/guicintra-inov-edu/) 
