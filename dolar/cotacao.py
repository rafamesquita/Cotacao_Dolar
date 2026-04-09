import json
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

URL = "https://www.remessaonline.com.br/cotacao/cotacao-dolar"
TAG_HTML = "p"
CLASS = "styles_quoteTitle__fQWzD"

_ROOT = Path(__file__).resolve().parent.parent
_DATA_DIR = _ROOT / "data"
JSON_PATH = _DATA_DIR / "banco_cotacoes.json"


def carregar_historico():
    if not JSON_PATH.exists():
        return []
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError:
        return []
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        for key in ("cotacoes", "historico", "dados"):
            inner = raw.get(key)
            if isinstance(inner, list):
                return inner
    return []


def obter_cotacao():
    # Adicionar um cabeçalho (User-Agent) simula um navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 1. Fazer a requisição HTTP para obter o HTML
    resposta = requests.get(URL, headers=headers)

    # Verificar se a requisição foi bem sucedida (código 200)
    if resposta.status_code != 200:
        print(f"Erro ao acessar a página. Código de status: {resposta.status_code}")
        return

    # 2. Analisar (parse) o HTML com BeautifulSoup
    sopa = BeautifulSoup(resposta.text, "html.parser")

    # 3. Raspa o valor principal
    dolar = sopa.find(TAG_HTML, {"class": CLASS})

    if dolar:
        return dolar.text

    return None


def salvar_no_json(novo_valor):
    # 1. Carrega os dados existentes
    dados = carregar_historico()

    # 2. Verifica se o valor é diferente do último salvo
    valor_mudou = True
    if dados:
        ultimo_registro = dados[-1]
        # Comparamos apenas o valor numérico
        if ultimo_registro["valor"] == novo_valor:
            valor_mudou = False

    # 3. Se for diferente (ou se for o primeiro), adiciona e salva
    if valor_mudou:
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        novo_registro = {
            "data_hora": agora,
            "valor": novo_valor
        }
        dados.append(novo_registro)

        _DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print(f"Sucesso: Novo valor salvo: {novo_valor} em {agora}")
    else:
        print(f"O valor não mudou ({novo_valor}). Nada foi registrado.")
