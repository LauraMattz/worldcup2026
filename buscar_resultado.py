"""
Script para buscar resultados de jogos da Copa automaticamente.
Usa múltiplas fontes para garantir confiabilidade.
"""

import requests
import re
import json
from datetime import datetime

def normalizar_nome(nome):
    """Normaliza nomes de times para comparação."""
    mapa = {
        "germany": "Alemanha",
        "alemanha": "Alemanha",
        "paraguay": "Paraguai",
        "paraguai": "Paraguai",
        "netherlands": "Países Baixos",
        "países baixos": "Países Baixos",
        "paises baixos": "Países Baixos",
        "holanda": "Países Baixos",
        "morocco": "Marrocos",
        "marrocos": "Marrocos",
        "brasil": "Brasil",
        "brazil": "Brasil",
        "japao": "Japão",
        "japan": "Japão",
        "japão": "Japão",
    }
    nome_lower = nome.lower().strip()
    return mapa.get(nome_lower, nome)

def buscar_resultado_google(time_a, time_b):
    """
    Busca resultado via pesquisa no Google (usando headers para simular navegador).
    """
    query = f"{time_a} vs {time_b} world cup 2026 score result"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text

        # Regex para encontrar placares tipo "2-1", "3 - 0", etc
        padrao_placar = r'(\d+)\s*[-–]\s*(\d+)'
        matches = re.findall(padrao_placar, html)

        if matches:
            gols_a, gols_b = matches[0]
            placar = f"{gols_a}-{gols_b}"

            # Determinar vencedor
            if int(gols_a) > int(gols_b):
                vencedor = time_a
            elif int(gols_b) > int(gols_a):
                vencedor = time_b
            else:
                vencedor = "Empate"

            return {
                "placar": placar,
                "vencedor": vencedor,
                "fonte": "Google Search"
            }
    except Exception as e:
        print(f"❌ Erro ao buscar no Google: {e}")

    return None

def buscar_resultado_api_football(time_a, time_b):
    """
    Busca resultado em API pública de futebol.
    Nota: Requer API key gratuita do api-football.com
    """
    # Por enquanto retorna None - pode ser implementado com API key
    return None

def buscar_resultado_olympics(jogo_key):
    """
    Tenta buscar resultado no site Olympics.com (fonte oficial).
    """
    url_base = "https://www.olympics.com/pt/noticias/copa-do-mundo-2026-jogos-hoje-onde-assistir"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url_base, headers=headers, timeout=10)
        html = response.text

        # Procurar por padrões de placar no HTML
        # Exemplo: "Brasil 2 x 1 Japão" ou "Brasil 2-1 Japão"
        times = jogo_key.split(' × ')
        if len(times) == 2:
            time_a, time_b = times[0].strip(), times[1].strip()

            # Regex flexível para encontrar o jogo e placar
            padrao = rf'{time_a}.*?(\d+)\s*[-x×]\s*(\d+).*?{time_b}'
            match = re.search(padrao, html, re.IGNORECASE)

            if match:
                gols_a, gols_b = match.groups()
                placar = f"{gols_a}-{gols_b}"

                if int(gols_a) > int(gols_b):
                    vencedor = time_a
                elif int(gols_b) > int(gols_a):
                    vencedor = time_b
                else:
                    vencedor = "Empate"

                return {
                    "placar": placar,
                    "vencedor": vencedor,
                    "fonte": "Olympics.com"
                }
    except Exception as e:
        print(f"❌ Erro ao buscar no Olympics.com: {e}")

    return None

def buscar_resultado(time_a, time_b):
    """
    Busca resultado usando múltiplas fontes.
    Retorna: {"placar": "2-1", "vencedor": "Time A", "fonte": "..."}
    """
    print(f"🔍 Buscando resultado de {time_a} × {time_b}...")

    # Tentar múltiplas fontes
    resultado = None

    # 1. Tentar Google
    resultado = buscar_resultado_google(time_a, time_b)
    if resultado:
        print(f"✅ Resultado encontrado via {resultado['fonte']}: {resultado['placar']}")
        return resultado

    # 2. Tentar Olympics.com
    jogo_key = f"{time_a} × {time_b}"
    resultado = buscar_resultado_olympics(jogo_key)
    if resultado:
        print(f"✅ Resultado encontrado via {resultado['fonte']}: {resultado['placar']}")
        return resultado

    # 3. Tentar API (se configurada)
    resultado = buscar_resultado_api_football(time_a, time_b)
    if resultado:
        print(f"✅ Resultado encontrado via {resultado['fonte']}: {resultado['placar']}")
        return resultado

    print(f"⚠️  Não foi possível encontrar resultado automático para {time_a} × {time_b}")
    return None

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Uso: python buscar_resultado.py 'Time A' 'Time B'")
        sys.exit(1)

    time_a = sys.argv[1]
    time_b = sys.argv[2]

    resultado = buscar_resultado(time_a, time_b)

    if resultado:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"erro": "Resultado não encontrado"}, ensure_ascii=False))
        sys.exit(1)
